from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import QuizQuestion

DEFAULT_JSON_PATH = Path(__file__).resolve().parent / "quiz_questions.json"


def assign_category(bank: str) -> str:
    """根据专题名称归类到一级大分类"""
    if "杀手" in bank:
        return "反直觉杀手题"
    if "强化学习" in bank:
        return "强化学习"
    if "Agent" in bank or "智能体" in bank or "Harness" in bank:
        return "AI Agent 与智能体"
    if "RAG" in bank or "向量" in bank or "Embedding" in bank or "检索" in bank or "幻觉" in bank:
        return "RAG 与知识检索"
    if "微调" in bank or "训练" in bank or "部署" in bank or "优化" in bank or "评估" in bank or "数据工程" in bank:
        return "大模型训练与工程"
    if "Transformer" in bank or "LLM" in bank or "大模型" in bank or "Prompt" in bank or "长文本" in bank or "思维链" in bank:
        return "大模型与 Transformer"
    if "算法" in bank or "数学" in bank or "数据结构" in bank or "机考" in bank:
        return "算法与机考"
    if "半导体" in bank or "多模态" in bank or "工业" in bank:
        return "多模态与工业场景"
    return "综合理论"


def parse_quiz_txt(file_path: Path) -> list[dict]:
    """从纯文本题库文件中结构化解析题目"""
    if not file_path.is_file():
        return []

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    i = 0
    current_topic = ""
    current_type_str = ""
    questions: list[dict] = []

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("# "):
            current_topic = line[2:].strip()
            i += 1
            continue
        if any(line.startswith(prefix) for prefix in ["一、", "二、", "三、", "四、", "五、"]):
            current_type_str = line
            i += 1
            continue

        m = re.match(r"^(\d+)\.\s*(.+)$", line)
        if m:
            ordinal = int(m.group(1))
            stem = m.group(2)
            i += 1
            options: dict[str, str] = {}
            analysis: list[str] = []
            answer = ""

            # 读取题干后续行
            while i < len(lines):
                l = lines[i].strip()
                if (
                    re.match(r"^[A-D]\.", l)
                    or re.match(r"^(?:正确)?答案[：:]", l)
                    or l.startswith("【答案】")
                    or l.startswith("# ")
                    or any(l.startswith(p) for p in ["一、", "二、", "三、", "四、"])
                    or re.match(r"^\d+\.", l)
                ):
                    break
                if l:
                    stem += "\n" + l
                i += 1

            # 读取 A/B/C/D 选项
            while i < len(lines) and re.match(r"^[A-D]\.", lines[i].strip()):
                opt_line = lines[i].strip()
                opt_key = opt_line[0]
                opt_val = opt_line[2:].strip()
                options[opt_key] = opt_val
                i += 1

            # 读取答案
            while i < len(lines):
                l = lines[i].strip()
                ans_m = re.match(r"^(?:正确)?答案[：:]\s*(.+)$", l) or re.match(r"^【答案】\s*(.+)$", l)
                if ans_m:
                    answer = ans_m.group(1).strip()
                    i += 1
                    break
                elif l.startswith("# ") or any(l.startswith(p) for p in ["一、", "二、", "三、"]) or re.match(r"^\d+\.", l):
                    break
                i += 1

            # 读取解析
            if i < len(lines) and (re.match(r"^解析[：:]", lines[i].strip()) or lines[i].strip().startswith("【解析】")):
                i += 1
                while i < len(lines):
                    cur_line = lines[i].strip()
                    if (
                        cur_line.startswith("# ")
                        or any(cur_line.startswith(p) for p in ["一、", "二、", "三、"])
                        or re.match(r"^\d+\.", cur_line)
                    ):
                        break
                    analysis.append(lines[i])
                    i += 1

            # 判断题型
            q_type = "single"
            if "多选" in current_type_str:
                q_type = "multiple"
            elif "判断" in current_type_str or answer in ["正确", "错误"] or (not options and ("正确" in answer or "错误" in answer)):
                q_type = "judge"
                if not options:
                    options = {"A": "正确", "B": "错误"}
            elif len(answer) > 1 and all(c in "ABCD" for c in answer):
                q_type = "multiple"

            if q_type == "judge":
                if "正确" in answer or answer in ("A", "对", "T", "True"):
                    answer = "正确"
                elif "错误" in answer or answer in ("B", "错", "F", "False"):
                    answer = "错误"

            questions.append(
                {
                    "bank": current_topic,
                    "category": assign_category(current_topic),
                    "ordinal": ordinal,
                    "type": q_type,
                    "stem": stem.strip(),
                    "options": options,
                    "answer": answer,
                    "analysis": "\n".join(analysis).strip(),
                }
            )
        else:
            i += 1

    return questions


def export_quiz_json(txt_path: Path, json_path: Path = DEFAULT_JSON_PATH) -> int:
    """将 txt 题库解析并保存为 json"""
    questions = parse_quiz_txt(txt_path)
    if not questions:
        return 0
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(questions)


def load_quiz_questions(
    source_path: Path | str | None = None,
    session: Session | None = None,
) -> int:
    """导入/更新客观题题库"""
    from app import db as dbmod
    from app.db import Base, configure_db

    path = Path(source_path) if source_path is not None else None
    if path is None and DEFAULT_JSON_PATH.is_file():
        path = DEFAULT_JSON_PATH

    if path is None or not path.is_file():
        return 0

    if path.suffix == ".json":
        raw = json.loads(path.read_text(encoding="utf-8"))
        questions = raw
    else:
        questions = parse_quiz_txt(path)

    if not questions:
        return 0

    own_session = session is None
    if own_session:
        if dbmod.SessionLocal is None:
            configure_db()
            from app import models as _models  # noqa: F401

            assert dbmod.engine is not None
            Base.metadata.create_all(bind=dbmod.engine)
            dbmod.ensure_schema(dbmod.engine)
        assert dbmod.SessionLocal is not None
        session = dbmod.SessionLocal()

    assert session is not None
    try:
        existing = {
            (q.bank, q.ordinal): q for q in session.scalars(select(QuizQuestion)).all()
        }

        imported_count = 0
        for item in questions:
            key = (item["bank"], item["ordinal"])
            q_obj = existing.get(key)
            if q_obj is None:
                q_obj = QuizQuestion(
                    bank=item["bank"],
                    category=item.get("category") or assign_category(item["bank"]),
                    ordinal=item["ordinal"],
                    type=item["type"],
                    stem=item["stem"],
                    options=item["options"],
                    answer=item["answer"],
                    analysis=item["analysis"],
                )
                session.add(q_obj)
            else:
                q_obj.category = item.get("category") or assign_category(item["bank"])
                q_obj.type = item["type"]
                q_obj.stem = item["stem"]
                q_obj.options = item["options"]
                q_obj.answer = item["answer"]
                q_obj.analysis = item["analysis"]
            imported_count += 1

        if own_session:
            session.commit()
        else:
            session.flush()

        return imported_count
    except Exception:
        if own_session:
            session.rollback()
        raise
    finally:
        if own_session:
            session.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="导入客观题题库")
    parser.add_argument(
        "source",
        nargs="?",
        default=None,
        help="题库源文件路径（.json 或 .txt，默认自动探测）",
    )
    parser.add_argument(
        "--export-json",
        action="store_true",
        help="从 txt 导出为 json 题库",
    )
    args = parser.parse_args(argv)
    if args.export_json:
        if not args.source:
            parser.error("--export-json 需要提供 txt 源文件路径")
        n = export_quiz_json(Path(args.source), DEFAULT_JSON_PATH)
        print(f"已导出 {n} 道题到 {DEFAULT_JSON_PATH}")
        return 0

    n = load_quiz_questions(args.source)
    print(f"已导入 {n} 道客观题")
    return 0


if __name__ == "__main__":
    sys.exit(main())
