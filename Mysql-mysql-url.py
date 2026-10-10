"""
spotify_mysql_urls.py
~~~~~~~~~~~~~~~~~~~~~
Read track URLs from a file and bulk-insert every track into MySQL.
"""

from spotify_utils import (
    get_spotify_client,
    extract_track_id,
    fetch_track_metadata,
    get_db_connection,
    insert_track,
)

URLS_FILE = "track_urls.txt"

# ── Setup ─────────────────────────────────────────────────────────────────────
sp         = get_spotify_client()
connection = get_db_connection()
cursor     = connection.cursor()

# ── Process ───────────────────────────────────────────────────────────────────
with open(URLS_FILE) as fh:
    urls = [line.strip() for line in fh if line.strip()]

for url in urls:
    try:
        track_id   = extract_track_id(url)
        track_data = fetch_track_metadata(sp, track_id)
        insert_track(cursor, track_data)
        connection.commit()
        print(f"Inserted: {track_data['Track Name']} by {track_data['Artist']}")
    except Exception as exc:
        print(f"Skipped {url!r}: {exc}")

cursor.close()
connection.close()
print("Done — all tracks processed.")