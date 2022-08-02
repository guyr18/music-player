class Song:

    def __init__(self, id: int , name: str, uri: str, favorited: bool):
        self.id = id
        self.name = name
        self.uri = uri
        self.favorited = favorited

    def favorite(self):
        if not self.favorited:
            self.favorited = True
    
    def unfavorite(self):
        if self.favorited:
            self.favorited = False