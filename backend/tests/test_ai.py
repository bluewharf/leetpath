def test_ai_rejects_host_not_in_allowlist(admin_client):
    """白名单外的目标（含内网地址）应被拒绝，防止 SSRF"""
    r = admin_client.post(
        "/api/ai/models",
        json={"base_url": "http://backend:8000/v1", "api_key": "sk-test"},
    )
    assert r.status_code == 400
    assert "允许列表" in r.json()["detail"]

    r2 = admin_client.post(
        "/api/ai/chat",
        json={
            "base_url": "http://169.254.169.254/v1",
            "api_key": "sk-test",
            "model": "m",
            "messages": [{"role": "user", "content": "hi"}],
        },
    )
    assert r2.status_code == 400


def test_ai_rejects_non_http_scheme(admin_client):
    r = admin_client.post(
        "/api/ai/models",
        json={"base_url": "file:///etc/passwd", "api_key": "sk-test"},
    )
    assert r.status_code == 400


def test_ai_requires_login(client):
    r = client.post(
        "/api/ai/models",
        json={"base_url": "https://api.deepseek.com/v1", "api_key": "sk-test"},
    )
    assert r.status_code == 401
