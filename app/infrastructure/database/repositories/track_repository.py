from sqlalchemy.orm import Session
from app.infrastructure.database.orm import TrackORM
from app.models.track import Track
from app.infrastructure.database.orm import AlbumORM


def get_or_create_track_orm(track: Track, album_orm: AlbumORM, session: Session) -> TrackORM:
    track_cache = session.info.setdefault("track_cache", {})

    if track.get_id() in track_cache:
        return track_cache[track.get_id()]

    existing = session.get(TrackORM, track.get_id())
    if existing:
        track_cache[track.get_id()] = existing
        return existing

    track_orm = TrackORM(
        id=track.get_id(),
        title=track.get_title(),
        duration=track.get_duration(),
        url=track.get_url(),
        album=album_orm
    )
    session.add(track_orm)
    track_cache[track.get_id()] = track_orm
    return track_orm