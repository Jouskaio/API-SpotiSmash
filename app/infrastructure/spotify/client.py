import time
import logging
import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from app.config.settings import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
)

RETRY_ATTEMPTS = 3
RETRY_DELAY = 2

class SpotifyClientWithRetry:
    def __init__(
        self,
        use_user_auth=False,
        scope="user-library-read user-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private",
        redirect_uri=None,
        state=None
    ):
        if use_user_auth:
            self.auth_manager = SpotifyOAuth(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
                redirect_uri=redirect_uri or SPOTIFY_REDIRECT_URI,
                scope=scope,
                state=state
            )
        else:
            self.auth_manager = SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET
            )
        self.client = spotipy.Spotify(auth_manager=self.auth_manager)

    def safe_call(self, func, *args, **kwargs):
        for attempt in range(RETRY_ATTEMPTS):
            try:
                return func(*args, **kwargs)
            except SpotifyException as e:
                if e.http_status == 429:
                    wait = int(e.headers.get("Retry-After", RETRY_DELAY))
                    logging.debug(f"Spotify rate limit hit. Waiting {wait}s...")
                    time.sleep(wait)
                else:
                    logging.error(f"Spotify error: {e}")
                    raise e
            except Exception as e:
                logging.warning(f"Unexpected Spotify error: {e}")
                time.sleep(RETRY_DELAY)
        raise RuntimeError("Spotify max retry attempts exceeded")

    def user_playlists(self, user_id):
        return self.safe_call(self.client.user_playlists, user=user_id)

    def playlist_items(self, playlist_id):
        return self.safe_call(self.client.playlist_items, playlist_id)

    def audio_features(self, track_ids):
        return self.safe_call(self.client.audio_features, track_ids)
