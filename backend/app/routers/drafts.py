from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, field_validator
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Draft, Problem, User, utcnow

router = APIRouter(prefix="/drafts", tags=["drafts"])

CODE_MAX_BYTES = 64 * 1024

PYTHON3_TEMPLATE = (
    "import sys\n"
    "\n"
    "\n"
    "def main():\n"
    "    data = sys.stdin.read().split()\n"
    "    # TODO: 解析输入并求解\n"
    "    ...\n"
    "\n"
    "\n"
    'if __name__ == "__main__":\n'
    "    main()\n"
)

CPP_TEMPLATE = (
    "#include <bits/stdc++.h>\n"
    "using namespace std;\n"
    "\n"
    "int main() {\n"
    "    ios::sync_with_stdio(false);\n"
    "    cin.tie(nullptr);\n"
    "    // TODO\n"
    "    return 0;\n"
    "}\n"
)

TEMPLATES = {"python3": PYTHON3_TEMPLATE, "cpp": CPP_TEMPLATE}


class DraftOut(BaseModel):
    code: str
    updated_at: datetime | None
    is_default: bool


def _storage_language(language: str, io_mode: str) -> str:
    if io_mode == "leetcode":
        return f"{language}_lc"
    return language


class DraftPut(BaseModel):
    language: Literal["python3", "cpp"]
    io_mode: Literal["acm", "leetcode"] = "acm"
    code: str

    @field_validator("code")
    @classmethod
    def code_size(cls, v: str) -> str:
        if len(v.encode("utf-8")) > CODE_MAX_BYTES:
            raise ValueError("代码长度超过 64KB")
        return v


class DraftUpdated(BaseModel):
    updated_at: datetime


def _published_problem(db: Session, slug: str) -> Problem:
    problem = db.scalar(
        select(Problem).where(Problem.slug == slug, Problem.is_published.is_(True))
    )
    if problem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="题目不存在")
    return problem


@router.get("/{slug}")
def get_draft(
    slug: str,
    language: Literal["python3", "cpp"] = Query(default="python3"),
    io_mode: Literal["acm", "leetcode"] = Query(default="acm"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> DraftOut:
    problem = _published_problem(db, slug)
    stored = _storage_language(language, io_mode)
    draft = db.get(Draft, (user.id, problem.id, stored))
    if draft is None:
        if io_mode == "leetcode":
            from judge.leetcode_catalog import spec_for_problem
            from judge.leetcode_wrap import generate_starter

            spec = spec_for_problem(problem)
            if spec is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="本题暂不支持力扣函数模式",
                )
            return DraftOut(
                code=generate_starter(spec, language),
                updated_at=None,
                is_default=True,
            )
        return DraftOut(code=TEMPLATES[language], updated_at=None, is_default=True)
    return DraftOut(code=draft.code, updated_at=draft.updated_at, is_default=False)


@router.put("/{slug}")
def put_draft(
    slug: str,
    body: DraftPut,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> DraftUpdated:
    problem = _published_problem(db, slug)
    if body.io_mode == "leetcode":
        from judge.leetcode_catalog import spec_for_problem

        if spec_for_problem(problem) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="本题暂不支持力扣函数模式",
            )
    now = utcnow()
    stored = _storage_language(body.language, body.io_mode)
    draft = db.get(Draft, (user.id, problem.id, stored))
    if draft is None:
        draft = Draft(
            user_id=user.id,
            problem_id=problem.id,
            language=stored,
            code=body.code,
            updated_at=now,
        )
        db.add(draft)
    else:
        draft.code = body.code
        draft.updated_at = now
    db.commit()
    db.refresh(draft)
    return DraftUpdated(updated_at=draft.updated_at)
