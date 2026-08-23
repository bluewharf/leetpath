from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_admin
from app.models import Problem, User
from app.seed.loader import load_problems

router = APIRouter(prefix="/admin", tags=["admin"])


class SeedReloadOut(BaseModel):
    imported: int


class PublishIn(BaseModel):
    is_published: bool


class AdminProblemOut(BaseModel):
    id: int
    slug: str
    title: str
    difficulty: str
    source: str
    tags: list[str]
    time_limit_ms: int
    memory_limit_mb: int
    is_published: bool
    created_at: datetime


@router.post("/seed/reload")
def reload_seed(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> SeedReloadOut:
    imported = load_problems(session=db)
    db.commit()
    return SeedReloadOut(imported=imported)


@router.get("/problems")
def list_all_problems(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> list[AdminProblemOut]:
    problems = list(db.scalars(select(Problem).order_by(Problem.id)).all())
    return [
        AdminProblemOut(
            id=p.id,
            slug=p.slug,
            title=p.title,
            difficulty=p.difficulty,
            source=p.source,
            tags=p.tags or [],
            time_limit_ms=p.time_limit_ms,
            memory_limit_mb=p.memory_limit_mb,
            is_published=p.is_published,
            created_at=p.created_at,
        )
        for p in problems
    ]


@router.put("/problems/{problem_id}")
def set_published(
    problem_id: int,
    body: PublishIn,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> AdminProblemOut:
    problem = db.get(Problem, problem_id)
    if problem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="题目不存在")
    problem.is_published = body.is_published
    db.commit()
    db.refresh(problem)
    return AdminProblemOut(
        id=problem.id,
        slug=problem.slug,
        title=problem.title,
        difficulty=problem.difficulty,
        source=problem.source,
        tags=problem.tags or [],
        time_limit_ms=problem.time_limit_ms,
        memory_limit_mb=problem.memory_limit_mb,
        is_published=problem.is_published,
        created_at=problem.created_at,
    )
