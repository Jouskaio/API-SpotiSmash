import logging
from spotipy import Spotify

from app.infrastructure.spotify.client import SpotifyClientWithRetry


def clean_user_me(spotify_client: SpotifyClientWithRetry):
    try:
        # Get user profile
        user = spotify_client.client.me()
        user_id = user['id']

        # Get all playlists
        playlists = spotify_client.client.current_user_playlists()
        watch_later = None
        for playlist in playlists['items']:
            if playlist['name'] == "Watch Later":
                watch_later = playlist
                break

        # Create "Watch Later" if it doesn't exist
        if not watch_later:
            watch_later = spotify_client.client.user_playlist_create(user_id, "Watch Later", public=False)

        watch_later_id = watch_later['id']

        # Get all liked tracks
        liked_tracks = []
        results = spotify_client.client.current_user_saved_tracks()
        while results:
            liked_tracks.extend([item['track']['id'] for item in results['items']])
            if results['next']:
                results = spotify_client.client.next(results)
            else:
                break

        # Get all tracks in all playlists
        playlist_tracks = set()
        for playlist in playlists['items']:
            tracks = spotify_client.playlist_items(playlist['id'])
            while tracks:
                playlist_tracks.update([item['track']['id'] for item in tracks['items'] if item['track']])
                if tracks['next']:
                    tracks = spotify_client.client.next(tracks)
                else:
                    break

        # Find liked tracks not in any playlist
        tracks_to_add = [track_id for track_id in liked_tracks if track_id not in playlist_tracks]

        # Add them to "Watch Later"
        if tracks_to_add:
            # Spotify API allows max 100 tracks per add
            for i in range(0, len(tracks_to_add), 100):
                spotify_client.client.playlist_add_items(watch_later_id, tracks_to_add[i:i + 100])

        return user

    except Exception as e:
        logging.error(f"Error in clean_user_me: {e}")
