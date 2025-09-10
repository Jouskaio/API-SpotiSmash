from app.models.track import Track


class Playlist:
    def __init__(self, name, tracks : [Track] =None, genres=None, id=None):
        """
        Initialize a Playlist object.
        :param name: str
        :param tracks: List of tracks
        :param genres: List of genres
        """
        if genres is None:
            genres = []
        if tracks is None:
            tracks = []
        self.name = name
        self.tracks = tracks
        self.genres = genres
        self.id = id

    # Getters
    def get_name(self):
        """
        Get the name of the playlist.
        :return: str
        """
        return self.name

    def get_tracks(self):
        """
        Get the tracks in the playlist.
        :return: List of tracks
        """
        return self.tracks

    def get_genres(self):
        """
        Get the genres of the playlist.
        :return: List of genres
        """
        return self.genres

    def get_id(self):
        """
        Get the URL of the playlist.
        :return: str
        """
        return self.id

    # Setters
    def set_name(self, name):
        """
        Set the name of the playlist.
        :param name: str
        """
        self.name = name

    def set_tracks(self, tracks):
        """
        Set the tracks in the playlist.
        :param tracks: List of tracks
        """
        self.tracks = tracks

    def set_genres(self, genres):
        """
        Set the genres of the playlist.
        :param genres: List of genres
        """
        self.genres = genres

    def set_id(self, id):
        """
        Set the URL of the playlist.
        :param url: str
        """
        self.id = id

    def __str__(self):
        return f"Playlist: {self.name}, ID: {self.id}, Tracks: {self.tracks}, Genres: {self.genres}"