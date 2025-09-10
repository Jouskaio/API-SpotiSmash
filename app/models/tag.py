class Tag:
    def __init__(self, name: str):
        self.name = name

    def get_name(self):
        return self.name

    def __eq__(self, other):
        """
        Check if two Tag objects are equal based on their name.
        """
        return isinstance(other, Tag) and self.name == other.name

    def __hash__(self):
        """
        Hash function for the Tag object.
        This allows Tag objects to be used in sets and as dictionary keys.
        """
        return hash(self.name)

    def __repr__(self):
        return f"Tag({self.name})"