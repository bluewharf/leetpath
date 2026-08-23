def test_links(admin_client):
    r = admin_client.get("/api/links")
    assert r.status_code == 200
    items = r.json()
    assert items
    categories = {x["category"] for x in items}
    assert categories == {
        "图解网络",
        "操作系统",
        "MySQL",
        "Redis",
        "算法",
        "面试",
        "大模型面试",
    }
    for item in items:
        assert "title" in item and "url" in item
        assert item["url"].startswith("https://xiaolincoding.com")
    assert any(x["category"] == "大模型面试" for x in items)
