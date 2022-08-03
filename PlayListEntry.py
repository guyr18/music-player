import tkinter as tk
from Resources import Resources
from Song import Song
from typing import List
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
    
    VerifyComponents() verifies that the widgets of this component still exist and have not been garbage collected. If they
    have been garbage collected, instances are recreated.

    """
    
    def verifyComponents(self) -> None:
        if not self.titleLabel:
            self.titleLabel = tk.Label(text=self.title, bg=self.bg, font=("SegoeUI", 10))
        if not self.artistLabel:
            self.artistLabel = tk.Label(text=self.artist, bg=self.bg, font=("SegoeUI", 10))
        if not self.durationLabel:
            self.durationLabel = tk.Label(text=self.duration, bg=self.bg, font=("SegoeUI", 10))

    """
    
    OnClick() is an event binding that executes when this PlayListEntry object is clicked.

    """

    def onClick(self, *args) -> None:

        self.verifyComponents()

        if self.selected == True: return
        
        print(f"here={self.uri}")
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

        if not os.path.isdir("sounds"):
            os.makedirs("sounds")

        with open(os.path.join("sounds", slice), 'wb') as f:
            f.write(binary)

        Resources.AUDIO_PLAYER_CMP.setSong(Song(result['id'], self.fullTitle, slice, False))
        Resources.AUDIO_PLAYER_CMP.propagatePlay(True)

    """
    
    OnHoverIn() is an event-binding that executes when this PlayEntryList object is hovered.

    """

    def onHoverIn(self, *args) -> None:
        if not self.selected:
            self.verifyComponents()
            self.titleLabel.configure(fg="purple", font=("SegoeUI 10 bold"))
            self.artistLabel.configure(fg="purple", font=("SegoeUI 10 bold"))
            self.durationLabel.configure(fg="purple", font=("SegoeUI 10 bold"))

    """
    
    OnHoverOut() is an event-binding that executes when this PlayEntryList object loses its hover.

    """
    
    def onHoverOut(self, *args) -> None:
        if not self.selected:
            self.verifyComponents()
            self.titleLabel.configure(fg="#000", font=("SegoeUI", 10))
            self.artistLabel.configure(fg="#000", font=("SegoeUI", 10))
            self.durationLabel.configure(fg="#000", font=("SegoeUI", 10))

    """
    
    Render(rely, relx) is a helper method for setting absolute positioning, given a dynamic list. Relx
    is a default parameter specifying three lists of floats. These values should range from 0 to 1 and
    may be used to override the default x coordinate placement.

    """

    def render(self, rely: int,  relx: List[float] = None) -> None:

        xs = [.55, .74, .93] if relx == None else relx
        self.verifyComponents()
        self.titleLabel.place(relx=xs[0], rely=rely, anchor='center')
        self.artistLabel.place(relx=xs[1], rely=rely, anchor='center')
        self.durationLabel.place(relx=xs[2], rely=rely, anchor='center')
    
    """
    
    Destroy() destroys all UI components of this PlayListEntry object.

    """

    def destroy(self) -> None:
        self.titleLabel.destroy()
        self.artistLabel.destroy()
        self.durationLabel.destroy()