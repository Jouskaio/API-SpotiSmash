import logging

from app.infrastructure.logging.setup_logging import setup_logging
from app.infrastructure.spotify.auth import get_spotify_client
from app.infrastructure.spotify.get_user_profile import get_user_profile

if __name__ == "__main__":
    setup_logging()
    spotify_client = get_spotify_client()
    profile = get_user_profile(spotify_client=spotify_client, id="desespery")
    logging.info(profile)
