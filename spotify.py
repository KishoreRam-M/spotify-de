import re
import spotipy
import mysql.connector
from spotipy.oauth2 import SpotifyClientCredentials
from Config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, DB_CONFIG



def get_spotify_client() -> spotipy.Spotify:
    """Return an authenticated Spotify client."""
    return spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
        )
    )


def extract_track_id(url: str) -> str:
    """Parse a Spotify track URL and return the track ID."""
    match = re.search(r"track/([a-zA-Z0-9]+)", url)
    if not match:
        raise ValueError(f"Invalid Spotify track URL: {url!r}")
    return match.group(1)


def fetch_track_metadata(sp: spotipy.Spotify, track_id: str) -> dict:
    """Fetch a track from the API and return a flat metadata dict."""
    track = sp.track(track_id)
    return {
        "Track Name":          track["name"],
        "Artist":              track["artists"][0]["name"],
        "Album":               track["album"]["name"],
        "Popularity":          track["popularity"],
        "Duration (minutes)":  track["duration_ms"] / 60_000,
    }



_INSERT_QUERY = """
    INSERT INTO spotify_tracks
        (track_name, artist, album, popularity, duration_minutes)
    VALUES (%s, %s, %s, %s, %s)
"""


def get_db_connection() -> mysql.connector.MySQLConnection:
    """Return an open MySQL connection using settings from config."""
    return mysql.connector.connect(**DB_CONFIG)


def insert_track(cursor, track_data: dict) -> None:
    """Execute a single INSERT for *track_data* using *cursor*."""
    cursor.execute(
        _INSERT_QUERY,
        (
            track_data["Track Name"],
            track_data["Artist"],
            track_data["Album"],
            track_data["Popularity"],
            track_data["Duration (minutes)"],
        ),
    )