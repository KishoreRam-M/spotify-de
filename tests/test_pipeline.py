import pytest
from src.pipeline.transform import transform_track_data
from src.pipeline.extract import extract_track_id

def test_extract_track_id():
    url = "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"
    assert extract_track_id(url) == "3n3Ppam7vgaVa1iaRUc9Lp"
    
    with pytest.raises(ValueError):
        extract_track_id("invalid_url")

def test_transform_track_data():
    raw_data = {
        "id": "123",
        "name": "Test Track",
        "artists": [{"name": "Test Artist"}],
        "album": {"name": "Test Album"},
        "popularity": 85,
        "duration_ms": 120000
    }
    
    transformed = transform_track_data(raw_data)
    assert transformed["track_id"] == "123"
    assert transformed["track_name"] == "Test Track"
    assert transformed["artist"] == "Test Artist"
    assert transformed["album"] == "Test Album"
    assert transformed["popularity"] == 85
    assert transformed["duration_minutes"] == 2.0

def test_transform_missing_fields():
    raw_data = {
        "name": "Test Track",
    }
    with pytest.raises(ValueError):
        transform_track_data(raw_data)
