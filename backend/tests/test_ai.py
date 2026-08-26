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


def test_chat_upstream_body_forwards_reasoning_effort():
    from app.routers.ai import ChatStreamRequest, chat_upstream_body

    payload = ChatStreamRequest(
        model="grok-4.6",
        messages=[{"role": "user", "content": "hi"}],
        temperature=0.4,
        max_tokens=2048,
        reasoning_effort="high",
    )
    body = chat_upstream_body(payload, "grok-4.6")
    assert body["reasoning_effort"] == "high"
    assert body["temperature"] == 0.4
    assert body["max_tokens"] == 2048
    assert body["max_completion_tokens"] == 2048
    assert body["stream"] is True
    assert body["max_tokens"] + 128 <= 256000

    off = ChatStreamRequest(
        model="grok-4.6",
        messages=[{"role": "user", "content": "hi"}],
        reasoning_effort="off",
    )
    off_body = chat_upstream_body(off, "grok-4.6")
    assert "reasoning_effort" not in off_body
    assert off_body["max_completion_tokens"] == 4096

    huge = ChatStreamRequest(
        model="grok-4.6",
        messages=[{"role": "user", "content": "hi"}],
        max_tokens=256000,
    )
    huge_body = chat_upstream_body(huge, "grok-4.6")
    assert huge_body["max_tokens"] == huge_body["max_completion_tokens"]
    assert huge_body["max_completion_tokens"] < 256000
    assert huge_body["max_completion_tokens"] <= 256000 - 64


def test_chat_rejects_unknown_reasoning_effort(admin_client):
    r = admin_client.post(
        "/api/ai/chat",
        json={
            "base_url": "https://api.antithor.asia/v1",
            "api_key": "sk-test",
            "model": "grok-4.6",
            "messages": [{"role": "user", "content": "hi"}],
            "reasoning_effort": "ultra",
        },
    )
    assert r.status_code == 422


def test_ai_requires_login(client):
    r = client.post(
        "/api/ai/models",
        json={"base_url": "https://api.deepseek.com/v1", "api_key": "sk-test"},
    )
    assert r.status_code == 401
