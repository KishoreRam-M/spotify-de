from typing import Dict, Any, Tuple
from src.database.connection import get_connection

def insert_or_update_track(track_data: Dict[str, Any]) -> Tuple[bool, bool]:
    """
    Insert or update a track.
    Returns (inserted, updated) booleans.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Check if exists
        cursor.execute("SELECT track_id FROM spotify_tracks WHERE track_id = ?", (track_data["track_id"],))
        exists = cursor.fetchone() is not None
        
        if exists:
            # Update
            cursor.execute("""
                UPDATE spotify_tracks
                SET track_name = ?, artist = ?, album = ?, popularity = ?, duration_minutes = ?
                WHERE track_id = ?
            """, (
                track_data["track_name"],
                track_data["artist"],
                track_data["album"],
                track_data["popularity"],
                track_data["duration_minutes"],
                track_data["track_id"]
            ))
            return False, True
        else:
            # Insert
            cursor.execute("""
                INSERT INTO spotify_tracks (track_id, track_name, artist, album, popularity, duration_minutes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                track_data["track_id"],
                track_data["track_name"],
                track_data["artist"],
                track_data["album"],
                track_data["popularity"],
                track_data["duration_minutes"]
            ))
            return True, False

def log_pipeline_run(status: str, records_fetched: int = 0, records_inserted: int = 0, 
                    records_updated: int = 0, records_failed: int = 0, error_message: str = None) -> int:
    """Log a pipeline run and return the run_id."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pipeline_runs (status, records_fetched, records_inserted, 
                                     records_updated, records_failed, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (status, records_fetched, records_inserted, records_updated, records_failed, error_message))
        return cursor.lastrowid
        
def finish_pipeline_run(run_id: int, status: str, records_fetched: int, records_inserted: int,
                       records_updated: int, records_failed: int, error_message: str = None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pipeline_runs
            SET end_time = CURRENT_TIMESTAMP, status = ?, records_fetched = ?,
                records_inserted = ?, records_updated = ?, records_failed = ?, error_message = ?
            WHERE run_id = ?
        """, (status, records_fetched, records_inserted, records_updated, records_failed, error_message, run_id))
