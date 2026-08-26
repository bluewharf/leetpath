from pathlib import Path

import pytest
from fastapi.testclient import TestClient

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "leetpath.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path.as_posix()}")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-must-be-32-bytes-min")
    monkeypatch.setenv("COOKIE_SECURE", "false")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("PUBLIC_ORIGIN", "http://testserver")

    from app.seed import loader as seed_loader
    from app.seed import quiz_loader as quiz_seed_loader

    # 测试一律走 fixtures，禁止读写 app/seed/problems/ 与正式八股 JSON
    monkeypatch.setattr(seed_loader, "DEFAULT_PROBLEMS_DIR", FIXTURES_DIR)
    monkeypatch.setattr(quiz_seed_loader, "DEFAULT_JSON_PATH", FIXTURES_DIR / "quiz_questions.json")

    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture
def loaded_problem(client):
    from app import db as dbmod
    from app.seed.loader import load_problems

    assert dbmod.SessionLocal is not None
    db = dbmod.SessionLocal()
    try:
        n = load_problems(FIXTURES_DIR, session=db)
        db.commit()
    finally:
        db.close()
    assert n == 1
    return n


@pytest.fixture
def admin_client(client, loaded_problem):
    from app import db as dbmod
    from app.auth import hash_password
    from app.models import User

    assert dbmod.SessionLocal is not None
    with dbmod.SessionLocal() as db:
        db.add(
            User(
                username="admin",
                email="admin@example.com",
                password_hash=hash_password("password123"),
                is_admin=True,
            )
        )
        db.commit()
    r = client.post("/api/auth/login", json={"username": "admin", "password": "password123"})
    assert r.status_code == 200
    return client


@pytest.fixture
def user_client(admin_client):
    invite = admin_client.post("/api/admin/invites", json={"expires_in_days": 7})
    assert invite.status_code == 201
    code = invite.json()["code"]
    admin_client.post("/api/auth/logout")
    r = admin_client.post(
        "/api/auth/register",
        json={"username": "bob", "password": "password123", "invite_code": code},
    )
    assert r.status_code == 201
    return admin_client
