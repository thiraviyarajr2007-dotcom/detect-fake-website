from __future__ import annotations

import hashlib
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


@dataclass(slots=True)
class User:
    user_id: str
    username: str
    email: str
    created_at: datetime


class AuthStore:
    SESSION_TTL_HOURS = 72

    def __init__(self, db_path: str | Path = "scan_history.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def register(self, username: str, email: str, password: str) -> User | None:
        user_id = secrets.token_hex(12)
        pw_hash = self._hash_password(password)
        now = datetime.now(timezone.utc)
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO users (user_id, username, email, password_hash, created_at) VALUES (?, ?, ?, ?, ?)",
                    (user_id, username.strip(), email.strip().lower(), pw_hash, now.isoformat()),
                )
                conn.commit()
        except sqlite3.IntegrityError:
            return None
        return User(user_id=user_id, username=username.strip(), email=email.strip().lower(), created_at=now)

    def authenticate(self, username: str, password: str) -> User | None:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT user_id, username, email, password_hash, created_at FROM users WHERE username = ? OR email = ?",
                (username.strip(), username.strip().lower()),
            ).fetchone()
        if row is None:
            return None
        stored_hash = row[3]
        if stored_hash != self._hash_password(password):
            return None
        return User(user_id=row[0], username=row[1], email=row[2], created_at=datetime.fromisoformat(row[4]))

    def create_session(self, user_id: str) -> str:
        token = secrets.token_urlsafe(32)
        expires = datetime.now(timezone.utc) + timedelta(hours=self.SESSION_TTL_HOURS)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
                (token, user_id, expires.isoformat()),
            )
            conn.commit()
        return token

    def get_user_by_session(self, token: str) -> User | None:
        now = datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                """
                SELECT u.user_id, u.username, u.email, u.created_at
                FROM sessions s JOIN users u ON s.user_id = u.user_id
                WHERE s.token = ? AND s.expires_at > ?
                """,
                (token, now),
            ).fetchone()
        if row is None:
            return None
        return User(user_id=row[0], username=row[1], email=row[2], created_at=datetime.fromisoformat(row[3]))

    def delete_session(self, token: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
            conn.commit()

    def _initialize(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    token TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
                """
            )
            conn.commit()

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
