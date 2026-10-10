import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import logging

logger = logging.getLogger(__name__)

def get_spotify_client() -> spotipy.Spotify:
    """Return an authenticated Spotify client."""
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        logger.warning("Spotify credentials missing.")
        raise ValueError("Spotify credentials not set in environment.")
        
    return spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
        ),
        requests_timeout=10,
        retries=3
    )
