from datetime import date, timedelta


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
