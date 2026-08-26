from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def test_admin_seed_reload(admin_client, monkeypatch):
    from app.seed import loader

    monkeypatch.setattr(loader, "DEFAULT_PROBLEMS_DIR", FIXTURES_DIR)
    r = admin_client.post("/api/admin/seed/reload")
    assert r.status_code == 200
    assert r.json() == {"imported": 1, "quiz_imported": 0}


def test_non_admin_cannot_access_admin(user_client):
    assert user_client.get("/api/admin/problems").status_code == 403
    assert user_client.post("/api/admin/seed/reload").status_code == 403
    assert user_client.put("/api/admin/problems/1", json={"is_published": False}).status_code == 403


def test_admin_problems_includes_unpublished(admin_client):
    items = admin_client.get("/api/admin/problems").json()
    assert len(items) == 1
    pid = items[0]["id"]
    admin_client.put(f"/api/admin/problems/{pid}", json={"is_published": False})
    again = admin_client.get("/api/admin/problems").json()
    assert again[0]["is_published"] is False
    assert len(admin_client.get("/api/problems").json()) == 0
