import tkinter as tk

class PlaceholderEntry(tk.Entry):

    def __init__(self, placeholder=None, master=None, textColor="#FFF"):
        super().__init__(master)
        self.placeholder = placeholder
        self.placeholderColor = textColor
        self.defaultTextColor = self['fg']

        # Bind events
        self.bind("<FocusIn>", self.handleFocusIn)
        self.bind("<FocusOut>", self.handleFocusOut)

    """
    
    ApplyPlaceHolder() updates the content of this PlaceHolderEntry instance to @see self.placeholder and the
    corresponding foreground text color to @see self.placeholderColor.

    """

    def applyPlaceholder(self):
        self.insert(0, '  ' + self.placeholder)
        self['fg'] = self.placeholderColor

    """
    
    HandleFocusIn() is an event-binding that executes when this PlaceHolderEntry instance is focused ini.

    """

    def handleFocusIn(self, *args):
        if self['fg'] == self.placeholderColor:
            self.delete('0', 'end')
            self['fg'] = self.defaultTextColor

    """
    
    HandleFocusOut() is an event-binding that executes when this PlaceHolderEntry instance is focused out.

    """
    
    def handleFocusOut(self, *args):
        if not self.get():
            self.applyPlaceholder()

