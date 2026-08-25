from app.models import QuizQuestion


def test_quiz_crud_and_practice(admin_client):
    from app import db as dbmod

    with dbmod.SessionLocal() as db:
        db.add(
            QuizQuestion(
                bank="AI Agent 核心概念与架构",
                category="AI Agent 与智能体",
                type="single",
                ordinal=1,
                stem="AI Agent 的大脑通常指什么？",
                options={"A": "数据库", "B": "大语言模型（LLM）", "C": "操作系统", "D": "向量库"},
                answer="B",
                analysis="【正确项】B 正确: LLM 为决策大脑。",
            )
        )
        db.add(
            QuizQuestion(
                bank="AI Agent 核心概念与架构",
                category="AI Agent 与智能体",
                type="judge",
                ordinal=2,
                stem="Chatbot 本质上就是 AI Agent。",
                options={"A": "正确", "B": "错误"},
                answer="错误",
                analysis="【正确项】错误: Chatbot 无自主规划和工具调用。",
            )
        )
        db.commit()

    # 1. 获取 banks 列表
    r = admin_client.get("/api/quiz/banks")
    assert r.status_code == 200
    banks = r.json()
    assert len(banks) == 1
    assert banks[0]["bank"] == "AI Agent 核心概念与架构"
    assert banks[0]["total"] == 2
    assert banks[0]["answered"] == 0

    # 2. 获取题目列表
    r = admin_client.get("/api/quiz/questions?bank=AI Agent 核心概念与架构")
    assert r.status_code == 200
    res = r.json()
    assert res["total"] == 2
    items = res["items"]
    q1_id = items[0]["id"]
    q2_id = items[1]["id"]
    assert items[0]["is_answered"] is False
    assert items[0]["answer"] is None  # 答案未作答时不暴露

    # 3. 作答第一题（回答正确）
    ans_r = admin_client.post(
        f"/api/quiz/questions/{q1_id}/answer", json={"user_answer": "B"}
    )
    assert ans_r.status_code == 200
    ans_body = ans_r.json()
    assert ans_body["is_correct"] is True
    assert ans_body["correct_answer"] == "B"
    assert "LLM 为决策大脑" in ans_body["analysis"]

    # 4. 作答第二题（回答错误）
    ans_r2 = admin_client.post(
        f"/api/quiz/questions/{q2_id}/answer", json={"user_answer": "正确"}
    )
    assert ans_r2.status_code == 200
    assert ans_r2.json()["is_correct"] is False
    assert ans_r2.json()["wrong_count"] == 1

    # 5. 查看错题本筛选
    wrong_r = admin_client.get("/api/quiz/questions?status=wrong")
    assert wrong_r.status_code == 200
    wrong_items = wrong_r.json()["items"]
    assert len(wrong_items) == 1
    assert wrong_items[0]["id"] == q2_id

    # 6. 斩题（从错题本消除）
    slash_r = admin_client.post(f"/api/quiz/questions/{q2_id}/slash", json={"slashed": True})
    assert slash_r.status_code == 200
    assert slash_r.json()["is_slashed"] is True

    # 斩题后再查错题本，应该为空
    wrong_r2 = admin_client.get("/api/quiz/questions?status=wrong")
    assert len(wrong_r2.json()["items"]) == 0

    # 7. 收藏功能
    fav_r = admin_client.post(f"/api/quiz/questions/{q1_id}/favorite")
    assert fav_r.status_code == 200
    assert fav_r.json()["is_favorite"] is True

    fav_list = admin_client.get("/api/quiz/questions?status=favorited")
    assert len(fav_list.json()["items"]) == 1

    # 8. 统计数据
    stats_r = admin_client.get("/api/quiz/stats")
    assert stats_r.status_code == 200
    stats = stats_r.json()
    assert stats["total_questions"] == 2
    assert stats["answered_count"] == 2
    assert stats["correct_count"] == 1
    assert stats["accuracy_rate"] == 50.0
    assert stats["favorite_count"] == 1


def test_quiz_seed_includes_agent_harness_bank():
    from pathlib import Path
    import json

    path = Path(__file__).resolve().parents[1] / "app" / "seed" / "quiz_questions.json"
    questions = json.loads(path.read_text(encoding="utf-8"))
    harness = [q for q in questions if q["bank"] == "Agent Harness 与编码智能体"]
    assert len(harness) >= 20
    assert all(q["category"] == "AI Agent 与智能体" for q in harness)
    stems = " ".join(q["stem"] + q["analysis"] for q in harness)
    for kw in ("Harness", "MCP", "CLAUDE.md", "Skill", "compaction"):
        assert kw in stems
    answers = {q["answer"] for q in harness}
    assert "B" in answers
