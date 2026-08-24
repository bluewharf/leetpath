import argparse
import getpass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.db import Base, configure_db
from app.models import User


def create_admin(db: Session, username: str, password: str, email: str | None = None) -> User:
    if not 3 <= len(username) <= 32 or not username.replace("_", "a").isalnum():
        raise ValueError("用户名须为 3-32 位字母、数字或下划线")
    password_bytes = len(password.encode("utf-8"))
    if password_bytes < 8 or password_bytes > 72:
        raise ValueError("密码须为 8-72 字节")
    if db.scalar(select(User.id).where(User.username == username)) is not None:
        raise ValueError("用户名已存在")
    user = User(
        username=username,
        email=email.strip() if email else None,
        password_hash=hash_password(password),
        is_admin=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def main() -> None:
    parser = argparse.ArgumentParser(description="leetpath 管理命令")
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser("create-admin", help="创建管理员账号")
    create.add_argument("username")
    create.add_argument("--email")
    args = parser.parse_args()

    password = getpass.getpass("管理员密码: ")
    password_confirm = getpass.getpass("再次输入密码: ")
    if password != password_confirm:
        raise SystemExit("两次密码不一致")

    engine = configure_db()
    Base.metadata.create_all(bind=engine)
    from app import db as dbmod

    assert dbmod.SessionLocal is not None
    with dbmod.SessionLocal() as db:
        user = create_admin(db, args.username, password, args.email)
    print(f"管理员已创建: {user.username}")


if __name__ == "__main__":
    main()
