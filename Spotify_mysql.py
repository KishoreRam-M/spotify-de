"""
spotify_mysql.py
~~~~~~~~~~~~~~~~
Fetch a single track from the Spotify API and insert it into MySQL.
"""

from spotify_utils import (
    get_spotify_client,
    extract_track_id,
    fetch_track_metadata,
    get_db_connection,
    insert_track,
)

TRACK_URL = "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"

# ── Fetch ─────────────────────────────────────────────────────────────────────
sp         = get_spotify_client()
track_id   = extract_track_id(TRACK_URL)
track_data = fetch_track_metadata(sp, track_id)

# ── Insert ────────────────────────────────────────────────────────────────────
connection = get_db_connection()
cursor     = connection.cursor()

insert_track(cursor, track_data)
connection.commit()

print(f"Inserted: '{track_data['Track Name']}' by {track_data['Artist']}")

cursor.close()
connection.close()