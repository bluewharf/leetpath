import logging
import os
import sqlite3
import time
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy.engine import make_url


logger = logging.getLogger(__name__)


def backup_once(
    source: Path,
    backup_dir: Path,
    *,
    retention: int = 7,
    now: datetime | None = None,
) -> Path:
    if retention < 1:
        raise ValueError("retention must be at least 1")

    source = Path(source)
    if not source.is_file():
        raise FileNotFoundError(source)

    backup_dir = Path(backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    destination = backup_dir / f"leetpath-{timestamp:%Y%m%d-%H%M%S}.db"
    temporary = destination.with_suffix(".db.part")

    try:
        source_uri = f"{source.resolve().as_uri()}?mode=ro"
        with closing(sqlite3.connect(source_uri, uri=True)) as source_db:
            with closing(sqlite3.connect(temporary)) as backup_db:
                source_db.backup(backup_db)
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)

    backups = sorted(backup_dir.glob("leetpath-*.db"), reverse=True)
    for expired in backups[retention:]:
        expired.unlink()
    return destination


def _database_path(database_url: str) -> Path:
    url = make_url(database_url)
    if url.get_backend_name() != "sqlite" or not url.database or url.database == ":memory:":
        raise ValueError("backup service requires a file-based SQLite DATABASE_URL")
    return Path(url.database)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    source = _database_path(os.getenv("DATABASE_URL", "sqlite:///data/leetpath.db"))
    backup_dir = Path(os.getenv("BACKUP_DIR", "/app/backups"))
    interval = max(60, int(os.getenv("BACKUP_INTERVAL_SECONDS", "86400")))
    retention = max(1, int(os.getenv("BACKUP_RETENTION", "7")))

    while True:
        try:
            destination = backup_once(source, backup_dir, retention=retention)
            logger.info("SQLite backup created: %s", destination)
        except (FileNotFoundError, sqlite3.Error) as exc:
            logger.warning("SQLite backup skipped: %s", exc)
        time.sleep(interval)


if __name__ == "__main__":
    main()
