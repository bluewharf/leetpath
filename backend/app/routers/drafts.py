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


class DraftPut(BaseModel):
    language: Literal["python3", "cpp"]
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
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> DraftOut:
    problem = _published_problem(db, slug)
    draft = db.get(Draft, (user.id, problem.id, language))
    if draft is None:
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
    now = utcnow()
    draft = db.get(Draft, (user.id, problem.id, body.language))
    if draft is None:
        draft = Draft(
            user_id=user.id,
            problem_id=problem.id,
            language=body.language,
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
