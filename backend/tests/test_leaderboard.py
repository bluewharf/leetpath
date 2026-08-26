from datetime import datetime, timedelta, timezone

from app import db as dbmod
from app.auth import hash_password
from app.models import Problem, QuizQuestion, QuizRecord, QuizSolveEvent, Submission, User


def _seed_users_and_activity():
    assert dbmod.SessionLocal is not None
    with dbmod.SessionLocal() as db:
        admin = db.query(User).filter_by(username="admin").one()
        p2 = Problem(
            slug="second-problem",
            title="第二题",
            difficulty="easy",
            source="hot100",
            statement_md="",
            is_published=True,
        )
        db.add(p2)
        db.flush()
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        db.add_all(
            [
                Submission(
                    user_id=admin.id,
                    problem_id=p2.id,
                    language="python3",
                    code="",
                    status="AC",
                    created_at=now,
                    judged_at=now,
                ),
                Submission(
                    user_id=admin.id,
                    problem_id=p2.id,
                    language="python3",
                    code="",
                    status="AC",
                    created_at=now,
                    judged_at=now,
                ),
            ]
        )
        q = QuizQuestion(
            bank="测试专题",
            category="测试",
            type="single",
            ordinal=1,
            stem="1+1=?",
            options={"A": "2"},
            answer="A",
            analysis="",
        )
        db.add(q)
        db.flush()
        db.add(QuizRecord(user_id=admin.id, question_id=q.id, is_correct=True, user_answer="A"))
        db.add(QuizSolveEvent(user_id=admin.id, question_id=q.id, solved_at=now))
        db.commit()


def test_leaderboard_returns_problem_quiz_and_duration_boards(admin_client):
    _seed_users_and_activity()
    problem = admin_client.get("/api/leaderboard?board=problems&period=today")
    assert problem.status_code == 200
    assert problem.json()["metric"] == "solved_count"
    assert problem.json()["entries"][0]["value"] == 1

    quiz = admin_client.get("/api/leaderboard?board=quiz&period=all")
    assert quiz.status_code == 200
    assert quiz.json()["metric"] == "quiz_solved_count"
    assert quiz.json()["entries"][0]["value"] == 1

    duration = admin_client.get("/api/leaderboard?board=duration&period=today")
    assert duration.status_code == 200
    assert duration.json()["metric"] == "active_seconds"


def test_heartbeat_is_capped_and_idempotent(admin_client):
    first = admin_client.post(
        "/api/activity/heartbeat",
        json={"session_id": "session-a", "surface": "problem", "elapsed_seconds": 60},
    )
    assert first.status_code == 200
    assert first.json()["accepted_seconds"] == 60

    duplicate = admin_client.post(
        "/api/activity/heartbeat",
        json={"session_id": "session-a", "surface": "problem", "elapsed_seconds": 60},
    )
    assert duplicate.status_code == 200
    assert duplicate.json()["accepted_seconds"] == 0

    too_large = admin_client.post(
        "/api/activity/heartbeat",
        json={"session_id": "session-b", "surface": "quiz", "elapsed_seconds": 61},
    )
    assert too_large.status_code == 422


def test_leaderboard_rejects_invalid_dimensions(admin_client):
    assert admin_client.get("/api/leaderboard?board=wat&period=today").status_code == 422
    assert admin_client.get("/api/leaderboard?board=problems&period=month").status_code == 422


def test_all_time_problem_board_keeps_legacy_ac_submissions(admin_client):
    assert dbmod.SessionLocal is not None
    with dbmod.SessionLocal() as db:
        user = db.query(User).filter_by(username="admin").one()
        problem = db.query(Problem).filter_by(slug="two-sum").one()
        db.add(
            Submission(
                user_id=user.id,
                problem_id=problem.id,
                language="python3",
                code="",
                status="AC",
            )
        )
        db.commit()
    response = admin_client.get("/api/leaderboard?board=problems&period=all")
    assert response.status_code == 200
    assert response.json()["entries"][0]["value"] == 1
