import sqlite3
from typing import Generator
from src.config import DB_PATH

def get_connection() -> sqlite3.Connection:
    """Return an open SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
