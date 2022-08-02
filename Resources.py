from abc import ABC

"""

Resources is intended to operate as a statically defined class that will manage
several differenct class instances through the application lifetime.

"""
class Resources(ABC):

    REDIS_DB = None # RedisWrapper instance reference.
    TK_CLIENT = None # TKClient instance reference.
    ACTIVE_USER = None # User instance reference; the currently logged in user.
    COVER_IDS = None # Cover IDs to be referred to when viewing a specific cover.
    AUTH_MANAGER = None # SpotifyClientCredentials instance.
    SPOTIFY = None # spotipy.Spotify instance.
    AUDIO_PLAYER_CMP = None # AudioPlayerComponent instance.