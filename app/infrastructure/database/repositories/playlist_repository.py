from sqlalchemy.orm import Session
from app.infrastructure.database.orm import PlaylistORM
from app.models.playlist import Playlist


def get_or_create_playlist_orm(playlist: Playlist, user_id: str, session: Session) -> PlaylistORM:
    playlist_cache = session.info.setdefault("playlist_cache", {})

    if playlist.get_id() in playlist_cache:
        return playlist_cache[playlist.get_id()]

    existing = session.get(PlaylistORM, playlist.get_id())
    if existing:
        playlist_cache[playlist.get_id()] = existing
        return existing

    playlist_orm = PlaylistORM(
        id=playlist.get_id(),
        name=playlist.get_name(),
        user_id=user_id
    )
    session.add(playlist_orm)
    playlist_cache[playlist.get_id()] = playlist_orm
    return playlist_orm