import re
from typing import List, Dict, Any
import spotipy

def extract_track_id(url: str) -> str:
    """Parse a Spotify track URL and return the track ID."""
    match = re.search(r"track/([a-zA-Z0-9]+)", url)
    if not match:
        raise ValueError(f"Invalid Spotify track URL: {url!r}")
    return match.group(1)

def fetch_track_metadata(sp: spotipy.Spotify, track_id: str) -> Dict[str, Any]:
    """Fetch a track from the API."""
    return sp.track(track_id)

def get_track_urls_from_file(file_path: str) -> List[str]:
    """Read track URLs from a file."""
    try:
        with open(file_path, 'r') as fh:
            return [line.strip() for line in fh if line.strip()]
    except FileNotFoundError:
        return []
