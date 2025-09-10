from app.models.playlist import Playlist
from app.infrastructure.database.orm import PlaylistORM, TrackORM

def map_playlist_to_orm(playlist: Playlist, user_id: str) -> PlaylistORM:
    playlist_orm = PlaylistORM(
        id=playlist.get_id(),
        name=playlist.get_name(),
        user_id=user_id
    )

    playlist_orm.tracks = [
        TrackORM(id=track.get_id())
        for track in playlist.get_tracks() if track.get_id()
    ]

    return playlist_orm