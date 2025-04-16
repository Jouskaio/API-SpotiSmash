import logging

from spotipy import Spotify

from app.models.user import User


def get_user_profile(spotify_client: Spotify, id: str):
    """
    Get a user profile from Spotify API.
    :param spotify_client: Spotify client
    :param id: User ID
    :return: User object
    """
    try:
        # Get the user profile
        data = spotify_client.user(id)
        # Extract relevant information
        return User.from_api_response(data)
    except Exception as e:
        # Handle the error
        logging.error(f"Error getting user profile: {e}")
        return None
