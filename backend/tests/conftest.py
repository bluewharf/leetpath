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

    from app.seed import loader as seed_loader

    # 测试一律走 fixtures，禁止读写 app/seed/problems/
    monkeypatch.setattr(seed_loader, "DEFAULT_PROBLEMS_DIR", FIXTURES_DIR)

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
    r = client.post(
        "/api/auth/register",
        json={"username": "alice", "password": "password123", "email": "a@example.com"},
    )
    assert r.status_code == 201
    return client


@pytest.fixture
def user_client(admin_client):
    r = admin_client.post(
        "/api/auth/register",
        json={"username": "bob", "password": "password123"},
    )
    assert r.status_code == 201
    return admin_client
