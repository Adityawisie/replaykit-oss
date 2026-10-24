from __future__ import annotations
import json, sqlite3
from pathlib import Path
from typing import Any
from .config import DATA_DIR, DB_PATH


def connect() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    with connect() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS experiments (id TEXT PRIMARY KEY, data TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, experiment_id TEXT NOT NULL, data TEXT NOT NULL, created_at TEXT NOT NULL, FOREIGN KEY(experiment_id) REFERENCES experiments(id));
        CREATE TABLE IF NOT EXISTS comparisons (id TEXT PRIMARY KEY, experiment_id TEXT NOT NULL, data TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS analyses (id TEXT PRIMARY KEY, run_id TEXT NOT NULL, data TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS prompts (id TEXT PRIMARY KEY, run_id TEXT NOT NULL, data TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS verifications (id TEXT PRIMARY KEY, data TEXT NOT NULL, created_at TEXT NOT NULL);
        """)


def put(table: str, item_id: str, data: dict[str, Any], **columns: str) -> None:
    allowed = {"experiments", "runs", "comparisons", "analyses", "prompts", "verifications"}
    if table not in allowed: raise ValueError("Invalid table")
    payload = json.dumps(data, default=str)
    col_names = ["id", *columns.keys(), "data"]
    vals = [item_id, *columns.values(), payload]
    placeholders = ",".join("?" for _ in vals)
    with connect() as c:
        c.execute(f"INSERT OR REPLACE INTO {table} ({','.join(col_names)}) VALUES ({placeholders})", vals)


def get(table: str, item_id: str) -> dict[str, Any] | None:
    if table not in {"experiments", "runs", "comparisons", "analyses", "prompts", "verifications"}: raise ValueError("Invalid table")
    with connect() as c:
        row = c.execute(f"SELECT data FROM {table} WHERE id=?", (item_id,)).fetchone()
    return json.loads(row["data"]) if row else None


def list_items(table: str, limit: int = 100, experiment_id: str | None = None) -> list[dict[str, Any]]:
    if table not in {"experiments", "runs", "comparisons", "analyses", "prompts", "verifications"}: raise ValueError("Invalid table")
    with connect() as c:
        if table in {"runs", "comparisons"} and experiment_id:
            rows = c.execute(f"SELECT data FROM {table} WHERE experiment_id=? ORDER BY created_at DESC LIMIT ?", (experiment_id, limit)).fetchall()
        else:
            rows = c.execute(f"SELECT data FROM {table} ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    return [json.loads(r["data"]) for r in rows]
