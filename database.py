import os
from typing import Any, Dict, List

DATABASE_URL = os.getenv("DATABASE_URL")
DB_PATH = os.getenv("DATABASE_PATH", "data/sbsb_demo.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

USE_POSTGRES = bool(DATABASE_URL and DATABASE_URL.startswith("postgres"))

if USE_POSTGRES:
    import psycopg2
    import psycopg2.extras
else:
    import sqlite3


def get_connection():
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    if USE_POSTGRES:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                if os.path.exists(SCHEMA_PATH):
                    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                        cur.execute(f.read())
                    conn.commit()
        finally:
            conn.close()
        return

    conn = get_connection()
    try:
        if os.path.exists(SCHEMA_PATH):
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
                conn.commit()
    finally:
        conn.close()


def list_items() -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        if USE_POSTGRES:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT id, title, category, created_at FROM items ORDER BY id DESC")
                return [dict(row) for row in cur.fetchall()]
        cursor = conn.execute("SELECT id, title, category, created_at FROM items ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def create_item(title: str, category: str = "general") -> Dict[str, Any]:
    conn = get_connection()
    try:
        if USE_POSTGRES:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    "INSERT INTO items (title, category) VALUES (%s, %s) RETURNING id, title, category, created_at",
                    (title, category),
                )
                created = dict(cur.fetchone())
                cur.execute(
                    "INSERT INTO deploy_logs (event, details) VALUES (%s, %s)",
                    ("ITEM_CREATED", f"새 항목 생성: {title}"),
                )
                conn.commit()
                return created
        cursor = conn.execute(
            "INSERT INTO items (title, category) VALUES (?, ?)",
            (title, category),
        )
        conn.execute(
            "INSERT INTO deploy_logs (event, details) VALUES (?, ?)",
            ("ITEM_CREATED", f"새 항목 생성: {title}"),
        )
        conn.commit()
        item_id = cursor.lastrowid
        row = conn.execute("SELECT id, title, category, created_at FROM items WHERE id = ?", (item_id,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def delete_item(item_id: int) -> bool:
    conn = get_connection()
    try:
        if USE_POSTGRES:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
                cur.execute(
                    "INSERT INTO deploy_logs (event, details) VALUES (%s, %s)",
                    ("ITEM_DELETED", f"항목 삭제 (ID: {item_id})"),
                )
                conn.commit()
                return cur.rowcount > 0
        cursor = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.execute(
            "INSERT INTO deploy_logs (event, details) VALUES (?, ?)",
            ("ITEM_DELETED", f"항목 삭제 (ID: {item_id})"),
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def get_db_status() -> Dict[str, Any]:
    conn = get_connection()
    try:
        if USE_POSTGRES:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM items")
                item_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM deploy_logs")
                log_count = cur.fetchone()[0]
                return {
                    "status": "connected",
                    "engine": "PostgreSQL",
                    "database_url_configured": True,
                    "total_items": item_count,
                    "total_logs": log_count,
                }
        item_count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        log_count = conn.execute("SELECT COUNT(*) FROM deploy_logs").fetchone()[0]
        db_size_bytes = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
        return {
            "status": "connected",
            "engine": "SQLite",
            "db_path": os.path.abspath(DB_PATH),
            "size_bytes": db_size_bytes,
            "total_items": item_count,
            "total_logs": log_count,
        }
    finally:
        conn.close()
