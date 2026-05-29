from __future__ import annotations

import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "submissions.db"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_database_path(db_path: str | Path | None = None) -> Path:
    if db_path is None:
        db_path = os.getenv("SUBMISSIONS_DB_PATH") or DEFAULT_DB_PATH

    path = Path(db_path).expanduser()
    if not path.is_absolute():
        path = (BASE_DIR / path).resolve()
    return path


def initialize_database(db_path: str | Path | None = None) -> Path:
    path = get_database_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path, timeout=30) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS submissions (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                status TEXT NOT NULL,
                model TEXT NOT NULL,
                temperature REAL NOT NULL,
                problem_statement TEXT NOT NULL,
                solution_code TEXT NOT NULL,
                editorial_markdown TEXT,
                error_message TEXT,
                metadata_json TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_submissions_created_at
            ON submissions(created_at DESC)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_submissions_status
            ON submissions(status)
            """
        )

    return path


def create_submission_record(
    *,
    problem_statement: str,
    solution_code: str,
    model: str,
    temperature: float,
    status: str = "received",
    editorial_markdown: str | None = None,
    error_message: str | None = None,
    metadata: Optional[dict[str, Any]] = None,
    db_path: str | Path | None = None,
) -> str:
    path = initialize_database(db_path)
    submission_id = str(uuid.uuid4())
    timestamp = _utc_now()

    with sqlite3.connect(path, timeout=30) as conn:
        conn.execute(
            """
            INSERT INTO submissions (
                id, created_at, updated_at, status, model, temperature,
                problem_statement, solution_code, editorial_markdown,
                error_message, metadata_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                submission_id,
                timestamp,
                timestamp,
                status,
                model,
                temperature,
                problem_statement,
                solution_code,
                editorial_markdown,
                error_message,
                json.dumps(metadata or {}, ensure_ascii=True),
            ),
        )

    return submission_id


def update_submission_record(
    submission_id: str,
    *,
    status: str,
    editorial_markdown: str | None = None,
    error_message: str | None = None,
    metadata: Optional[dict[str, Any]] = None,
    db_path: str | Path | None = None,
) -> None:
    path = initialize_database(db_path)
    timestamp = _utc_now()

    updates: list[str] = ["status = ?", "updated_at = ?"]
    values: list[Any] = [status, timestamp]

    if editorial_markdown is not None:
        updates.append("editorial_markdown = ?")
        values.append(editorial_markdown)

    if error_message is not None:
        updates.append("error_message = ?")
        values.append(error_message)

    if metadata is not None:
        updates.append("metadata_json = ?")
        values.append(json.dumps(metadata, ensure_ascii=True))

    values.append(submission_id)

    with sqlite3.connect(path, timeout=30) as conn:
        cursor = conn.execute(
            f"UPDATE submissions SET {', '.join(updates)} WHERE id = ?",
            values,
        )
        if cursor.rowcount == 0:
            raise KeyError(f"Submission not found: {submission_id}")


def fetch_submissions(
    *,
    db_path: str | Path | None = None,
    status: str | None = None,
    query: str | None = None,
    limit: int = 500,
) -> pd.DataFrame:
    path = initialize_database(db_path)

    clauses: list[str] = []
    params: list[Any] = []

    if status:
        clauses.append("status = ?")
        params.append(status)

    if query:
        like = f"%{query.strip()}%"
        clauses.append(
            "(id LIKE ? OR problem_statement LIKE ? OR solution_code LIKE ? OR editorial_markdown LIKE ? OR error_message LIKE ?)"
        )
        params.extend([like, like, like, like, like])

    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    sql = f"""
        SELECT
            id, created_at, updated_at, status, model, temperature,
            problem_statement, solution_code, editorial_markdown,
            error_message, metadata_json
        FROM submissions
        {where_sql}
        ORDER BY created_at DESC
        LIMIT ?
    """
    params.append(limit)

    with sqlite3.connect(path, timeout=30) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, params).fetchall()

    records = [dict(row) for row in rows]
    if not records:
        return pd.DataFrame(
            columns=[
                "id",
                "created_at",
                "updated_at",
                "status",
                "model",
                "temperature",
                "problem_statement",
                "solution_code",
                "editorial_markdown",
                "error_message",
                "metadata_json",
            ]
        )

    return pd.DataFrame.from_records(records)


def get_submission(submission_id: str, db_path: str | Path | None = None) -> dict[str, Any] | None:
    path = initialize_database(db_path)

    with sqlite3.connect(path, timeout=30) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """
            SELECT
                id, created_at, updated_at, status, model, temperature,
                problem_statement, solution_code, editorial_markdown,
                error_message, metadata_json
            FROM submissions
            WHERE id = ?
            """,
            (submission_id,),
        ).fetchone()

    return dict(row) if row else None
