def test_production_rejects_missing_or_untrusted_origin(client, monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("SECRET_KEY", "x" * 48)
    monkeypatch.setenv("COOKIE_SECURE", "true")
    monkeypatch.setenv("PUBLIC_ORIGIN", "https://learn.example.com")

    missing = client.post("/api/auth/login", json={"username": "none", "password": "password123"})
    assert missing.status_code == 403
    untrusted = client.post(
        "/api/auth/login",
        json={"username": "none", "password": "password123"},
        headers={"Origin": "https://evil.example"},
    )
    assert untrusted.status_code == 403
    trusted = client.post(
        "/api/auth/login",
        json={"username": "none", "password": "password123"},
        headers={"Origin": "https://learn.example.com"},
    )
    assert trusted.status_code == 401


def test_login_is_rate_limited(client):
    statuses = [
        client.post(
            "/api/auth/login",
            json={"username": "missing", "password": "password123"},
        ).status_code
        for _ in range(6)
    ]
    assert statuses[:5] == [401] * 5
    assert statuses[5] == 429
    assert client.post(
        "/api/auth/login",
        json={"username": "other", "password": "password123"},
    ).status_code == 401
