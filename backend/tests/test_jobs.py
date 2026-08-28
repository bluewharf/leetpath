from datetime import date, timedelta

import pytest
from sqlalchemy import create_engine, text

from app.db import ensure_schema


def test_jobs_crud_admin(admin_client):
    empty = admin_client.get("/api/jobs")
    assert empty.status_code == 200
    assert empty.json() == []

    soon = (date.today() + timedelta(days=3)).isoformat()
    later = (date.today() + timedelta(days=10)).isoformat()
    created = admin_client.post(
        "/api/jobs",
        json={
            "company": "字节跳动",
            "position": "后端开发",
            "batch": "2026秋招",
            "deadline_at": later,
            "jd_text": "熟悉 Python",
            "apply_url": "https://example.com/apply",
        },
    )
    assert created.status_code == 201
    job = created.json()
    assert job["company"] == "字节跳动"
    assert job["status"] == "open"
    assert job["days_left"] == 10
    job_id = job["id"]

    admin_client.post(
        "/api/jobs",
        json={"company": "阿里巴巴", "position": "客户端", "deadline_at": soon},
    )
    listed = admin_client.get("/api/jobs").json()
    assert [j["company"] for j in listed] == ["阿里巴巴", "字节跳动"]
    assert listed[0]["days_left"] == 3

    updated = admin_client.put(f"/api/jobs/{job_id}", json={"status": "closed", "position": "资深后端"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "closed"
    assert updated.json()["position"] == "资深后端"

    deleted = admin_client.delete(f"/api/jobs/{job_id}")
    assert deleted.status_code == 204
    remaining = admin_client.get("/api/jobs").json()
    assert len(remaining) == 1
    assert remaining[0]["company"] == "阿里巴巴"


def test_jobs_null_deadline_last(admin_client):
    admin_client.post("/api/jobs", json={"company": "无截止日期", "position": "P6"})
    d = (date.today() + timedelta(days=1)).isoformat()
    admin_client.post("/api/jobs", json={"company": "有截止日期", "position": "P6", "deadline_at": d})
    names = [j["company"] for j in admin_client.get("/api/jobs").json()]
    assert names == ["有截止日期", "无截止日期"]
    assert admin_client.get("/api/jobs").json()[1]["days_left"] is None


def test_jobs_non_admin_forbidden(user_client):
    r = user_client.post("/api/jobs", json={"company": "X", "position": "Y"})
    assert r.status_code == 403
    listed = user_client.get("/api/jobs")
    assert listed.status_code == 200


def test_job_track_sync(admin_client, user_client):
    # admin_client / user_client 共享同一 TestClient，注册 bob 后会话已切到 bob，
    # 需要用 login 显式切换回管理员 admin 建岗
    r = admin_client.post("/api/auth/login", json={"username": "admin", "password": "password123"})
    assert r.status_code == 200
    job = admin_client.post("/api/jobs", json={"company": "腾讯", "position": "后端"}).json()
    job_id = job["id"]

    r = user_client.post("/api/auth/login", json={"username": "bob", "password": "password123"})
    assert r.status_code == 200
    assert user_client.get("/api/jobs/track").json() == {}

    r = user_client.put(f"/api/jobs/{job_id}/track", json={"status": "applied"})
    assert r.status_code == 200
    assert r.json()["status"] == "applied"
    assert user_client.get("/api/jobs/track").json() == {str(job_id): "applied"}

    r = user_client.put(f"/api/jobs/{job_id}/track", json={"status": "interview"})
    assert r.json()["status"] == "interview"

    # 非法状态与不存在岗位
    assert user_client.put(f"/api/jobs/{job_id}/track", json={"status": "hacked"}).status_code == 422
    assert user_client.put("/api/jobs/99999/track", json={"status": "applied"}).status_code == 404

    # none 清除
    user_client.put(f"/api/jobs/{job_id}/track", json={"status": "none"})
    assert user_client.get("/api/jobs/track").json() == {}

    # 另一个用户的标记互不影响
    admin_client.post("/api/auth/login", json={"username": "admin", "password": "password123"})
    admin_client.put(f"/api/jobs/{job_id}/track", json={"status": "offer"})
    assert admin_client.get("/api/jobs/track").json() == {str(job_id): "offer"}
    user_client.post("/api/auth/login", json={"username": "bob", "password": "password123"})
    assert user_client.get("/api/jobs/track").json() == {}


def test_delete_job_cascades_existing_tracks(admin_client, user_client):
    admin_client.post("/api/auth/login", json={"username": "admin", "password": "password123"})
    job = admin_client.post("/api/jobs", json={"company": "级联测试", "position": "后端"}).json()
    job_id = job["id"]

    user_client.post("/api/auth/login", json={"username": "bob", "password": "password123"})
    tracked = user_client.put(f"/api/jobs/{job_id}/track", json={"status": "applied"})
    assert tracked.status_code == 200

    admin_client.post("/api/auth/login", json={"username": "admin", "password": "password123"})
    deleted = admin_client.delete(f"/api/jobs/{job_id}")
    assert deleted.status_code == 204

    user_client.post("/api/auth/login", json={"username": "bob", "password": "password123"})
    assert user_client.get("/api/jobs/track").json() == {}


def test_ensure_schema_adds_job_track_delete_cascade_to_legacy_database(tmp_path):
    db_path = tmp_path / "legacy-jobs.db"
    legacy = create_engine(f"sqlite:///{db_path.as_posix()}", future=True)
    with legacy.begin() as conn:
        conn.execute(text("PRAGMA foreign_keys=ON"))
        conn.execute(text("CREATE TABLE users (id INTEGER PRIMARY KEY)"))
        conn.execute(text("CREATE TABLE jobs (id INTEGER PRIMARY KEY)"))
        conn.execute(
            text(
                """
                CREATE TABLE job_tracks (
                    user_id INTEGER NOT NULL,
                    job_id INTEGER NOT NULL,
                    status VARCHAR(16) NOT NULL,
                    updated_at DATETIME NOT NULL,
                    PRIMARY KEY (user_id, job_id),
                    FOREIGN KEY(user_id) REFERENCES users (id),
                    FOREIGN KEY(job_id) REFERENCES jobs (id)
                )
                """
            )
        )
        conn.execute(text("INSERT INTO users (id) VALUES (1)"))
        conn.execute(text("INSERT INTO jobs (id) VALUES (2)"))
        conn.execute(
            text(
                "INSERT INTO job_tracks (user_id, job_id, status, updated_at) "
                "VALUES (1, 2, 'applied', '2026-08-28 00:00:00')"
            )
        )

    ensure_schema(legacy)
    ensure_schema(legacy)

    with legacy.begin() as conn:
        foreign_keys = conn.execute(text("PRAGMA foreign_key_list(job_tracks)")).fetchall()
        job_fk = next(row for row in foreign_keys if row[2] == "jobs" and row[3] == "job_id")
        assert job_fk[6].upper() == "CASCADE"
        assert conn.scalar(text("SELECT count(*) FROM job_tracks")) == 1
        conn.execute(text("DELETE FROM jobs WHERE id = 2"))
        assert conn.scalar(text("SELECT count(*) FROM job_tracks")) == 0

    legacy.dispose()


def test_job_track_cascade_migration_rolls_back_cleanly_on_invalid_legacy_data(tmp_path):
    db_path = tmp_path / "broken-legacy-jobs.db"
    legacy = create_engine(f"sqlite:///{db_path.as_posix()}", future=True)
    with legacy.begin() as conn:
        conn.execute(text("PRAGMA foreign_keys=OFF"))
        conn.execute(text("CREATE TABLE users (id INTEGER PRIMARY KEY)"))
        conn.execute(text("CREATE TABLE jobs (id INTEGER PRIMARY KEY)"))
        conn.execute(
            text(
                """
                CREATE TABLE job_tracks (
                    user_id INTEGER NOT NULL,
                    job_id INTEGER NOT NULL,
                    status VARCHAR(16) NOT NULL,
                    updated_at DATETIME NOT NULL,
                    PRIMARY KEY (user_id, job_id),
                    FOREIGN KEY(user_id) REFERENCES users (id),
                    FOREIGN KEY(job_id) REFERENCES jobs (id)
                )
                """
            )
        )
        conn.execute(text("INSERT INTO users (id) VALUES (1)"))
        conn.execute(
            text(
                "INSERT INTO job_tracks (user_id, job_id, status, updated_at) "
                "VALUES (1, 99, 'applied', '2026-08-28 00:00:00')"
            )
        )

    with pytest.raises(RuntimeError, match="外键迁移后校验失败"):
        ensure_schema(legacy)

    with legacy.begin() as conn:
        tables = {row[0] for row in conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))}
        assert "job_tracks" in tables
        assert "job_tracks__cascade_new" not in tables
        assert conn.scalar(text("SELECT count(*) FROM job_tracks WHERE job_id = 99")) == 1
        job_fk = next(
            row
            for row in conn.execute(text("PRAGMA foreign_key_list(job_tracks)"))
            if row[2] == "jobs" and row[3] == "job_id"
        )
        assert job_fk[6].upper() == "NO ACTION"
        conn.execute(text("INSERT INTO jobs (id) VALUES (99)"))

    ensure_schema(legacy)
    with legacy.begin() as conn:
        job_fk = next(
            row
            for row in conn.execute(text("PRAGMA foreign_key_list(job_tracks)"))
            if row[2] == "jobs" and row[3] == "job_id"
        )
        assert job_fk[6].upper() == "CASCADE"

    legacy.dispose()


def test_job_urls_must_use_https(admin_client):
    base = {"company": "示例公司", "position": "开发", "tier": "small"}
    javascript = admin_client.post("/api/jobs", json={**base, "apply_url": "javascript:alert(1)"})
    assert javascript.status_code == 422
    insecure = admin_client.post("/api/jobs", json={**base, "apply_url": "http://example.com"})
    assert insecure.status_code == 422
    secure = admin_client.post("/api/jobs", json={**base, "apply_url": "https://example.com/apply"})
    assert secure.status_code == 201
    assert secure.json()["apply_url"] == "https://example.com/apply"


@pytest.mark.parametrize("field", ["company", "position", "tier", "status"])
def test_job_update_rejects_null_required_fields(admin_client, field):
    created = admin_client.post(
        "/api/jobs",
        json={"company": "示例公司", "position": "开发", "tier": "small"},
    )
    response = admin_client.put(f"/api/jobs/{created.json()['id']}", json={field: None})
    assert response.status_code == 422


def test_jobs_hide_legacy_non_https_urls(admin_client):
    from app import db as dbmod
    from app.models import Job

    assert dbmod.SessionLocal is not None
    with dbmod.SessionLocal() as db:
        db.add(
            Job(
                company="历史数据",
                position="开发",
                tier="small",
                apply_url="javascript:alert(document.domain)",
                status="open",
            )
        )
        db.commit()

    listed = admin_client.get("/api/jobs")
    assert listed.status_code == 200
    legacy = next(job for job in listed.json() if job["company"] == "历史数据")
    assert legacy["apply_url"] is None


def test_job_import_discards_non_https_urls():
    from app.seed.import_jobs import build_job

    job = build_job(
        {
            "company": "导入公司",
            "role": "开发",
            "apply_url": "javascript:alert(1)",
        },
        today=date(2026, 1, 1),
    )
    assert job.apply_url is None
