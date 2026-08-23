from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings

BACKEND_ROOT = Path(__file__).resolve().parent.parent

engine: Engine | None = None
SessionLocal: sessionmaker[Session] | None = None


class Base(DeclarativeBase):
    pass


def resolve_database_url(url: str) -> str:
    if not url.startswith("sqlite:///"):
        return url
    rest = url[len("sqlite:///"):]
    if rest == ":memory:" or rest.startswith(":memory:"):
        return url
    path = Path(rest)
    if not path.is_absolute():
        path = BACKEND_ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return "sqlite:///" + path.resolve().as_posix()


def _sqlite_connect(dbapi_conn, _connection_record) -> None:
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def configure_db(database_url: str | None = None) -> Engine:
    global engine, SessionLocal
    if engine is not None:
        engine.dispose()
        engine = None
        SessionLocal = None

    settings = get_settings()
    url = resolve_database_url(database_url or settings.DATABASE_URL)
    connect_args = {}
    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    engine = create_engine(url, connect_args=connect_args, future=True)
    if url.startswith("sqlite"):
        event.listen(engine, "connect", _sqlite_connect)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return engine


def get_db() -> Generator[Session, None, None]:
    if SessionLocal is None:
        configure_db()
    assert SessionLocal is not None
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
