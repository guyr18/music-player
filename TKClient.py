import tkinter as tk
from AuthPage import AuthPage
from PlayListPage import PlayListPage
from PortalPage import PortalPage
from FavoritesPage import FavoritesPage
from Page import Page

"""

TKClient is derived from a tk.Tk object and is a wrapper for the root window.

"""

class TKClient(tk.Tk):

    """
    
    __init__(title, resizable, geom) takes the following three parameters:

        title -> A string representing the window title for this tk.Tk instance.
        resizable -> A boolean parameter that determines if this tk.Tk window instance
                     can be resized.
        geom -> A "WxH" formatted string representing the width and height dimensions of this tk.Tk window instance.
                For example, "500x500" is a valid input.

    """

    def __init__(self, title: str, resizable: bool = False, geom: str = None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.activeFrame = None

        if not resizable: self.resizable(False, False)

        try:
            self.geometry(geom)
        except tk.TclError as tce:
            print(tce)

        self.container.winfo_toplevel().title(title)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (AuthPage, PortalPage, PlayListPage, FavoritesPage):
            if F != None:
                frame = F(self.container)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky='nsew')
        self.showFrame(AuthPage)

    """
    
    ShowFrame(page) shows @param page to the user.

    """

    def showFrame(self, page: Page, *args):
        if page in self.frames:
            if self.activeFrame:
                self.activeFrame.destroy()
            frame = self.frames[page]
            self.activeFrame = frame
            if len(args) > 0:
                frame.layout(*args)
            else:
                frame.layout()
            frame.tkraise()