import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_admin
from app.invites import hash_invite_code
from app.models import Invite, User, utcnow

router = APIRouter(prefix="/admin/invites", tags=["admin"])


class InviteCreate(BaseModel):
    expires_in_days: int = Field(default=7, ge=1, le=30)


class InviteOut(BaseModel):
    id: int
    expires_at: datetime
    used_at: datetime | None
    revoked_at: datetime | None
    created_at: datetime


class InviteCreated(InviteOut):
    code: str


def invite_out(invite: Invite) -> InviteOut:
    return InviteOut(
        id=invite.id,
        expires_at=invite.expires_at,
        used_at=invite.used_at,
        revoked_at=invite.revoked_at,
        created_at=invite.created_at,
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_invite(
    body: InviteCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> InviteCreated:
    code = secrets.token_urlsafe(24)
    now = utcnow()
    invite = Invite(
        code_hash=hash_invite_code(code),
        expires_at=now + timedelta(days=body.expires_in_days),
        created_by_id=admin.id,
        created_at=now,
    )
    db.add(invite)
    db.commit()
    db.refresh(invite)
    return InviteCreated(code=code, **invite_out(invite).model_dump())


@router.get("")
def list_invites(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> list[InviteOut]:
    invites = db.scalars(select(Invite).order_by(Invite.id.desc())).all()
    return [invite_out(invite) for invite in invites]


@router.delete("/{invite_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_invite(
    invite_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> None:
    invite = db.get(Invite, invite_id)
    if invite is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="邀请码不存在")
    if invite.used_at is None and invite.revoked_at is None:
        invite.revoked_at = utcnow()
        db.commit()
