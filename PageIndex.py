import tkinter as tk
import Page

class PageIndex(tk.Button):

    """
    
    __init__(parent, caller, width, height, text, bg, fg) accepts the following parameters:

        parent: A tk.Frame instance representing the parent of this PageIndex instance.
        caller: The Page instance that instantiated this PageIndex instance.
        width: An integer representing the width of this PageIndex instance.
        height: An integer representing the height of this PageIndex instance.
        text: A string representing the default text for this PageIndex instance; i.e.: the index or page number.
        bg: A hexadecimal string representing the default background color of this PageIndex instance.
        fg: A hexadecimal string representing the default foreground color of this PageIndex instance.

    """

    def __init__(self, parent: tk.Frame, caller: Page.Page, width: int, height: int, text:str, bg="#FFF", fg="purple"):
        super().__init__(parent)
        self.caller = caller
        self.configure(text=text, width=width, height=height, font=("SegoeUI 10 bold"), bg=bg, fg=fg)
        self.active = False
        self.bind("<Button-1>", self.handleClick)
     
    """
    
    Activate() sets @self.active to true if it is currently false. It also updates the background and
    foreground of this PageIndex instance accordingly. If @self.active is currently true, it returns
    the function address.

    """

    def activate(self) -> None:
        if self.active: return

        self.active = True
        self.configure(bg="purple", fg="#FFF")

    """
    
    Deactivate() sets @self.active to false if it is currently true. It also updates the background and
    foreground of this PageIndex instance accordingly. If @self.ative is currently false, it returns the
    function address.

    """

    def deactivate(self) -> None:
        if not self.active: return
        
        self.active = False
        self.configure(bg="#FFF", fg="purple")

    """
    
    HandleClick() is an event-binding that is executed when this PageIndex instance is clicked.

    """

    def handleClick(self, *args) -> None:
        self.activate()
        self.caller.unselectPagesExcept(self)
        intIndex = int(self['text'])
        self.caller.renderPageByIndex(intIndex - 1)
        