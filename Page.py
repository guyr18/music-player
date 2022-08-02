import tkinter as tk
from abc import ABC, abstractmethod

"""

Page is an abstract class that derives from a tk.Frame. It is intended
to modularize a standard screen component.

"""
class Page(ABC, tk.Frame):

    def __init__(self, parent: tk.Frame):
        super().__init__(parent)
        self.widgets = []

    """
    
    Layout(*args) is an abstract method that must be overridden in children classes.
    It is intended to serve as an area for allocating UI components to the deriving
    instance.
    """
    @abstractmethod
    def layout(self, *args) -> None:
        pass

    """
    
    Destroy() invokes the .destroy() method on all children of @see self.widgets.
    """
    def destroy(self) -> None:
        for widget in self.widgets:
            if widget:
                widget.destroy()

