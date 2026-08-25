def test_links(admin_client):
    r = admin_client.get("/api/links")
    assert r.status_code == 200
    items = r.json()
    assert items
    categories = {x["category"] for x in items}
    assert {
        "图解网络",
        "操作系统",
        "MySQL",
        "Redis",
        "算法",
        "面试",
        "大模型面试",
        "Agent Harness 前沿",
    } <= categories
    for item in items:
        assert "title" in item and "url" in item
        assert item["url"].startswith("https://")
    xiaolin = [x for x in items if x["category"] != "Agent Harness 前沿"]
    for item in xiaolin:
        assert item["url"].startswith("https://xiaolincoding.com")
    harness = [x for x in items if x["category"] == "Agent Harness 前沿"]
    assert len(harness) >= 6
    assert any("modelcontextprotocol.io" in x["url"] for x in harness)
    assert any("code.claude.com" in x["url"] or "openai.com" in x["url"] for x in harness)
