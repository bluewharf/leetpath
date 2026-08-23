from datetime import date, datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user, require_admin
from app.models import Job, User

router = APIRouter(prefix="/jobs", tags=["jobs"])


class JobCreate(BaseModel):
    company: str
    position: str
    tier: Literal["big", "mid", "small"] = "small"
    batch: str | None = None
    open_at: date | None = None
    deadline_at: date | None = None
    jd_text: str | None = None
    apply_url: str | None = None
    status: Literal["open", "closed"] = "open"


class JobUpdate(BaseModel):
    company: str | None = None
    position: str | None = None
    tier: Literal["big", "mid", "small"] | None = None
    batch: str | None = None
    open_at: date | None = None
    deadline_at: date | None = None
    jd_text: str | None = None
    apply_url: str | None = None
    status: Literal["open", "closed"] | None = None


class JobOut(BaseModel):
    id: int
    company: str
    position: str
    tier: str
    batch: str | None
    open_at: date | None
    deadline_at: date | None
    jd_text: str | None
    apply_url: str | None
    status: str
    created_at: datetime
    days_left: int | None


def job_out(job: Job) -> JobOut:
    days_left = None
    if job.deadline_at is not None:
        days_left = (job.deadline_at - date.today()).days
    return JobOut(
        id=job.id,
        company=job.company,
        position=job.position,
        tier=job.tier,
        batch=job.batch,
        open_at=job.open_at,
        deadline_at=job.deadline_at,
        jd_text=job.jd_text,
        apply_url=job.apply_url,
        status=job.status,
        created_at=job.created_at,
        days_left=days_left,
    )


@router.get("")
def list_jobs(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> list[JobOut]:
    jobs = list(
        db.scalars(select(Job).order_by(Job.deadline_at.asc().nulls_last(), Job.id.asc())).all()
    )
    return [job_out(j) for j in jobs]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_job(
    body: JobCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> JobOut:
    job = Job(**body.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job_out(job)


@router.put("/{job_id}")
def update_job(
    job_id: int,
    body: JobUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> JobOut:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="岗位不存在")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(job, key, value)
    db.commit()
    db.refresh(job)
    return job_out(job)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> None:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="岗位不存在")
    db.delete(job)
    db.commit()
