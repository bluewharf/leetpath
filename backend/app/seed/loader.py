from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import Problem, Testcase

DEFAULT_PROBLEMS_DIR = Path(__file__).resolve().parent / "problems"


def _parse_tests(tests_dir: Path, sample_ordinals: set[int]) -> list[dict]:
    if not tests_dir.is_dir():
        return []
    cases: list[dict] = []
    for inp in sorted(tests_dir.glob("*.in")):
        if not inp.stem.isdigit():
            continue
        outp = inp.with_suffix(".out")
        if not outp.exists():
            continue
        ordinal = int(inp.stem)
        cases.append(
            {
                "ordinal": ordinal,
                "input": inp.read_text(encoding="utf-8"),
                "expected_output": outp.read_text(encoding="utf-8"),
                "is_sample": ordinal in sample_ordinals,
            }
        )
    return cases


def _upsert_problem(session: Session, directory: Path) -> bool:
    meta_path = directory / "meta.toml"
    statement_path = directory / "statement.md"
    if not meta_path.is_file() or not statement_path.is_file():
        return False
    meta = tomllib.loads(meta_path.read_text(encoding="utf-8"))
    slug = meta.get("slug") or directory.name
    title = meta.get("title")
    if not title:
        return False
    samples = meta.get("samples") or []
    sample_ordinals = {int(x) for x in samples}
    cases = _parse_tests(directory / "tests", sample_ordinals)
    solution_path = directory / "solution.md"
    raw_lc = meta.get("leetcode_id")
    leetcode_id = int(raw_lc) if raw_lc is not None else None
    fields = {
        "slug": slug,
        "leetcode_id": leetcode_id,
        "title": title,
        "difficulty": meta.get("difficulty", "easy"),
        "source": meta.get("source", "hot100"),
        "tags": list(meta.get("tags") or []),
        "statement_md": statement_path.read_text(encoding="utf-8"),
        "solution_md": (
            solution_path.read_text(encoding="utf-8") if solution_path.is_file() else None
        ),
        "time_limit_ms": int(meta.get("time_limit_ms", 5000)),
        "memory_limit_mb": int(meta.get("memory_limit_mb", 256)),
    }
    problem = session.scalar(select(Problem).where(Problem.slug == slug))
    if problem is None:
        problem = Problem(**fields)
        session.add(problem)
        session.flush()
    else:
        for key, value in fields.items():
            setattr(problem, key, value)
        session.execute(delete(Testcase).where(Testcase.problem_id == problem.id))
        session.flush()
    for case in cases:
        session.add(Testcase(problem_id=problem.id, **case))
    return True


def load_problems(
    problems_dir: Path | str | None = None,
    session: Session | None = None,
) -> int:
    """Scan problems_dir and upsert problems. Returns imported count.

    tests 可通过传入目录参数使用 fixtures，默认扫描 app/seed/problems/。
    """
    from app import db as dbmod
    from app.db import Base, configure_db

    directory = Path(problems_dir) if problems_dir is not None else DEFAULT_PROBLEMS_DIR
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
    imported = 0
    try:
        if not directory.is_dir():
            if own_session:
                session.commit()
            return 0
        for child in sorted(directory.iterdir()):
            if not child.is_dir():
                continue
            if _upsert_problem(session, child):
                imported += 1
        if own_session:
            session.commit()
        else:
            session.flush()
        return imported
    except Exception:
        if own_session:
            session.rollback()
        raise
    finally:
        if own_session:
            session.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="导入题库种子")
    parser.add_argument(
        "problems_dir",
        nargs="?",
        default=None,
        help="题目目录（默认 app/seed/problems）",
    )
    args = parser.parse_args(argv)
    n = load_problems(args.problems_dir)
    print(n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
