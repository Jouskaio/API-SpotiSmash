from sqlalchemy.orm import Session
from app.infrastructure.database.orm import AlbumORM, ArtistORM
from app.models.album import Album

def map_album_to_orm(album: Album, session: Session) -> AlbumORM:
    # Check if the album already exists in the database
    existing_album = session.query(AlbumORM).filter_by(id=album.get_id()).first()
    if existing_album:
        existing_album.title = album.get_title()
        existing_album.release_year = album.get_release_year()
        existing_album.image = album.get_image()
    else:
        existing_album = AlbumORM(
            id=album.get_id(),
            title=album.get_title(),
            release_year=album.get_release_year(),
            image=album.get_image()
        )
        session.add(existing_album)

    # Map artists
    artist_orms = []
    for artist in album.get_artists():
        existing_artist = session.query(ArtistORM).filter_by(id=artist.get_id()).first()
        if existing_artist:
            artist_orms.append(existing_artist)
        else:
            new_artist = ArtistORM(
                id=artist.get_id(),
                name=artist.get_name(),
                image=artist.get_image()
            )
            session.add(new_artist)
            artist_orms.append(new_artist)

    # Update relation (clear then append, to prevent duplicates)
    existing_album.artists.clear()
    existing_album.artists.extend(artist_orms)

    return existing_album