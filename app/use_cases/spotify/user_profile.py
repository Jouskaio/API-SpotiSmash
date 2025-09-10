import logging

from pylast import LastFMNetwork
from spotipy import Spotify

from app.infrastructure.database.connection import get_db_session
from app.infrastructure.database.orm import UserORM
from app.infrastructure.spotify.client import SpotifyClientWithRetry
from app.models.user import User


def get_user_profile(spotify_client: SpotifyClientWithRetry, id: str):
    try:
        data = spotify_client.client.user(id)
        user = User.from_api_response(data)

        session = get_db_session()
        user_orm = session.query(UserORM).filter_by(id=user.get_id()).first()

        if user_orm:
            user_orm.display_name = user.get_display_name()
            user_orm.photo = user.get_photo()
            user_orm.uri = user.get_user_uri()
        else:
            user_orm = UserORM(
                id=user.get_id(),
                display_name=user.get_display_name(),
                photo=user.get_photo(),
                uri=user.get_user_uri()
            )
            session.add(user_orm)

        session.commit()
        session.close()

        return user

    except Exception as e:
        logging.error(f"Error getting user profile: {e}")
        return None
