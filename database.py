import sqlite3
from contextlib import contextmanager

DB_PATH = "licenses.db"


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS licenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_key TEXT UNIQUE NOT NULL,
                product_name TEXT NOT NULL,
                customer_email TEXT,
                max_activations INTEGER NOT NULL DEFAULT 1,
                status TEXT NOT NULL DEFAULT 'active',
                expires_at TEXT,
                note TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS activations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_id INTEGER NOT NULL,
                device_id TEXT NOT NULL,
                activated_at TEXT NOT NULL DEFAULT (datetime('now')),
                last_validated_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (license_id) REFERENCES licenses (id),
                UNIQUE (license_id, device_id)
            )
        """)
        db.commit()


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()
