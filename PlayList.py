from Song import Song
from typing import Set

class PlayList:

    def __init__(self, songs: Set[Song]):
        self.songs = set()

    def addSong(self, song):
        self.songs.add(song)

    def removeSong(self, song):
        self.songs.discard(song)

