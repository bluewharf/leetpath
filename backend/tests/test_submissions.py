def test_create_submission_pending(admin_client):
    r = admin_client.post(
        "/api/submissions",
        json={"problem_slug": "two-sum", "language": "python3", "code": "print(0, 1)\n"},
    )
    assert r.status_code == 202
    body = r.json()
    assert body["status"] == "pending"
    assert "id" in body

    detail = admin_client.get(f"/api/submissions/{body['id']}")
    assert detail.status_code == 200
    d = detail.json()
    assert d["problem_slug"] == "two-sum"
    assert d["problem_title"] == "两数之和"
    assert d["language"] == "python3"
    assert d["code"] == "print(0, 1)\n"
    assert d["status"] == "pending"
    assert d["runtime_ms"] is None
    assert d["compile_output"] is None
    assert d["detail"] is None
    assert "created_at" in d


def test_list_submissions_omits_code(admin_client):
    admin_client.post(
        "/api/submissions",
        json={"problem_slug": "two-sum", "language": "cpp", "code": "int main(){}"},
    )
    listed = admin_client.get("/api/submissions?problem_slug=two-sum&limit=50")
    assert listed.status_code == 200
    items = listed.json()
    assert len(items) >= 1
    assert "code" not in items[0]
    assert items[0]["problem_slug"] == "two-sum"
    assert items[0]["status"] == "pending"


def test_submission_rate_limit(admin_client):
    payload = {"problem_slug": "two-sum", "language": "python3", "code": "print(1)"}
    codes = []
    for _ in range(3):
        codes.append(admin_client.post("/api/submissions", json=payload).status_code)
    assert codes[:2] == [202] * 2
    assert codes[2] == 429


def test_submission_per_minute_limit(admin_client):
    from app import db as dbmod
    from app.models import Submission

    payload = {"problem_slug": "two-sum", "language": "python3", "code": "print(1)"}
    statuses = []
    for _ in range(11):
        response = admin_client.post("/api/submissions", json=payload)
        statuses.append(response.status_code)
        if response.status_code == 202:
            assert dbmod.SessionLocal is not None
            with dbmod.SessionLocal() as db:
                sub = db.get(Submission, response.json()["id"])
                assert sub is not None
                sub.status = "AC"
                db.commit()
    assert statuses[:10] == [202] * 10
    assert statuses[10] == 429


def test_submission_global_queue_limit(admin_client):
    from app import db as dbmod
    from app.auth import hash_password
    from app.models import Problem, Submission, User

    assert dbmod.SessionLocal is not None
    with dbmod.SessionLocal() as db:
        problem = db.query(Problem).filter_by(slug="two-sum").one()
        for index in range(5):
            user = User(
                username=f"queue{index}",
                password_hash=hash_password("password123"),
                is_admin=False,
            )
            db.add(user)
            db.flush()
            for _ in range(2):
                db.add(
                    Submission(
                        user_id=user.id,
                        problem_id=problem.id,
                        language="python3",
                        code="print(1)",
                        status="pending",
                    )
                )
        db.commit()

    response = admin_client.post(
        "/api/submissions",
        json={"problem_slug": "two-sum", "language": "python3", "code": "print(1)"},
    )
    assert response.status_code == 429
    assert response.json()["detail"] == "评测队列繁忙，请稍后再试"


def test_submission_other_user_forbidden(admin_client):
    created = admin_client.post(
        "/api/submissions",
        json={"problem_slug": "two-sum", "language": "python3", "code": "print(1)"},
    )
    sid = created.json()["id"]
    invite = admin_client.post("/api/admin/invites", json={"expires_in_days": 7}).json()["code"]
    admin_client.post("/api/auth/logout")
    admin_client.post(
        "/api/auth/register",
        json={"username": "bob", "password": "password123", "invite_code": invite},
    )
    r = admin_client.get(f"/api/submissions/{sid}")
    assert r.status_code == 403


def test_submission_unknown_problem(admin_client):
    r = admin_client.post(
        "/api/submissions",
        json={"problem_slug": "no-such", "language": "python3", "code": "print(1)"},
    )
    assert r.status_code == 404


def test_submission_invalid_language(admin_client):
    r = admin_client.post(
        "/api/submissions",
        json={"problem_slug": "two-sum", "language": "java", "code": "print(1)"},
    )
    assert r.status_code == 422
