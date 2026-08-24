from datetime import datetime


def test_admin_can_create_list_and_revoke_invite(admin_client):
    created = admin_client.post("/api/admin/invites", json={"expires_in_days": 3})
    assert created.status_code == 201
    body = created.json()
    assert len(body["code"]) >= 24
    assert body["used_at"] is None
    assert body["revoked_at"] is None
    assert datetime.fromisoformat(body["expires_at"])

    listed = admin_client.get("/api/admin/invites")
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]
    assert "code" not in listed.json()[0]

    revoked = admin_client.delete(f"/api/admin/invites/{body['id']}")
    assert revoked.status_code == 204
    listed_again = admin_client.get("/api/admin/invites")
    assert listed_again.json()[0]["revoked_at"] is not None


def test_non_admin_cannot_manage_invites(user_client):
    assert user_client.post("/api/admin/invites", json={"expires_in_days": 7}).status_code == 403
    assert user_client.get("/api/admin/invites").status_code == 403


def test_revoked_invite_cannot_register(admin_client):
    created = admin_client.post("/api/admin/invites", json={"expires_in_days": 7})
    code = created.json()["code"]
    admin_client.delete(f"/api/admin/invites/{created.json()['id']}")
    admin_client.post("/api/auth/logout")
    response = admin_client.post(
        "/api/auth/register",
        json={"username": "alice", "password": "password123", "invite_code": code},
    )
    assert response.status_code == 400


def test_create_admin_command_service(client):
    from app import db as dbmod
    from app.manage import create_admin

    assert dbmod.SessionLocal is not None
    with dbmod.SessionLocal() as db:
        user = create_admin(db, "owner", "password123", "owner@example.com")
        assert user.is_admin is True
        assert user.username == "owner"

    login = client.post("/api/auth/login", json={"username": "owner", "password": "password123"})
    assert login.status_code == 200
    assert login.json()["is_admin"] is True
