import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "spotify_data.db"
