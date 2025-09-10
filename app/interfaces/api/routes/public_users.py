import asyncio
from pathlib import Path

from fastapi import APIRouter

from app.infrastructure.datasets.repositories.public_users import import_all_users_concurrently
from app.infrastructure.lastfm.client import LastFMClientWithRetry
from app.infrastructure.spotify.client import SpotifyClientWithRetry

DB_PATH = Path(__file__).resolve().parent.parent / "public_users.xlsx"
router = APIRouter()

@router.get("/public-users")
async def get_public_users():
    spotify_client = SpotifyClientWithRetry()
    lastfm_client = LastFMClientWithRetry()
    await import_all_users_concurrently(spotify_client, lastfm_client)
