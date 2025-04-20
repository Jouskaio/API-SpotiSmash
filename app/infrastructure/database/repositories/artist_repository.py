from typing import Union, Type

from sqlalchemy.orm import Session

from app.infrastructure.database.orm import ArtistORM
from app.models.artist import Artist


def get_or_create_artist_orm(artist: Artist, session: Session) -> Union[Type[ArtistORM], None, ArtistORM]:
    if not artist.get_id():
        raise ValueError("Artist ID is required to get or create an ArtistORM")

    if not hasattr(session.info, "artist_cache"):
        session.info["artist_cache"] = set()

    if artist.get_id() in session.info["artist_cache"]:
        return session.get(ArtistORM, artist.get_id())

    existing_artist = session.get(ArtistORM, artist.get_id())
    if existing_artist:
        session.info["artist_cache"].add(artist.get_id())
        return existing_artist

    artist_orm = ArtistORM(
        id=artist.get_id(),
        name=artist.get_name(),
        image=artist.get_image()
    )
    session.add(artist_orm)
    session.info["artist_cache"].add(artist.get_id())
    return artist_orm