from typing import List, Optional
from app.models.artist import Artist

class Album:
    def __init__(
        self,
        title: str,
        artists: Optional[List[Artist]] = None,
        release_year: Optional[str] = None,
        id: Optional[str] = None,
        image: Optional[str] = None
    ):
        self.image = image
        self.id = id
        self.title = title
        self.artists = artists or []
        self.release_year = release_year

    # Getters
    def get_title(self):
        return self.title

    def get_artists(self) -> List[Artist]:
        return self.artists

    def get_release_year(self):
        return self.release_year

    def get_id(self):
        return self.id

    def get_image(self):
        return self.image

    # Setters
    def set_title(self, title: str):
        self.title = title

    def set_artists(self, artists: List[Artist]):
        self.artists = artists

    def add_artist(self, artist: Artist):
        if isinstance(artist, Artist):
            self.artists.append(artist)
        else:
            raise TypeError("artist must be an instance of Artist")

    def set_release_year(self, release_year: str):
        self.release_year = release_year

    def set_id(self, id: str):
        self.id = id

    def set_image(self, image: str):
        self.image = image

    def __repr__(self):
        return f"Album(title={self.title}, artists={self.artists}, release_year={self.release_year})"