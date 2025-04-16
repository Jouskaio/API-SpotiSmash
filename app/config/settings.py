import os
from dotenv import load_dotenv

load_dotenv(override=False)
# Load environment variables from .env file
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SCOPE = "user-read-private user-read-email"
CACHE_PATH = ".cache"
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

