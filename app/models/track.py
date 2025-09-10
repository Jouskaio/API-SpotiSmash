from typing import List, Optional
from app.models.album import Album
from app.models.artist import Artist
from app.models.tag import Tag


class Track:
    def __init__(
        self,
        title: str,
        artists: Optional[List[Artist]] = None,
        album: Optional[Album] = None,
        id: Optional[str] = None,
        url: Optional[str] = None,
        duration: Optional[int] = None,
        tags: Optional[List[Tag]] = None
    ):
        """
        Initialize a Track object.
        :param title: str
        :param artists: List[Artist]
        :param album: Album
        :param id: str
        :param url: str
        :param duration: int
        :param tags: List[Tag]
        """
        self.title = title
        self.artists = artists or []
        self.album = album
        self.id = id
        self.url = url
        self.duration = duration
        self.tags = tags or []

    # Getters
    def get_title(self):
        return self.title

    def get_artist(self) -> List[Artist]:
        return self.artists

    def get_album(self):
        return self.album

    def get_id(self):
        return self.id

    def get_url(self):
        return self.url

    def get_duration(self):
        return self.duration

    def get_tags(self):
        return self.tags

    # Setters
    def set_title(self, title: str):
        self.title = title

    def set_artist(self, artist: List[Artist]):
        self.artists = artist

    def add_artist(self, artist: Artist):
        if isinstance(artist, Artist):
            self.artists.append(artist)
        else:
            raise TypeError("artist must be an instance of Artist")

    def set_album(self, album: Album):
        self.album = album

    def set_id(self, id: str):
        self.id = id

    def set_url(self, url: str):
        self.url = url

    def set_duration(self, duration: int):
        self.duration = duration

    def set_tags(self, tags: List[Tag]):
        self.tags = tags

    def add_tag(self, tag: Tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def __repr__(self):
        return f"Track(title={self.title}, artist={self.artists}, album={self.album}, duration={self.duration})"