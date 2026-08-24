from pathlib import Path

from sqlalchemy import create_engine, text

from app.db import ensure_schema
from app.seed.loader import load_problems

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def test_problem_list_and_detail(admin_client):
    r = admin_client.get("/api/problems")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    item = items[0]
    assert item["slug"] == "two-sum"
    assert item["leetcode_id"] == 1
    assert item["title"] == "两数之和"
    assert item["difficulty"] == "easy"
    assert item["source"] == "hot100"
    assert item["tags"] == ["数组", "哈希表"]
    assert item["my_status"] is None
    assert item["has_solution"] is True
    assert item["memory"] is None
    assert "statement_md" not in item

    detail = admin_client.get("/api/problems/two-sum")
    assert detail.status_code == 200
    body = detail.json()
    assert body["slug"] == "two-sum"
    assert body["leetcode_id"] == 1
    assert "题目描述" in body["statement_md"]
    assert body["time_limit_ms"] == 5000
    assert body["memory_limit_mb"] == 256
    assert [s["ordinal"] for s in body["samples"]] == [1, 2]
    assert "2 7 11 15" in body["samples"][0]["input"]
    assert body["samples"][0]["expected_output"].strip() == "0 1"


def test_problem_filters(admin_client):
    assert admin_client.get("/api/problems?difficulty=easy").json()[0]["slug"] == "two-sum"
    assert admin_client.get("/api/problems?difficulty=hard").json() == []
    assert admin_client.get("/api/problems?source=hot100").json()[0]["slug"] == "two-sum"
    assert admin_client.get("/api/problems?source=mianjing").json() == []
    assert admin_client.get("/api/problems?tag=数组").json()[0]["slug"] == "two-sum"
    assert admin_client.get("/api/problems?tag=图论").json() == []
    assert admin_client.get("/api/problems?q=TWO").json()[0]["slug"] == "two-sum"
    assert admin_client.get("/api/problems?q=两数").json()[0]["slug"] == "two-sum"
    assert admin_client.get("/api/problems?q=1").json()[0]["slug"] == "two-sum"
    assert admin_client.get("/api/problems?q=zzzz").json() == []


def test_unpublished_hidden(admin_client):
    listed = admin_client.get("/api/admin/problems").json()
    pid = listed[0]["id"]
    r = admin_client.put(f"/api/admin/problems/{pid}", json={"is_published": False})
    assert r.status_code == 200
    assert r.json()["is_published"] is False
    assert admin_client.get("/api/problems").json() == []
    assert admin_client.get("/api/problems/two-sum").status_code == 404
    admin = admin_client.get("/api/admin/problems").json()
    assert len(admin) == 1
    assert admin[0]["is_published"] is False


def test_my_status_attempted_and_solved(admin_client):
    sub = admin_client.post(
        "/api/submissions",
        json={"problem_slug": "two-sum", "language": "python3", "code": "print(1)"},
    )
    assert sub.status_code == 202
    listed = admin_client.get("/api/problems").json()
    assert listed[0]["my_status"] == "attempted"

    from app import db as dbmod
    from app.models import Submission

    db = dbmod.SessionLocal()
    try:
        row = db.get(Submission, sub.json()["id"])
        row.status = "AC"
        db.commit()
    finally:
        db.close()
    listed = admin_client.get("/api/problems").json()
    assert listed[0]["my_status"] == "solved"


def test_loader_upsert_rebuilds_testcases(client):
    from sqlalchemy import func, select

    from app import db as dbmod
    from app.models import Problem, Testcase

    db = dbmod.SessionLocal()
    try:
        n1 = load_problems(FIXTURES_DIR, session=db)
        db.commit()
        n2 = load_problems(FIXTURES_DIR, session=db)
        db.commit()
        assert n1 == 1 and n2 == 1
        count = db.scalar(select(func.count()).select_from(Problem))
        cases = db.scalar(select(func.count()).select_from(Testcase))
        samples = db.scalar(select(func.count()).select_from(Testcase).where(Testcase.is_sample.is_(True)))
        assert count == 1
        assert cases == 3
        assert samples == 2
    finally:
        db.close()


def test_missing_problem_404(admin_client):
    assert admin_client.get("/api/problems/no-such").status_code == 404


def test_solution_endpoint(admin_client):
    r = admin_client.get("/api/problems/two-sum/solution")
    assert r.status_code == 200
    body = r.json()
    assert body["slug"] == "two-sum"
    assert "## 思路" in body["solution_md"]
    assert "```python" in body["solution_md"]
    assert admin_client.get("/api/problems/no-such/solution").status_code == 404


def test_memory_mark_and_list(admin_client):
    r = admin_client.post("/api/problems/two-sum/memory", json={"remembered": True})
    assert r.status_code == 200
    assert r.json()["memory"] == "remembered"
    assert r.json()["review_count"] == 1

    listed = admin_client.get("/api/problems").json()
    assert listed[0]["memory"] == "remembered"

    r = admin_client.post("/api/problems/two-sum/memory", json={"remembered": False})
    assert r.json()["memory"] == "unremembered"
    assert r.json()["review_count"] == 2
    assert admin_client.get("/api/problems").json()[0]["memory"] == "unremembered"

    assert admin_client.post("/api/problems/no-such/memory", json={"remembered": True}).status_code == 404


def test_ensure_schema_adds_leetcode_id_column(tmp_path):
    db_path = tmp_path / "legacy.db"
    engine = create_engine(f"sqlite:///{db_path.as_posix()}", future=True)
    with engine.begin() as conn:
        conn.execute(
            text(
                "CREATE TABLE problems (id INTEGER PRIMARY KEY, slug VARCHAR(128), title VARCHAR(255))"
            )
        )
    ensure_schema(engine)
    with engine.connect() as conn:
        cols = {row[1] for row in conn.execute(text("PRAGMA table_info(problems)"))}
    assert "leetcode_id" in cols
    ensure_schema(engine)  # 幂等
