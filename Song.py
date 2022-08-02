class Song:

    """

    __init__(id, name, uri, favorited) takes the following 4 parameters:

        id: A string representing the unique identifier for this Song instance.
        name: A string representing the name of this Song instance.
        uri: A string representing the URI that this Song instance can be located at.
        favorited: A boolean value that represents if this Song is marked as favorited 
                   for the currently logged in user.

    """

    def __init__(self, id: str , name: str, uri: str, favorited: bool):
        self.id = id
        self.name = name
        self.uri = uri
        self.favorited = favorited

    """
    
    Favorite() marks @see self.favorited to true if it is false. And otherwise, does nothing.

    """

    def favorite(self):
        if not self.favorited:
            self.favorited = True
    
    """
    
    Unfavorite() marks @see self.favorited to false if it is true. And otherwise, does nothing.

    """
    
    def unfavorite(self):
        if self.favorited:
            self.favorited = False