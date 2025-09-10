from app.models.playlist import Playlist


class User:
    def __init__(self, id: str,
                 display_name: str = None,
                 photo: str = None,
                 uri: str = None,
                 playlists: [Playlist] = None):
        """
        Initialize a User object.
        :param id: str
        :param display_name: str
        :param photo: str
        :param uri: str
        :param playlists: List[Playlist]
        """
        self.id = id
        self.display_name = display_name
        self.photo = photo
        self.uri = uri
        self.playlists = playlists if playlists else []

    @classmethod
    def from_api_response(cls, data: dict):
        return cls(
            id=data.get("id"),
            display_name=data.get("display_name"),
            photo=(data.get("images")[0]["url"] if data.get("images") else None),
            uri=data.get("uri")
        )

    # Getters
    def get_id(self):
        """
        Get the user ID.
        :return: User ID
        """
        return self.id

    def get_display_name(self):
        """
        Get the user display name.
        :return: User display name
        """
        return self.display_name

    def get_photo(self):
        """
        Get the user photo.
        :return: User photo
        """
        return self.photo

    def get_user_uri(self):
        """
        Get the user URI.
        :return: User URI
        """
        return self.uri

    def get_playlists(self):
        """
        Get the user's playlists.
        :return: List of playlists
        """
        return self.playlists

    #    Setters
    def set_display_name(self, display_name):
        """
        Set the user display name.
        :param display_name: User display name
        :return: User object
        """
        self.display_name = display_name
        return self

    def set_photo(self, photo):
        """
        Set the user photo.
        :param photo: User photo
        :return: User object
        """
        self.photo = photo
        return self

    def set_uri(self, uri):
        """
        Set the user URI.
        :param uri: User URI
        :return: User object
        """
        self.uri = uri
        return self

    def set_id(self, id):
        """
        Set the user ID.
        :param id: User ID
        :return: User object
        """
        self.id = id
        return self

    def set_playlists(self, playlists):
        """
        Set the user's playlists.
        :param playlists: List of playlists
        :return: User object
        """
        self.playlists = playlists
        return self

    def add_playlist(self, playlist):
        """
        Add a playlist to the user's playlists.
        :param playlist: Playlist object
        :return: User object
        """
        self.playlists.append(playlist)
        return self

    def __repr__(self):
        return f"User(id={self.id}, name={self.display_name})"