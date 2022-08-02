import tkinter as tk
from PIL import Image
from Resources import Resources
from PlayListPage import PlayListPage
from typing import Any
import copy

class CoverArt(tk.Label):

    """
    
    __init__(parent, uri, image) takes the following three parameters:

        parent: A parent tk.Frame instance for invoking the base class constructor.
        uri: A string representing the URL of the graphic associated with this CoverArt instance.
        name: A string representing the name of the playlist that this CoverArt instance represents.
        desc: A string representing the description of the playlist that this CoverArt instance represents.
        image: A image representing the image that was loaded from @param uri.
        clickDisabled: A boolean flag that determining whether or not this CoverArt instance will 
                      listen for a click event.

    """
    def __init__(self, parent: tk.Frame, uri: str, name: str, desc: str, image: Image, caller: Any = None, clickDisabled: bool = False):
        super().__init__(parent)
        self.uri = uri
        self.name = name
        self.desc = desc
        self.image = image
        
        if caller: self.caller = caller

        self.configure(image=image)

        if not clickDisabled:
            self.bind("<Button-1>", self.handleClick)
            self.bind("<Enter>", self.handleHoverIn)
            self.bind("<Leave>", self.handleHoverOut)

    def handleClick(self, *args) -> None:
        Resources.TK_CLIENT.showFrame(PlayListPage, copy.deepcopy(self.uri))

    def handleHoverIn(self, *args) -> None:
        if self.caller:
            self.caller.propagateCoverArt(self.name, self.desc, False)

    def handleHoverOut(self, *args) -> None:
        if self.caller:
            self.caller.propagateCoverArt(self.name, self.desc, True)