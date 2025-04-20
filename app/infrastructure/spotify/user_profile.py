import logging
from spotipy import Spotify

from app.models.album import Album
from app.models.artist import Artist
from app.models.playlist import Playlist
from app.models.track import Track
from app.models.user import User


def get_user_profile(spotify_client: Spotify, id: str):
    """
    Get a user profile from Spotify API.
    """
    try:
        data = spotify_client.user(id)
        return User.from_api_response(data)
    except Exception as e:
        logging.error(f"Error getting user profile: {e}")
        return None


def get_current_user_profile_tracks(spotify_client: Spotify, user: User):
    """
    Get the current user's playlists and tracks from Spotify API.
    """
    try:
        logging.info(f"Fetching playlists for user: {user.get_id()}")
        data = spotify_client.user_playlists(user=user.get_id())
        playlist_items = data.get("items", [])

        playlists = [
            Playlist(name=pl["name"], id=pl["id"])
            for pl in playlist_items if pl.get("name") and pl.get("id")
        ]

        all_tracks = []

        for playlist in playlists:
            raw_tracks = spotify_client.playlist_items(playlist.get_id())
            track_items = raw_tracks.get("items", []) if raw_tracks else []
            tracks = []

            for item in track_items:
                track_data = item.get("track")
                if not track_data:
                    continue

                # Build Artist list
                artists: list[Artist] = [
                    Artist(name=artist.get("name"), id=artist.get("id"))
                    for artist in track_data.get("artists", [])
                    if artist.get("name")
                ]

                # Build Album artist list
                album_artists: list[Artist] = [
                    Artist(name=a.get("name"), id=a.get("id"))
                    for a in track_data.get("album", {}).get("artists", [])
                    if a.get("name")
                ]

                album = Album(
                    title=track_data.get("album", {}).get("name"),
                    id=track_data.get("album", {}).get("id"),
                    image=track_data.get("album", {}).get("images", [{}])[0].get("url"),
                    release_year=track_data.get("album", {}).get("release_date"),
                    artists=album_artists
                )

                track = Track(
                    title=track_data.get("name"),
                    artists=artists,
                    album=album,
                    id=track_data.get("id"),
                    url=track_data.get("external_urls", {}).get("spotify"),
                    duration=track_data.get("duration_ms")
                )

                tracks.append(track)

            playlist.set_tracks(tracks)
            all_tracks.extend(tracks)

        unique_tracks = {track.id: track for track in all_tracks if track.id}
        return list(unique_tracks.values())

    except Exception as e:
        logging.error(f"Error getting current user profile tracks: {e}")
        return []