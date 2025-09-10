from sqlalchemy.orm import Session
from app.models.artist import Artist
from app.infrastructure.database.orm import ArtistORM

def get_or_create_artist_orm(artist: Artist, session: Session) -> ArtistORM:
    artist_cache = session.info.setdefault("artist_cache", {})
    artist_id = artist.get_id()

    if not artist_id:
        raise ValueError("Artist ID is required")

    # Check cache
    if artist_id in artist_cache:
        return artist_cache[artist_id]

    # Check DB
    existing = session.get(ArtistORM, artist_id)
    if existing:
        artist_cache[artist_id] = existing
        return existing

    # Create new ArtistORM
    artist_orm = ArtistORM(
        id=artist_id,
        name=artist.get_name(),
        image=artist.get_image()
    )

    session.add(artist_orm)
    artist_cache[artist_id] = artist_orm
    return artist_orm