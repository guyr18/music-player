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

    def applyPlaceholder(self):
        self.insert(0, '  ' + self.placeholder)
        self['fg'] = self.placeholderColor

    def handleFocusIn(self, *args):
        if self['fg'] == self.placeholderColor:
            self.delete('0', 'end')
            self['fg'] = self.defaultTextColor

    def handleFocusOut(self, *args):
        if not self.get():
            self.applyPlaceholder()

