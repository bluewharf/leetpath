from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_admin
from app.models import Problem, User
from app.seed.loader import load_problems
from app.seed.quiz_loader import load_quiz_questions

router = APIRouter(prefix="/admin", tags=["admin"])


class SeedReloadOut(BaseModel):
    imported: int
    quiz_imported: int = 0


class PublishIn(BaseModel):
    is_published: bool


class AdminProblemOut(BaseModel):
    id: int
    slug: str
    leetcode_id: int | None
    title: str
    difficulty: str
    source: str
    tags: list[str]
    time_limit_ms: int
    memory_limit_mb: int
    is_published: bool
    created_at: datetime


@router.post("/seed/reload")
def reload_seed(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> SeedReloadOut:
    imported = load_problems(session=db)
    quiz_imported = load_quiz_questions(session=db)
    db.commit()
    return SeedReloadOut(imported=imported, quiz_imported=quiz_imported)


@router.get("/problems")
def list_all_problems(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> list[AdminProblemOut]:
    problems = list(db.scalars(select(Problem).order_by(Problem.id)).all())
    return [
        AdminProblemOut(
            id=p.id,
            slug=p.slug,
            leetcode_id=p.leetcode_id,
            title=p.title,
            difficulty=p.difficulty,
            source=p.source,
            tags=p.tags or [],
            time_limit_ms=p.time_limit_ms,
            memory_limit_mb=p.memory_limit_mb,
            is_published=p.is_published,
            created_at=p.created_at,
        )
        for p in problems
    ]


@router.put("/problems/{problem_id}")
def set_published(
    problem_id: int,
    body: PublishIn,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> AdminProblemOut:
    problem = db.get(Problem, problem_id)
    if problem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="题目不存在")
    problem.is_published = body.is_published
    db.commit()
    db.refresh(problem)
    return AdminProblemOut(
        id=problem.id,
        slug=problem.slug,
        leetcode_id=problem.leetcode_id,
        title=problem.title,
        difficulty=problem.difficulty,
        source=problem.source,
        tags=problem.tags or [],
        time_limit_ms=problem.time_limit_ms,
        memory_limit_mb=problem.memory_limit_mb,
        is_published=problem.is_published,
        created_at=problem.created_at,
    )


class SystemAiConfigIn(BaseModel):
    api_key: str = ""
    base_url: str = "https://api.antithor.asia/v1"
    model: str = "grok-4.6-xhigh"


class SystemAiConfigOut(BaseModel):
    has_key: bool
    masked_key: str
    base_url: str
    model: str
    updated_at: datetime | None = None


@router.get("/ai-config")
def get_system_ai_config(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> SystemAiConfigOut:
    from app.config import get_settings
    from app.models import SystemSetting
    settings = get_settings()

    k_rec = db.get(SystemSetting, "ai_api_key")
    u_rec = db.get(SystemSetting, "ai_base_url")
    m_rec = db.get(SystemSetting, "ai_model")

    raw_key = (k_rec.value if k_rec else "") or settings.SYSTEM_AI_API_KEY
    raw_url = (u_rec.value if u_rec else "") or settings.SYSTEM_AI_BASE_URL
    raw_model = (m_rec.value if m_rec else "") or settings.SYSTEM_AI_MODEL

    masked = f"{raw_key[:3]}****{raw_key[-4:]}" if len(raw_key) > 8 else ("已配置" if raw_key else "未配置")

    return SystemAiConfigOut(
        has_key=bool(raw_key.strip()),
        masked_key=masked,
        base_url=raw_url,
        model=raw_model,
        updated_at=k_rec.updated_at if k_rec else None,
    )


@router.put("/ai-config")
def update_system_ai_config(
    body: SystemAiConfigIn,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> SystemAiConfigOut:
    from app.models import SystemSetting, utcnow

    k_rec = db.get(SystemSetting, "ai_api_key")
    if body.api_key.strip():
        if not k_rec:
            k_rec = SystemSetting(key="ai_api_key", value=body.api_key.strip(), description="系统内置共享 AI API Key")
            db.add(k_rec)
        else:
            k_rec.value = body.api_key.strip()
            k_rec.updated_at = utcnow()

    u_rec = db.get(SystemSetting, "ai_base_url")
    url_val = body.base_url.strip() or "https://api.antithor.asia/v1"
    if not u_rec:
        u_rec = SystemSetting(key="ai_base_url", value=url_val, description="系统内置 Base URL")
        db.add(u_rec)
    else:
        u_rec.value = url_val

    m_rec = db.get(SystemSetting, "ai_model")
    model_val = body.model.strip() or "grok-4.6-xhigh"
    if not m_rec:
        m_rec = SystemSetting(key="ai_model", value=model_val, description="系统内置默认模型")
        db.add(m_rec)
    else:
        m_rec.value = model_val

    db.commit()
    return get_system_ai_config(db=db, _admin=_admin)
