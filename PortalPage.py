import tkinter as tk
from Page import Page
from Resources import Resources
from AudioPlayerComponent import AudioPlayerComponent
from FavoritesPage import FavoritesPage
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from io import BytesIO
from PIL import Image, ImageTk
from CoverArt import CoverArt
import requests
import AuthPage

class PortalPage(Page):

    """
    
    __init__(parent) takes one parameter, parent. Parent is a tk.Frame instance indicating
    the parent container for this PortalPage instance.

    """

    def __init__(self, parent):
        super().__init__(parent)

    """
    
    Layout() is an overridden abstract method intended to layout the UI components for this PortalPage instance.

    """

    def layout(self, *args):
        self.configure(background="#FFF")
        self.testLabel = tk.Label(text=f"Hello there, {Resources.ACTIVE_USER.nickname}! Pick a playlist to get started.", font=("SegoeUI 18 bold"))
        self.testLabel.configure(bg="#FFF")
        self.testLabel.place(relx=.45, rely=.25, anchor='center')
        self.widgets.append(self.testLabel)

        # If we are revisiting the portal page, we have a SpotifyClientCredentials object cached. If this is the first time,
        # create it.
        if not Resources.AUTH_MANAGER:
            Resources.AUTH_MANAGER = SpotifyClientCredentials(client_id='879dffc284a14c4d84c734e9d917ec6c', client_secret='ea63c7a8eff94acd96193b0a5077ab2e')

        # If we are revisiting the portal page, we have a spotipy.Spotify object cached. If this is the first time,
        # create it.
        if not Resources.SPOTIFY:
            Resources.SPOTIFY = spotipy.Spotify(auth_manager=Resources.AUTH_MANAGER)

        playlists = Resources.SPOTIFY.featured_playlists()['playlists']
        items = playlists['items']
        self.photoImages = []
        self.covers = []
        self.lastX = -1
        index, limit = 0, 3
        Resources.COVER_IDS = {}

        while index < limit:
            item = items[index]
            temp = requests.get(item['images'][0]['url'])
            Resources.COVER_IDS[item['images'][0]['url']] = item['id']
            raw = temp.content
            image = Image.open(BytesIO(raw)).resize((200, 200), Image.ANTIALIAS)
            self.photoImages.append(ImageTk.PhotoImage(image))
            self.covers.append(CoverArt(Resources.TK_CLIENT, item['images'][0]['url'], item['name'], item['description'], caller=self, image=self.photoImages[-1]))
            self.widgets.append(self.covers[-1])
            self.lastX = self.lastX + .3 if self.lastX != -1 else 0.2
            self.covers[-1].place(relx=self.lastX, rely=.5, anchor='center')
            index += 1

        # Initialize AudioPlayerComponent instance if needed. We first check the cache to see if we have an instance created.
        if not Resources.AUDIO_PLAYER_CMP:
            self.audioPlayerComponent = AudioPlayerComponent(Resources.TK_CLIENT, width=960, height=200)
            self.audioPlayerComponent.place(relx=.5, rely=0, anchor='center')
            Resources.AUDIO_PLAYER_CMP = self.audioPlayerComponent
        else:
            self.audioPlayerComponent = Resources.AUDIO_PLAYER_CMP

        # Initialize cover name label.
        self.coverNameLabel = tk.Label(text="", fg="#FFF", bg="#FFF", font=("SegoeUI 16 bold"))
        self.coverNameLabel.place(relx=0, rely=.73)
        self.widgets.append(self.coverNameLabel)

        # Initialize description label.
        self.descLabel = tk.Label(text="", bg="#FFF", fg="#000", font=("SegoeUI 10"))
        self.descLabel.place(relx=0.03, rely=.8)
        self.widgets.append(self.descLabel)

        # Initialize logout button
        self.logoutButton = tk.Button(Resources.TK_CLIENT, command=self.handleLogout, borderwidth=1, bg="purple", activebackground="#FF5733", activeforeground="#FFF", fg="#FFF", text="Logout", font=("SegoeUI", 12))
        self.logoutButton.place(width=120, relx=.9, rely=.25, anchor='center')
        self.widgets.append(self.logoutButton)

        # Initialize favorites button
        self.favoritesButton = tk.Button(Resources.TK_CLIENT, command=self.handleFavorites, borderwidth=1, bg="purple", activebackground="#FF5733", activeforeground="#FFF", fg="#FFF", text="Favorites", font=("SegoeUI", 12))
        self.favoritesButton.place(width=180, relx=.82, rely=.76, anchor='center')
        self.widgets.append(self.favoritesButton)

    """
    
    HandleFavorites() is an event handler that is triggerred when the favorites button is clicked.

    """

    def handleFavorites(self) -> None:
        Resources.TK_CLIENT.showFrame(FavoritesPage)

    """
    
    HandleLogout() is an event handler that is triggered when the logout button is clicked. It will perform cleanup
    and transition to the login frame.

    """
    
    def handleLogout(self) -> None:
        Resources.ACTIVE_USER = None
        Resources.AUDIO_PLAYER_CMP.destroy()
        Resources.AUDIO_PLAYER_CMP = None
        Resources.TK_CLIENT.showFrame(AuthPage.AuthPage)

    """

    PropagateCoverArt() hides or updates the cover art user interface components depending on the value of args[2].

    """

    def propagateCoverArt(self, *args) -> None:
        if args[2] == True:
            self.coverNameLabel.configure(text="", bg="#FFF")
            self.descLabel.configure(text="")
        else:
            self.coverNameLabel.configure(text=args[0], bg="#FF5733")
            self.descLabel.configure(text=args[1])

    """

    Destroy() is an overridden method intended to deallocate and remove the UI components for this PortalPage instance.

    """

    def destroy(self):
        super().destroy()