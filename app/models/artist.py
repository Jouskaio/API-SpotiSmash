from app.models.genre import Genre


class Artist:
    def __init__(self, name: str=None, genres: [Genre]= None, id: str = None, image: str = None):
        """
        Initialize an Artist object.
        :param name: str
        :param genres: Genre
        :param id: str
        :param image: str
        """
        self.image = image
        self.id = id
        self.name = name
        self.genres = genres if genres else []

    # Getters
    def get_name(self):
        """
        Get the name of the artist.
        :return: str
        """
        return self.name

    def get_genres(self):
        """
        Get the genre of the artist.
        :return: Genre
        """
        return self.genres

    def get_id(self):
        """
        Get the ID of the artist.
        :return: str
        """
        return self.id

    def get_image(self):
        """
        Get the image of the artist.
        :return: str
        """
        return self.image

    # Setters
    def set_name(self, name: str):
        """
        Set the name of the artist.
        :param name: str
        """
        self.name = name

    def set_genres(self, genre: Genre):
        """
        Set the genre of the artist.
        :param genre: Genre
        """
        self.genres = genre

    def set_id(self, id: str):
        """
        Set the ID of the artist.
        :param id: str
        """
        self.id = id

    def set_image(self, image: str):
        """
        Set the image of the artist.
        :param image: str
        """
        self.image = image

    def add_genre(self, genre: Genre):
        """
        Add a genre to the artist.
        :param genre: Genre
        """
        self.genres.append(genre)

    def __str__(self):
        return f"Artist: {self.name}, Genre: {self.genres}"