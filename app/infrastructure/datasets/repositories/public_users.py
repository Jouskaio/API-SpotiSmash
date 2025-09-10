import asyncio
import pandas as pd
from pylast import LastFMNetwork
from spotipy import Spotify
from concurrent.futures import ThreadPoolExecutor

from pathlib import Path
from app.use_cases.spotify.user_profile import get_user_profile
from app.use_cases.spotify.user_tracks import get_current_user_profile_tracks

DB_PATH = Path(__file__).resolve().parent.parent / "public_users.xlsx"
def load_public_user_ids(filepath: Path) -> list[str]:
    df = pd.read_excel(filepath)
    return df.iloc[:, 0].dropna().astype(str).tolist()

def import_user(user_id: str, spotify_client: Spotify, lastfm_client: LastFMNetwork):
    try:
        print(f"🎧 Importing user {user_id}...")
        user = get_user_profile(spotify_client, user_id)
        if not user:
            print(f"⚠️ Skipped {user_id}, profile not found.")
            return
        get_current_user_profile_tracks(spotify_client, user, lastfm_client)
        print(f"✅ Imported {user_id}")
    except Exception as e:
        print(f"❌ Failed to import {user_id}: {e}")

async def import_all_users_concurrently(spotify_client, lastfm_client):
    user_ids = load_public_user_ids(DB_PATH)
    print(f"📥 Found {len(user_ids)} public user IDs")

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=10) as executor:  # You can tune the concurrency level
        tasks = [
            loop.run_in_executor(executor, import_user, user_id, spotify_client, lastfm_client)
            for user_id in user_ids
        ]
        await asyncio.gather(*tasks)