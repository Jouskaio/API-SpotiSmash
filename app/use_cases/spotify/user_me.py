import logging

from app.infrastructure.spotify.client import SpotifyClientWithRetry


def get_user_me(spotify_client: SpotifyClientWithRetry):
    try:
        data = spotify_client.client.me()
        return data

    except Exception as e:
        logging.error(f"Error getting user profile: {e}")

