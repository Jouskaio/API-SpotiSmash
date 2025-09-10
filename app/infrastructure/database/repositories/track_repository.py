import logging

from sqlalchemy.orm import Session

from app.infrastructure.database.orm import AlbumORM, TrackORM, TagORM
from app.infrastructure.database.repositories.artist_repository import get_or_create_artist_orm
from app.infrastructure.lastfm.client import LastFMClientWithRetry
from app.models.track import Track


import logging
from sqlalchemy.orm import Session

from app.infrastructure.database.orm import AlbumORM, TrackORM, TagORM
from app.infrastructure.database.repositories.artist_repository import get_or_create_artist_orm
from app.infrastructure.lastfm.client import LastFMClientWithRetry
from app.models.track import Track

def get_or_create_track_orm(
    track: Track,
    album_orm: AlbumORM,
    session: Session,
    lastfm_client: LastFMClientWithRetry
) -> TrackORM:
    track_cache = session.info.setdefault("track_cache", {})
    tag_cache = session.info.setdefault("tag_cache", {})

    # Check minimal info
    if not track.get_id() or not track.get_artist():
        logging.warning(f"⚠️ Track missing ID or artists: {track}")
        return None

    # Check cache
    if track.get_id() in track_cache:
        return track_cache[track.get_id()]

    # Check DB
    existing = session.get(TrackORM, track.get_id())
    if existing:
        track_cache[track.get_id()] = existing
        return existing

    # Build new TrackORM
    track_orm = TrackORM(
        id=track.get_id(),
        title=track.get_title(),
        duration=track.get_duration(),
        url=track.get_url(),
        album=album_orm,
    )

    # Attach artist ORM
    track_orm.artists = [
        get_or_create_artist_orm(artist, session)
        for artist in track.get_artist()
        if artist.get_id()
    ]

    # Attach tag ORM (from Last.fm)
    for artist in track.get_artist():
        try:
            tags = lastfm_client.get_track_tags(artist_name=artist.get_name(), track_title=track.get_title())
            for tag_name in tags:
                tag_name = tag_name.lower()
                if tag_name in tag_cache:
                    tag_orm = tag_cache[tag_name]
                else:
                    tag_orm = session.get(TagORM, tag_name)
                    if not tag_orm:
                        tag_orm = TagORM(name=tag_name)
                        session.add(tag_orm)
                    tag_cache[tag_name] = tag_orm

                if tag_orm not in track_orm.tags:
                    track_orm.tags.append(tag_orm)

        except Exception as e:
            logging.warning(f"❌ Failed to fetch Last.fm tags for '{track.get_title()}' by '{artist.get_name()}': {e}")

    session.add(track_orm)
    track_cache[track.get_id()] = track_orm
    return track_orm