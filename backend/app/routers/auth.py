import re

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.auth import (
    clear_auth_cookie,
    create_access_token,
    hash_password,
    set_auth_cookie,
    verify_password,
)
from app.db import get_db
from app.deps import get_current_user
from app.invites import hash_invite_code
from app.models import Invite, User, utcnow
from app.rate_limit import client_ip, request_limiter

router = APIRouter(prefix="/auth", tags=["auth"])

USERNAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,32}$")


class RegisterIn(BaseModel):
    username: str
    password: str = Field(min_length=8)
    email: str | None = None
    invite_code: str

    @field_validator("password")
    @classmethod
    def validate_password_bytes(cls, password: str) -> str:
        if len(password.encode("utf-8")) > 72:
            raise ValueError("密码不能超过 72 字节")
        return password

class LoginIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str | None
    is_admin: bool


def user_out(user: User) -> UserOut:
    return UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        is_admin=user.is_admin,
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    body: RegisterIn,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> UserOut:
    request_limiter.check(f"register:{client_ip(request)}", limit=5, window_seconds=3600)
    if not USERNAME_RE.fullmatch(body.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名须为 3-32 位字母、数字或下划线",
        )
    exists = db.scalar(select(User.id).where(User.username == body.username))
    if exists is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="用户名已存在")
    email = body.email.strip() if body.email else None
    if email == "":
        email = None
    user = User(
        username=body.username,
        email=email,
        password_hash=hash_password(body.password),
        is_admin=False,
    )
    db.add(user)
    db.flush()
    now = utcnow()
    claimed = db.execute(
        update(Invite)
        .where(
            Invite.code_hash == hash_invite_code(body.invite_code),
            Invite.used_at.is_(None),
            Invite.revoked_at.is_(None),
            Invite.expires_at > now,
        )
        .values(used_at=now, used_by_id=user.id)
    )
    if claimed.rowcount != 1:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="注册邀请码无效或已失效",
        )
    db.commit()
    db.refresh(user)
    set_auth_cookie(response, create_access_token(user.id))
    return user_out(user)


@router.post("/login")
def login(
    body: LoginIn,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> UserOut:
    request_limiter.check(
        f"login:{client_ip(request)}:{body.username}",
        limit=5,
        window_seconds=60,
    )
    user = db.scalar(select(User).where(User.username == body.username))
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    set_auth_cookie(response, create_access_token(user.id))
    return user_out(user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response) -> None:
    clear_auth_cookie(response)


@router.get("/me")
def me(user: User = Depends(get_current_user)) -> UserOut:
    return user_out(user)
