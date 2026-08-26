from app.routers.drafts import CPP_TEMPLATE, PYTHON3_TEMPLATE


def test_default_templates(admin_client):
    py = admin_client.get("/api/drafts/two-sum?language=python3")
    assert py.status_code == 200
    assert py.json()["is_default"] is True
    assert py.json()["code"] == PYTHON3_TEMPLATE
    assert py.json()["updated_at"] is None

    cpp = admin_client.get("/api/drafts/two-sum?language=cpp")
    assert cpp.status_code == 200
    assert cpp.json()["is_default"] is True
    assert cpp.json()["code"] == CPP_TEMPLATE


def test_draft_default_language_is_python3(admin_client):
    r = admin_client.get("/api/drafts/two-sum")
    assert r.status_code == 200
    assert r.json()["code"] == PYTHON3_TEMPLATE


def test_put_and_get_draft(admin_client):
    put = admin_client.put(
        "/api/drafts/two-sum",
        json={"language": "python3", "code": "print(42)\n"},
    )
    assert put.status_code == 200
    assert "updated_at" in put.json()

    got = admin_client.get("/api/drafts/two-sum?language=python3")
    assert got.json()["is_default"] is False
    assert got.json()["code"] == "print(42)\n"
    assert got.json()["updated_at"] is not None


def test_draft_unknown_problem(admin_client):
    assert admin_client.get("/api/drafts/no-such").status_code == 404


def test_draft_code_too_large(admin_client):
    huge = "x" * (64 * 1024 + 1)
    r = admin_client.put("/api/drafts/two-sum", json={"language": "python3", "code": huge})
    assert r.status_code == 422


def test_leetcode_default_starter_and_isolated_from_acm(admin_client):
    lc = admin_client.get("/api/drafts/two-sum?language=python3&io_mode=leetcode")
    assert lc.status_code == 200
    body = lc.json()
    assert body["is_default"] is True
    assert "class Solution:" in body["code"]
    assert "def twoSum" in body["code"]
    assert "stdin" not in body["code"]

    admin_client.put(
        "/api/drafts/two-sum",
        json={"language": "python3", "io_mode": "leetcode", "code": "class Solution:\n    pass\n"},
    )
    acm = admin_client.get("/api/drafts/two-sum?language=python3")
    assert acm.json()["is_default"] is True
    assert acm.json()["code"] == PYTHON3_TEMPLATE
    saved = admin_client.get("/api/drafts/two-sum?language=python3&io_mode=leetcode")
    assert saved.json()["is_default"] is False
    assert saved.json()["code"] == "class Solution:\n    pass\n"
