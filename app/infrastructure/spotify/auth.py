import logging

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from app.config.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

def get_spotify_client():
    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    return spotipy.Spotify(auth_manager=auth_manager)