from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, field_validator
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Problem, Submission, User

router = APIRouter(prefix="/submissions", tags=["submissions"])

CODE_MAX_BYTES = 64 * 1024
MAX_IN_FLIGHT = 5


class SubmissionCreate(BaseModel):
    problem_slug: str
    language: Literal["python3", "cpp"]
    code: str

    @field_validator("code")
    @classmethod
    def code_size(cls, v: str) -> str:
        if len(v.encode("utf-8")) > CODE_MAX_BYTES:
            raise ValueError("代码长度超过 64KB")
        return v


class SubmissionCreated(BaseModel):
    id: int
    status: str


class SubmissionDetail(BaseModel):
    id: int
    problem_slug: str
    problem_title: str
    language: str
    code: str
    status: str
    runtime_ms: int | None
    compile_output: str | None
    detail: list | dict | None
    created_at: datetime


class SubmissionListItem(BaseModel):
    id: int
    problem_slug: str
    problem_title: str
    language: str
    status: str
    runtime_ms: int | None
    created_at: datetime


@router.post("", status_code=status.HTTP_202_ACCEPTED)
def create_submission(
    body: SubmissionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> SubmissionCreated:
    problem = db.scalar(
        select(Problem).where(Problem.slug == body.problem_slug, Problem.is_published.is_(True))
    )
    if problem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="题目不存在")
    in_flight = db.scalar(
        select(func.count())
        .select_from(Submission)
        .where(
            Submission.user_id == user.id,
            Submission.status.in_(("pending", "judging")),
        )
    )
    if (in_flight or 0) >= MAX_IN_FLIGHT:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="待评测提交过多")
    sub = Submission(
        user_id=user.id,
        problem_id=problem.id,
        language=body.language,
        code=body.code,
        status="pending",
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return SubmissionCreated(id=sub.id, status="pending")


@router.get("")
def list_submissions(
    problem_slug: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[SubmissionListItem]:
    stmt = (
        select(Submission, Problem)
        .join(Problem, Submission.problem_id == Problem.id)
        .where(Submission.user_id == user.id)
        .order_by(Submission.created_at.desc(), Submission.id.desc())
        .limit(limit)
    )
    if problem_slug:
        stmt = stmt.where(Problem.slug == problem_slug)
    rows = db.execute(stmt).all()
    return [
        SubmissionListItem(
            id=sub.id,
            problem_slug=problem.slug,
            problem_title=problem.title,
            language=sub.language,
            status=sub.status,
            runtime_ms=sub.runtime_ms,
            created_at=sub.created_at,
        )
        for sub, problem in rows
    ]


@router.get("/{submission_id}")
def get_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> SubmissionDetail:
    row = db.execute(
        select(Submission, Problem)
        .join(Problem, Submission.problem_id == Problem.id)
        .where(Submission.id == submission_id)
    ).first()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="提交不存在")
    sub, problem = row
    if sub.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权查看该提交")
    return SubmissionDetail(
        id=sub.id,
        problem_slug=problem.slug,
        problem_title=problem.title,
        language=sub.language,
        code=sub.code,
        status=sub.status,
        runtime_ms=sub.runtime_ms,
        compile_output=sub.compile_output,
        detail=sub.detail,
        created_at=sub.created_at,
    )
