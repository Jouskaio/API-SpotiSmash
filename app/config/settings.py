import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=False)
# Load environment variables from .env file
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
LASTFM_API_KEY= os.getenv("LASTFM_API_KEY")
LASTFM_API_SECRET= os.getenv("LASTFM_API_SECRET")
SPOTIFY_REDIRECT_URI= os.getenv("SPOTIFY_REDIRECT_URI")