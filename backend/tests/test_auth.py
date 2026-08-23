from app.config import get_settings
from app.routers.auth import UserOut


def test_register_login_me_logout(client):
    settings = get_settings()
    r = client.post(
        "/api/auth/register",
        json={"username": "alice", "password": "password123", "email": "a@example.com"},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["username"] == "alice"
    assert body["email"] == "a@example.com"
    assert body["is_admin"] is True
    assert "password_hash" not in body
    assert settings.COOKIE_NAME in r.cookies
    set_cookie = r.headers.get("set-cookie", "")
    assert "HttpOnly" in set_cookie
    assert "Path=/" in set_cookie
    assert "samesite=lax" in set_cookie.lower()

    me = client.get("/api/auth/me")
    assert me.status_code == 200
    assert me.json()["username"] == "alice"
    assert me.json()["is_admin"] is True

    out = client.post("/api/auth/logout")
    assert out.status_code == 204

    me2 = client.get("/api/auth/me")
    assert me2.status_code == 401

    bad = client.post("/api/auth/login", json={"username": "alice", "password": "wrongpass"})
    assert bad.status_code == 401
    assert bad.json()["detail"] == "用户名或密码错误"

    ok = client.post("/api/auth/login", json={"username": "alice", "password": "password123"})
    assert ok.status_code == 200
    assert ok.json()["username"] == "alice"
    assert client.get("/api/auth/me").status_code == 200


def test_first_user_is_admin_second_is_not(client):
    a = client.post("/api/auth/register", json={"username": "alice", "password": "password123"})
    b = client.post("/api/auth/register", json={"username": "bob", "password": "password123"})
    assert a.status_code == 201 and a.json()["is_admin"] is True
    assert b.status_code == 201 and b.json()["is_admin"] is False
    me = client.get("/api/auth/me")
    assert me.json()["username"] == "bob"
    assert me.json()["is_admin"] is False


def test_duplicate_username_409(client):
    client.post("/api/auth/register", json={"username": "alice", "password": "password123"})
    r = client.post("/api/auth/register", json={"username": "alice", "password": "password123"})
    assert r.status_code == 409


def test_register_validation(client):
    short_name = client.post("/api/auth/register", json={"username": "ab", "password": "password123"})
    assert short_name.status_code in (400, 422)
    bad_name = client.post(
        "/api/auth/register", json={"username": "alice!", "password": "password123"}
    )
    assert bad_name.status_code in (400, 422)
    short_pw = client.post("/api/auth/register", json={"username": "alice", "password": "short"})
    assert short_pw.status_code == 422


def test_protected_requires_login(client):
    assert client.get("/api/problems").status_code == 401
    assert client.get("/api/jobs").status_code == 401
    assert client.get("/api/links").status_code == 401


def test_user_out_excludes_password():
    assert "password_hash" not in UserOut.model_fields
