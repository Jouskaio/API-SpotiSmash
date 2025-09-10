class Genre:
    def __init__(self, name: str):
        self.name = name

    # Getters
    def get_name(self):
        """
        Get the name of the genre.
        :return: str
        """
        return self.name

    # Setters
    def set_name(self, name: str):
        """
        Set the name of the genre.
        :param name: str
        """
        self.name = name

    def __str__(self):
        return f"Genre: {self.name}"