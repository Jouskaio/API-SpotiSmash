import time
import logging
from pylast import LastFMNetwork, WSError
from app.config.settings import LASTFM_API_KEY, LASTFM_API_SECRET

RETRY_ATTEMPTS = 3
RETRY_DELAY = 2

class LastFMClientWithRetry:
    def __init__(self):
        self.client = LastFMNetwork(api_key=LASTFM_API_KEY, api_secret=LASTFM_API_SECRET)

    def safe_call(self, func, *args, **kwargs):
        for attempt in range(RETRY_ATTEMPTS):
            try:
                return func(*args, **kwargs)
            except WSError as e:
                if "rate limit" in str(e).lower():
                    logging.debug("Last.fm rate limit hit. Waiting...")
                    time.sleep(RETRY_DELAY)
                else:
                    logging.error(f"Last.fm error: {e}")
                    raise e
            except Exception as e:
                logging.warning(f"Unexpected Last.fm error: {e}")
                time.sleep(RETRY_DELAY)
        raise RuntimeError("Last.fm max retry attempts exceeded")

    def get_track_tags(self, artist_name: str, track_title: str) -> list[str]:
        return self.safe_call(
            lambda: [
                tag.item.get_name() for tag in self.client.get_track(artist_name, track_title).get_top_tags(limit=5)
            ]
        )

