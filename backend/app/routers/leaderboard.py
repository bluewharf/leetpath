from __future__ import annotations

from zoneinfo import ZoneInfo
from typing import Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import StudySession, User, utcnow
from app.services.leaderboard import build_leaderboard

router = APIRouter(tags=["leaderboard"])


class HeartbeatIn(BaseModel):
    session_id: str = Field(min_length=1, max_length=64)
    surface: Literal["problem", "quiz", "review", "handbook", "jobs"]
    elapsed_seconds: int = Field(ge=1, le=60)


@router.get("/leaderboard")
def leaderboard(
    board: Literal["problems", "quiz", "duration"] = "problems",
    period: Literal["today", "week", "all"] = "today",
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    return build_leaderboard(db, user.id, board, period)


@router.post("/activity/heartbeat")
def heartbeat(
    body: HeartbeatIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict[str, int]:
    now = utcnow()
    local_day = now.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Shanghai")).date()
    session = db.scalar(
        select(StudySession).where(
            StudySession.user_id == user.id,
            StudySession.session_id == body.session_id,
            StudySession.day == local_day,
        )
    )
    if session is None:
        session = StudySession(
            user_id=user.id,
            session_id=body.session_id,
            surface=body.surface,
            day=local_day,
            active_seconds=0,
            last_heartbeat_at=None,
        )
        db.add(session)
        db.flush()

    # 心跳间隔过短时视为重复请求；真实客户端每 30 秒发送一次。
    accepted = body.elapsed_seconds
    if session.last_heartbeat_at is not None:
        gap = (now - session.last_heartbeat_at).total_seconds()
        if gap < 5:
            accepted = 0
    daily_total = db.scalar(
        select(func.coalesce(func.sum(StudySession.active_seconds), 0)).where(
            StudySession.user_id == user.id, StudySession.day == local_day
        )
    ) or 0
    accepted = min(accepted, max(0, 8 * 60 * 60 - int(daily_total)))
    session.active_seconds += accepted
    session.surface = body.surface
    session.last_heartbeat_at = now
    db.commit()
    return {"accepted_seconds": accepted, "daily_seconds": int(daily_total) + accepted}
