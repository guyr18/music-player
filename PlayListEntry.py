import tkinter as tk
from Resources import Resources
from Song import Song
import requests
import os

class PlayListEntry(tk.LabelFrame):

    """
    
    __init__(parent, w, h, bg, title, fullTitle, artist, duration, uri) takes various parameters that will be documented below:

        parent: The parent Tk.Frame instance of this PlayListEntry object.
        w: An integer representing the width of this PlayListEntry object.
        h: An integer representing the height of this PlayListEntry object.
        bg: A hexadecimal string that represents the background color of this PlayListEntry object.
        title: A string representing the truncated title of this PlayListEntry object. This is needed to fit the text within the dimensions of the UI.
        fullTitle: A string representing the non-truncated title of this PlayListEntryObject.
        artist: A string representing the artist of this PlayListEntryObject (or this song).
        uri: A string representing the URI of this PlayListEntryObject (or this song).

    """

    def __init__(self, parent: tk.Frame, w: int, h: int, bg: str, title: str, fullTitle: str, artist: str, duration: str, uri: str):
        super().__init__(parent)
        self.parent = parent
        self.bg = bg
        self['bd'] = 0
        self.configure(bg=bg, width=w, height=h)
        self.title = title
        self.fullTitle = fullTitle
        self.artist = artist
        self.duration = duration
        self.titleLabel = tk.Label(text=title, bg=bg, font=("SegoeUI", 10))
        self.artistLabel = tk.Label(text=artist, bg=bg, font=("SegoeUI", 10))
        self.durationLabel = tk.Label(text=duration, bg=bg, font=("SegoeUI", 10))
        self.uri = uri
        self.selected = False

        for obj in (self, self.titleLabel, self.artistLabel, self.durationLabel):
            obj.bind("<Button-1>", self.onClick)
            obj.bind("<Enter>", self.onHoverIn)
            obj.bind("<Leave>", self.onHoverOut)

    """
    
    OnClick() is an event binding that executes when this PlayListEntry object is clicked.

    """

    def onClick(self, *args) -> None:

        if self.selected: return
        
        result = Resources.SPOTIFY.track(self.uri)
        previewURL = result['preview_url'] 
        if previewURL is None:
            Resources.AUDIO_PLAYER_CMP.updateTrackText("Sorry! This track is down. Try a different one.", True)
            return

        if self.parent != None: self.parent.unselectOtherEntries(self)
        
        self.selected = True
        self.titleLabel.configure(fg="purple", font=("SegoeUI 10 bold"))
        self.artistLabel.configure(fg="purple", font=("SegoeUI 10 bold"))
        self.durationLabel.configure(fg="purple", font=("SegoeUI 10 bold"))
        binary = requests.get(previewURL).content
        slice = previewURL[35:] + '.mp3'

        with open(os.path.join("sounds", slice), 'wb') as f:
            f.write(binary)

        Resources.AUDIO_PLAYER_CMP.setSong(Song(result['id'], self.fullTitle, slice, False))
        Resources.AUDIO_PLAYER_CMP.propagatePlay()

    """
    
    OnHoverIn() is an event-binding that executes when this PlayEntryList object is hovered.

    """

    def onHoverIn(self, *args) -> None:

        if not self.selected:
            self.titleLabel.configure(fg="purple", font=("SegoeUI 10 bold"))
            self.artistLabel.configure(fg="purple", font=("SegoeUI 10 bold"))
            self.durationLabel.configure(fg="purple", font=("SegoeUI 10 bold"))

    """
    
    OnHoverOut() is an event-binding that executes when this PlayEntryList object loses its hover.

    """
    
    def onHoverOut(self, *args) -> None:
        if not self.selected:
            self.titleLabel.configure(fg="#000", font=("SegoeUI", 10))
            self.artistLabel.configure(fg="#000", font=("SegoeUI", 10))
            self.durationLabel.configure(fg="#000", font=("SegoeUI", 10))

    """
    
    Render(rely) is a helper method for setting absolute positioning, given a dynamic list.

    """

    def render(self, rely: int) -> None:
        self.titleLabel.place(relx=.55, rely=rely, anchor='center')
        self.artistLabel.place(relx=.74, rely=rely, anchor='center')
        self.durationLabel.place(relx=.93, rely=rely, anchor='center')
    
    """
    
    Destroy() destroys all UI components of this PlayListEntry object.

    """

    def destroy(self) -> None:
        self.titleLabel.destroy()
        self.artistLabel.destroy()
        self.durationLabel.destroy()