import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def create_spotify_connection() -> spotipy.Spotify:

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    missing = [
        name
        for name, value in (
            ("SPOTIFY_CLIENT_ID", client_id),
            ("SPOTIFY_CLIENT_SECRET", client_secret),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(
            "Missing Spotify credentials: " + ", ".join(missing)
        )

    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret,
    )
    return spotipy.Spotify(auth_manager=auth_manager)
