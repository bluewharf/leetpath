from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.avatars import avatar_url
from app.models import Problem, QuizSolveEvent, StudySession, Submission, User

LEADERBOARD_TZ = ZoneInfo("Asia/Shanghai")
MAX_ENTRIES = 50


def _window(period: str) -> tuple[datetime | None, date | None]:
    if period == "all":
        return None, None
    local_now = datetime.now(LEADERBOARD_TZ)
    start_date = local_now.date()
    if period == "week":
        start_date -= timedelta(days=local_now.weekday())
    local_start = datetime.combine(start_date, datetime.min.time(), tzinfo=LEADERBOARD_TZ)
    return local_start.astimezone(ZoneInfo("UTC")).replace(tzinfo=None), start_date


def _ranked_rows(
    values: dict[int, tuple[int, datetime | None]],
    users: dict[int, User],
    current_id: int,
):
    rows = [
        {
            "user_id": user_id,
            "username": users[user_id].username,
            "avatar_url": avatar_url(users[user_id]),
            "value": value,
            "first_at": first_at,
        }
        for user_id, (value, first_at) in values.items()
        if value > 0 and user_id in users
    ]
    rows.sort(key=lambda row: (-row["value"], row["first_at"] or datetime.max, row["username"]))
    entries = []
    for index, row in enumerate(rows, start=1):
        entries.append(
            {
                "rank": index,
                "username": row["username"],
                "avatar_url": row["avatar_url"],
                "value": row["value"],
                "is_me": row["user_id"] == current_id,
            }
        )
    me_row = next((entry for entry in entries if entry["is_me"]), None)
    current = users.get(current_id)
    if me_row is None:
        me = {
            "rank": None,
            "username": current.username if current else "",
            "avatar_url": avatar_url(current) if current else None,
            "value": 0,
        }
    else:
        me = {
            "rank": me_row["rank"],
            "username": me_row["username"],
            "avatar_url": me_row["avatar_url"],
            "value": me_row["value"],
        }
    return entries[:MAX_ENTRIES], me


def build_leaderboard(db: Session, user_id: int, board: str, period: str) -> dict:
    start_utc, start_day = _window(period)
    users = {user.id: user for user in db.scalars(select(User)).all()}
    values: dict[int, tuple[int, datetime | None]] = {}

    if board == "problems":
        published_ids = set(
            db.scalars(select(Problem.id).where(Problem.is_published.is_(True))).all()
        )
        firsts: dict[tuple[int, int], datetime] = {}
        for submission in db.scalars(select(Submission).where(Submission.status == "AC")).all():
            if submission.problem_id not in published_ids:
                continue
            solved_at = submission.judged_at or (submission.created_at if period == "all" else None)
            if solved_at is None:
                continue
            key = (submission.user_id, submission.problem_id)
            if key not in firsts or solved_at < firsts[key]:
                firsts[key] = solved_at
        grouped: dict[int, list[datetime]] = defaultdict(list)
        for (uid, _), solved_at in firsts.items():
            if start_utc is None or solved_at >= start_utc:
                grouped[uid].append(solved_at)
        values = {uid: (len(times), min(times)) for uid, times in grouped.items()}
        metric = "solved_count"
    elif board == "quiz":
        grouped: dict[int, list[datetime]] = defaultdict(list)
        for event in db.scalars(select(QuizSolveEvent)).all():
            if start_utc is None or event.solved_at >= start_utc:
                grouped[event.user_id].append(event.solved_at)
        values = {uid: (len(times), min(times)) for uid, times in grouped.items()}
        metric = "quiz_solved_count"
    else:
        grouped_seconds: dict[int, int] = defaultdict(int)
        grouped_first: dict[int, datetime] = {}
        for session in db.scalars(select(StudySession)).all():
            if start_day is not None and session.day < start_day:
                continue
            grouped_seconds[session.user_id] += session.active_seconds
            if session.created_at and (
                session.user_id not in grouped_first or session.created_at < grouped_first[session.user_id]
            ):
                grouped_first[session.user_id] = session.created_at
        values = {
            uid: (seconds, grouped_first.get(uid)) for uid, seconds in grouped_seconds.items()
        }
        metric = "active_seconds"

    entries, me = _ranked_rows(values, users, user_id)
    return {
        "board": board,
        "period": period,
        "timezone": "Asia/Shanghai",
        "metric": metric,
        "me": me,
        "entries": entries,
    }
