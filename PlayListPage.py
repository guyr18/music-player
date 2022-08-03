import tkinter as tk
from Page import Page
from PlayListEntry import PlayListEntry
import PortalPage
from Resources import Resources
from PIL import ImageTk, Image
from io import BytesIO
import CoverArt
import requests

class PlayListPage(Page):

    
    MAX_ITEMS = 15

    """
    
    __init__(parent) takes one parameter, parent. Parent is a tk.Frame instance indicating
    the parent container for this PlayListPage instance.

    """
    
    def __init__(self, parent: tk.Frame):
        super().__init__(parent)
        self.configure(bg="#FFF")

    """
    
    Layout() is an overridden abstract method intended to layout the UI components for this PlayListPage instance.

    """

    def layout(self, *args) -> None:
        
        print("laywe")
        self.audioPlayerComponent = Resources.AUDIO_PLAYER_CMP
        temp = requests.get(args[0])
        raw = temp.content
        self.image = ImageTk.PhotoImage(Image.open(BytesIO(raw)).resize((350, 350), Image.ANTIALIAS))
        self.cover = CoverArt.CoverArt(Resources.TK_CLIENT, args[0], None, None, self.image, clickDisabled=True)
        self.cover.place(relx=.25, rely=.55, anchor='center')
        self.widgets.append(self.cover)
        self.entries = []
        id = Resources.COVER_IDS[args[0]]
        items = Resources.SPOTIFY.playlist(id)['tracks']['items']
        lastY = -1

        for i in range(0, PlayListPage.MAX_ITEMS):
            track = items[i]['track']
            artists = track['artists']
            strUri = track['uri']
            strName = track['name'] if len(track['name']) <= 18 else track['name'][:22] + ".."
            strArtist = artists[0]['name']
            duration = int(track['duration_ms'])
            mins = duration // 60000
            secs = (duration - (mins * 60000)) // 1000
            strSecs = "0" + str(secs) if secs < 10 else str(secs)
            strDuration = f"{str(mins)}:{strSecs}"
            self.entries.append(PlayListEntry(self, 460, 25, "#FFF", strName, track['name'], strArtist, strDuration, strUri))
            lastY = .25 if lastY == -1 else lastY + 0.05
            self.entries[-1].pack(side=tk.TOP)
            self.entries[-1].place(relx=.78, rely=lastY, anchor='center')
            self.entries[-1].render(lastY)

        # Title header     
        self.titleLabel = tk.Label(text="Title", font=("SegoeUI 12 bold"), bg="#FFF") 
        self.titleLabel.place(relx=.55, rely=.2, anchor='center')
        self.widgets.append(self.titleLabel)

        # Artist header
        self.artistLabel = tk.Label(text="Artist", font=("SegoeUI 12 bold"), bg="#FFF")
        self.artistLabel.place(relx=.74, rely=.2, anchor='center')
        self.widgets.append(self.artistLabel)

        # Duration header
        self.durationLabel = tk.Label(text="Duration", font=("SegoeUI 12 bold"), bg="#FFF")
        self.durationLabel.place(relx=.93, rely=.2, anchor='center')    
        self.widgets.append(self.durationLabel)

        # Go back button
        self.goBackButton = tk.Button(Resources.TK_CLIENT, command=lambda: Resources.TK_CLIENT.showFrame(PortalPage.PortalPage), borderwidth=1, bg="purple", activebackground="#FF5733", activeforeground="#FFF", fg="#FFF", text="Go Back", font=("SegoeUI", 12))
        self.goBackButton.place(width=200, relx=.26, rely=.22, anchor='center')
        self.widgets.append(self.goBackButton)

    """
    
    UnselectOtherEntries() modifies the foreground color of all members of @see self.entries except @param exclude.
    This makes @param exclude appear selected, while the others are not.

    """

    def unselectOtherEntries(self, exclude: PlayListEntry) -> None:
        for entry in self.entries:
            if entry != exclude:
                entry.titleLabel.configure(fg="#000", font=("SegoeUI", 10))
                entry.artistLabel.configure(fg="#000", font=("SegoeUI", 10))
                entry.durationLabel.configure(fg="#000", font=("SegoeUI", 10))
                self.selected = False

    """

    Destroy() is an overridden method intended to deallocate and remove the UI components for this PlayListPage instance.

    """

    def destroy(self) -> None:
        try:
            for widget in self.widgets:
                if widget:
                    widget.destroy()
            for entry in self.entries:
                if entry:
                    entry.destroy()
        except Exception:
            pass
        self.widgets = []