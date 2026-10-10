from typing import Dict, Any

def transform_track_data(raw_track: Dict[str, Any]) -> Dict[str, Any]:
    """Transform raw Spotify track data into a flat structure suitable for the database."""
    try:
        return {
            "track_id": raw_track["id"],
            "track_name": raw_track["name"],
            "artist": raw_track["artists"][0]["name"] if raw_track.get("artists") else "Unknown",
            "album": raw_track["album"]["name"] if raw_track.get("album") else "Unknown",
            "popularity": raw_track.get("popularity", 0),
            "duration_minutes": round(raw_track.get("duration_ms", 0) / 60000.0, 2),
        }
    except KeyError as e:
        raise ValueError(f"Missing required field in track data: {e}")
