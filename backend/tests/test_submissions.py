def test_create_submission_pending(admin_client):
    r = admin_client.post(
        "/api/submissions",
        json={"problem_slug": "two-sum", "language": "python3", "code": "print(0, 1)\n"},
    )
    assert r.status_code == 202
    body = r.json()
    assert body["status"] == "pending"
    assert "id" in body

    detail = admin_client.get(f"/api/submissions/{body['id']}")
    assert detail.status_code == 200
    d = detail.json()
    assert d["problem_slug"] == "two-sum"
    assert d["problem_title"] == "两数之和"
    assert d["language"] == "python3"
    assert d["code"] == "print(0, 1)\n"
    assert d["status"] == "pending"
    assert d["runtime_ms"] is None
    assert d["compile_output"] is None
    assert d["detail"] is None
    assert "created_at" in d


def test_list_submissions_omits_code(admin_client):
    admin_client.post(
        "/api/submissions",
        json={"problem_slug": "two-sum", "language": "cpp", "code": "int main(){}"},
    )
    listed = admin_client.get("/api/submissions?problem_slug=two-sum&limit=50")
    assert listed.status_code == 200
    items = listed.json()
    assert len(items) >= 1
    assert "code" not in items[0]
    assert items[0]["problem_slug"] == "two-sum"
    assert items[0]["status"] == "pending"


def test_submission_rate_limit(admin_client):
    payload = {"problem_slug": "two-sum", "language": "python3", "code": "print(1)"}
    codes = []
    for _ in range(6):
        codes.append(admin_client.post("/api/submissions", json=payload).status_code)
    assert codes[:5] == [202] * 5
    assert codes[5] == 429


def test_submission_other_user_forbidden(admin_client):
    created = admin_client.post(
        "/api/submissions",
        json={"problem_slug": "two-sum", "language": "python3", "code": "print(1)"},
    )
    sid = created.json()["id"]
    admin_client.post("/api/auth/register", json={"username": "bob", "password": "password123"})
    r = admin_client.get(f"/api/submissions/{sid}")
    assert r.status_code == 403


def test_submission_unknown_problem(admin_client):
    r = admin_client.post(
        "/api/submissions",
        json={"problem_slug": "no-such", "language": "python3", "code": "print(1)"},
    )
    assert r.status_code == 404


def test_submission_invalid_language(admin_client):
    r = admin_client.post(
        "/api/submissions",
        json={"problem_slug": "two-sum", "language": "java", "code": "print(1)"},
    )
    assert r.status_code == 422
