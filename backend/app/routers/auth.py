import re

from fastapi import APIRouter, Depends, File, HTTPException, Request, Response, UploadFile, status
from fastapi.responses import FileResponse
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
from app.avatars import (
    MAX_UPLOAD_BYTES,
    absolute_avatar_path,
    avatar_url,
    delete_avatar_file,
    save_avatar,
)
from app.db import get_db
from app.deps import get_current_user
from app.invites import hash_invite_code
from app.models import Invite, User, utcnow
from app.rate_limit import client_ip, request_limiter

_DUMMY_PASSWORD_HASH = hash_password("timing-equalizer-dummy")

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
    avatar_url: str | None = None


class PasswordChangeIn(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_password_bytes(cls, password: str) -> str:
        if len(password.encode("utf-8")) > 72:
            raise ValueError("密码不能超过 72 字节")
        return password


def user_out(user: User) -> UserOut:
    return UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        is_admin=user.is_admin,
        avatar_url=avatar_url(user),
    )


def _issue_session(response: Response, user: User) -> None:
    set_auth_cookie(response, create_access_token(user.id, int(user.token_version or 0)))


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
    _issue_session(response, user)
    return user_out(user)


@router.post("/login")
def login(
    body: LoginIn,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> UserOut:
    request_limiter.check(f"login-ip:{client_ip(request)}", limit=20, window_seconds=60)
    request_limiter.check(
        f"login:{client_ip(request)}:{body.username}",
        limit=5,
        window_seconds=60,
    )
    user = db.scalar(select(User).where(User.username == body.username))
    if user is None:
        verify_password(body.password, _DUMMY_PASSWORD_HASH)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    if not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    _issue_session(response, user)
    return user_out(user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response) -> None:
    clear_auth_cookie(response)


@router.get("/me")
def me(user: User = Depends(get_current_user)) -> UserOut:
    return user_out(user)


@router.post("/password")
def change_password(
    body: PasswordChangeIn,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UserOut:
    request_limiter.check(f"password:{user.id}", limit=5, window_seconds=900)
    if body.new_password == body.old_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="新密码不能与当前密码相同")
    if not verify_password(body.old_password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="当前密码不正确")
    user.password_hash = hash_password(body.new_password)
    user.token_version = int(user.token_version or 0) + 1
    db.commit()
    db.refresh(user)
    _issue_session(response, user)
    return user_out(user)


@router.post("/avatar")
async def upload_avatar(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    file: UploadFile = File(...),
) -> UserOut:
    request_limiter.check(f"avatar:{user.id}", limit=10, window_seconds=3600)
    content_type = (file.content_type or "").lower()
    if content_type not in {"image/jpeg", "image/png", "image/webp", "image/gif"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="只支持 JPG / PNG / WebP / GIF")
    data = await file.read()
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="图片不能超过 1.5MB")
    try:
        relative = save_avatar(user.id, data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    user.avatar_path = relative
    user.avatar_updated_at = utcnow()
    db.commit()
    db.refresh(user)
    return user_out(user)


@router.delete("/avatar")
def remove_avatar(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UserOut:
    delete_avatar_file(user.avatar_path)
    user.avatar_path = None
    user.avatar_updated_at = utcnow()
    db.commit()
    db.refresh(user)
    return user_out(user)


@router.get("/avatar/{user_id}")
def get_avatar(
    user_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> FileResponse:
    target = db.get(User, user_id)
    if target is None or not target.avatar_path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未设置头像")
    path = absolute_avatar_path(target.avatar_path)
    if not path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未设置头像")
    return FileResponse(
        path,
        media_type="image/webp",
        headers={"Cache-Control": "private, max-age=3600"},
    )
