from src.database.connection import get_connection

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS spotify_tracks (
    track_id TEXT PRIMARY KEY,
    track_name TEXT NOT NULL,
    artist TEXT NOT NULL,
    album TEXT NOT NULL,
    popularity INTEGER,
    duration_minutes REAL,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    status TEXT,
    records_fetched INTEGER DEFAULT 0,
    records_inserted INTEGER DEFAULT 0,
    records_updated INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    error_message TEXT
);
"""

def init_db():
    """Initialize the SQLite database schema."""
    with get_connection() as conn:
        conn.executescript(SCHEMA_SQL)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
