import sqlite3
from datetime import datetime, timedelta, timezone


def test_backup_is_consistent_and_retention_is_enforced(tmp_path):
    from app.backup import backup_once

    source = tmp_path / "leetpath.db"
    with sqlite3.connect(source) as db:
        db.execute("CREATE TABLE marker (value TEXT NOT NULL)")
        db.execute("INSERT INTO marker VALUES ('ok')")
        db.commit()

    backup_dir = tmp_path / "backups"
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for day in range(8):
        backup_once(source, backup_dir, retention=7, now=start + timedelta(days=day))

    backups = sorted(backup_dir.glob("leetpath-*.db"))
    assert len(backups) == 7
    assert "20260102" in backups[0].name
    with sqlite3.connect(backups[-1]) as db:
        assert db.execute("SELECT value FROM marker").fetchone() == ("ok",)
