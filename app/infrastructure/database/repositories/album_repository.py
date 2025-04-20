import logging

from sqlalchemy.orm import Session

from app.infrastructure.database.orm import AlbumORM, ArtistORM
from app.models.album import Album


def get_or_create_album_orm(album: Album, session: Session) -> AlbumORM:
    if not album.get_id():
        raise logging.error("Album ID is required to get or create an AlbumORM")

    album_cache = session.info.setdefault("album_cache", {})
    artist_cache = session.info.setdefault("artist_cache", {})

    # Cache album
    if album.get_id() in album_cache:
        return album_cache[album.get_id()]

    existing_album = session.get(AlbumORM, album.get_id())
    if existing_album:
        album_cache[album.get_id()] = existing_album
        return existing_album

    artist_orms = []
    for artist in album.get_artists():
        artist_id = artist.get_id()
        if not artist_id:
            continue

        # Check artist cache
        if artist_id in artist_cache:
            artist_orm = artist_cache[artist_id]
        else:
            artist_orm = session.get(ArtistORM, artist_id)
            if not artist_orm:
                artist_orm = ArtistORM(
                    id=artist_id,
                    name=artist.get_name(),
                    image=artist.get_image()
                )
                session.add(artist_orm)
            artist_cache[artist_id] = artist_orm

        artist_orms.append(artist_orm)

    album_orm = AlbumORM(
        id=album.get_id(),
        title=album.get_title(),
        release_year=album.get_release_year(),
        image=album.get_image(),
        artists=artist_orms
    )
    session.add(album_orm)
    album_cache[album.get_id()] = album_orm
    return album_orm