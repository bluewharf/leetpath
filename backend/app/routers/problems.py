from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Problem, ReviewCard, Submission, Testcase, User, utcnow

router = APIRouter(prefix="/problems", tags=["problems"])


class ProblemListItem(BaseModel):
    id: int
    slug: str
    leetcode_id: int | None
    title: str
    difficulty: str
    source: str
    tags: list[str]
    my_status: str | None
    has_solution: bool
    memory: str | None  # remembered / unremembered / None（未背过）


class SampleOut(BaseModel):
    ordinal: int
    input: str
    expected_output: str


class ProblemDetail(BaseModel):
    id: int
    slug: str
    leetcode_id: int | None
    title: str
    difficulty: str
    source: str
    tags: list[str]
    statement_md: str
    time_limit_ms: int
    memory_limit_mb: int
    samples: list[SampleOut]
    leetcode_available: bool
    leetcode_starters: dict[str, str] | None = None


def _my_status_map(db: Session, user_id: int) -> dict[int, str]:
    rows = db.execute(
        select(Submission.problem_id, Submission.status).where(Submission.user_id == user_id)
    ).all()
    result: dict[int, str] = {}
    for problem_id, sub_status in rows:
        if sub_status == "AC":
            result[problem_id] = "solved"
        elif problem_id not in result:
            result[problem_id] = "attempted"
    return result


def _memory_map(db: Session, user_id: int) -> dict[int, str]:
    rows = db.execute(
        select(ReviewCard.problem_id, ReviewCard.remembered).where(
            ReviewCard.user_id == user_id
        )
    ).all()
    return {pid: ("remembered" if rem else "unremembered") for pid, rem in rows}


@router.get("")
def list_problems(
    difficulty: str | None = None,
    source: str | None = None,
    tag: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[ProblemListItem]:
    stmt = select(Problem).where(Problem.is_published.is_(True)).order_by(Problem.id)
    if difficulty:
        stmt = stmt.where(Problem.difficulty == difficulty)
    if source:
        stmt = stmt.where(Problem.source == source)
    if q:
        like = f"%{q}%"
        q_filters = [Problem.title.ilike(like), Problem.slug.ilike(like)]
        if q.isdigit():
            q_filters.append(Problem.leetcode_id == int(q))
        stmt = stmt.where(or_(*q_filters))
    problems = list(db.scalars(stmt).all())
    if tag:
        problems = [p for p in problems if tag in (p.tags or [])]
    statuses = _my_status_map(db, user.id)
    memories = _memory_map(db, user.id)
    return [
        ProblemListItem(
            id=p.id,
            slug=p.slug,
            leetcode_id=p.leetcode_id,
            title=p.title,
            difficulty=p.difficulty,
            source=p.source,
            tags=p.tags or [],
            my_status=statuses.get(p.id),
            has_solution=p.solution_md is not None,
            memory=memories.get(p.id),
        )
        for p in problems
    ]


@router.get("/{slug}")
def get_problem(
    slug: str,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> ProblemDetail:
    problem = db.scalar(
        select(Problem).where(Problem.slug == slug, Problem.is_published.is_(True))
    )
    if problem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="题目不存在")
    samples = list(
        db.scalars(
            select(Testcase)
            .where(Testcase.problem_id == problem.id, Testcase.is_sample.is_(True))
            .order_by(Testcase.ordinal)
        ).all()
    )
    from judge.leetcode_catalog import spec_for_problem
    from judge.leetcode_wrap import generate_starter

    spec = spec_for_problem(problem)
    starters = None
    if spec is not None:
        starters = {
            "python3": generate_starter(spec, "python3"),
            "cpp": generate_starter(spec, "cpp"),
        }
    return ProblemDetail(
        id=problem.id,
        slug=problem.slug,
        leetcode_id=problem.leetcode_id,
        title=problem.title,
        difficulty=problem.difficulty,
        source=problem.source,
        tags=problem.tags or [],
        statement_md=problem.statement_md,
        time_limit_ms=problem.time_limit_ms,
        memory_limit_mb=problem.memory_limit_mb,
        samples=[
            SampleOut(ordinal=s.ordinal, input=s.input, expected_output=s.expected_output)
            for s in samples
        ],
        leetcode_available=spec is not None,
        leetcode_starters=starters,
    )


class SolutionOut(BaseModel):
    slug: str
    solution_md: str


@router.get("/{slug}/solution")
def get_solution(
    slug: str,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> SolutionOut:
    problem = db.scalar(
        select(Problem).where(Problem.slug == slug, Problem.is_published.is_(True))
    )
    if problem is None or problem.solution_md is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="题解不存在")
    return SolutionOut(slug=problem.slug, solution_md=problem.solution_md)


class MemoryIn(BaseModel):
    remembered: bool


class MemoryOut(BaseModel):
    slug: str
    memory: str
    review_count: int


@router.post("/{slug}/memory")
def mark_memory(
    slug: str,
    body: MemoryIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MemoryOut:
    problem = db.scalar(
        select(Problem).where(Problem.slug == slug, Problem.is_published.is_(True))
    )
    if problem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="题目不存在")
    card = db.get(ReviewCard, (user.id, problem.id))
    if card is None:
        card = ReviewCard(user_id=user.id, problem_id=problem.id)
        db.add(card)
    card.remembered = body.remembered
    card.review_count = (card.review_count or 0) + 1
    card.updated_at = utcnow()
    db.commit()
    return MemoryOut(
        slug=slug,
        memory="remembered" if card.remembered else "unremembered",
        review_count=card.review_count,
    )
