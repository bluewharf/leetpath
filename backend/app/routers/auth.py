import re

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
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
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

USERNAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,32}$")


class RegisterIn(BaseModel):
    username: str
    password: str = Field(min_length=8)
    email: str | None = None


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
def register(body: RegisterIn, response: Response, db: Session = Depends(get_db)) -> UserOut:
    if not USERNAME_RE.fullmatch(body.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名须为 3-32 位字母、数字或下划线",
        )
    exists = db.scalar(select(User.id).where(User.username == body.username))
    if exists is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="用户名已存在")
    is_first = db.scalar(select(func.count()).select_from(User)) == 0
    email = body.email.strip() if body.email else None
    if email == "":
        email = None
    user = User(
        username=body.username,
        email=email,
        password_hash=hash_password(body.password),
        is_admin=bool(is_first),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    set_auth_cookie(response, create_access_token(user.id))
    return user_out(user)


@router.post("/login")
def login(body: LoginIn, response: Response, db: Session = Depends(get_db)) -> UserOut:
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
