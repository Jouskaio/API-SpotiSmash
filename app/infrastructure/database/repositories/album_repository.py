import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.infrastructure.database.orm import AlbumORM
from app.infrastructure.database.repositories.artist_repository import get_or_create_artist_orm
from app.models.album import Album

def get_or_create_album_orm(album: Album, session: Session) -> AlbumORM:
    album_cache = session.info.setdefault("album_cache", {})

    album_id = album.get_id()
    if not album_id:
        raise ValueError("Album ID is required")

    # Cache check
    if album_id in album_cache:
        return album_cache[album_id]

    # DB check
    existing = session.get(AlbumORM, album_id)
    if existing:
        album_cache[album_id] = existing
        return existing

    # Create artists
    artist_orms = [
        get_or_create_artist_orm(artist, session)
        for artist in album.get_artists()
        if artist.get_id()
    ]

    # Build new AlbumORM
    album_orm = AlbumORM(
        id=album.get_id(),
        title=album.get_title(),
        release_year=album.get_release_year(),
        image=album.get_image(),
        artists=artist_orms
    )

    try:
        session.add(album_orm)
        session.flush()  # Trigger insert, catch error now
        album_cache[album_id] = album_orm
        return album_orm

    except IntegrityError:
        session.rollback()
        logging.warning(f"⚠️ Album already inserted by another thread: {album_id}")
        existing = session.get(AlbumORM, album_id)
        album_cache[album_id] = existing
        return existing