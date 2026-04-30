from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .models import ScanResult


class ScanStore:
    def __init__(self, db_path: str | Path = "scan_history.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def save(self, result: ScanResult) -> None:
        self._prune_old_records()
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO scans (
                    scan_id, url, verdict, timestamp, payload
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    result.scan_id,
                    result.url,
                    result.verdict.value,
                    result.timestamp.isoformat(),
                    json.dumps(result.to_dict()),
                ),
            )
            connection.commit()

    def get_history(self) -> list[ScanResult]:
        self._prune_old_records()
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                """
                SELECT payload
                FROM scans
                ORDER BY timestamp DESC
                """
            ).fetchall()
        return [ScanResult.from_dict(json.loads(row[0])) for row in rows]

    def get_by_url(self, url: str, within_hours: int) -> ScanResult | None:
        self._prune_old_records()
        cutoff = datetime.now(timezone.utc) - timedelta(hours=within_hours)
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(
                """
                SELECT payload
                FROM scans
                WHERE url = ? AND timestamp >= ?
                ORDER BY timestamp DESC
                LIMIT 1
                """,
                (url, cutoff.isoformat()),
            ).fetchone()
        return ScanResult.from_dict(json.loads(row[0])) if row else None

    def get_by_id(self, scan_id: str) -> ScanResult | None:
        self._prune_old_records()
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(
                """
                SELECT payload
                FROM scans
                WHERE scan_id = ?
                """,
                (scan_id,),
            ).fetchone()
        return ScanResult.from_dict(json.loads(row[0])) if row else None

    def _initialize(self) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS scans (
                    scan_id TEXT PRIMARY KEY,
                    url TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    payload TEXT NOT NULL
                )
                """
            )
            self._ensure_payload_column(connection)
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_scans_url_timestamp ON scans(url, timestamp DESC)"
            )
            connection.commit()

    def _ensure_payload_column(self, connection: sqlite3.Connection) -> None:
        columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(scans)").fetchall()
        }
        if "payload" not in columns:
            connection.execute("DROP TABLE scans")
            connection.execute(
                """
                CREATE TABLE scans (
                    scan_id TEXT PRIMARY KEY,
                    url TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    payload TEXT NOT NULL
                )
                """
            )

    def _prune_old_records(self) -> None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                "DELETE FROM scans WHERE timestamp < ?",
                (cutoff.isoformat(),),
            )
            connection.commit()
