import tkinter as tk
from typing import List, Literal, Any

class AudioControlButton(tk.Button):

    """
    
    __init__(parent, paths, default) is a three-parameter constructor and is defined as follows:

        parent -> The parent tk.Frame that invoked this instance.
        paths -> A two-element array containing two relative file path strings representing two discrete
                 icon states for this instance. For example, play/pause.
        default -> A literal string that can only be 'play' or 'pause'. This specifies the default icon
                   state this instance should render to.

    """
    
    def __init__(self, parent: tk.Frame, caller: Any, paths: List[str], default: Literal['play', 'pause'], bg: str = "#FFF"):
        super().__init__(parent)
        self.caller = caller
        self['bd'] = 0
        self['bg'] = bg
        self['highlightbackground'] = bg
        self['activebackground'] = bg
        self.paths = paths
        self.playing = True if default == 'play' else False
        self.paused = False
        self.update()

    """
    
    HandleClick() is an event listener for clicking this button.

    """

    def handleClick(self, *args) -> None:
        if self.playing:
            self.pause()
        else:
            self.play()
        self.update()

    """
    
    Update() updates the current image of this AudioControlButton instance.

    """

    def update(self) -> None:
        try:
            pathIndex = 1 if self.playing else 0
            self.photoImage = tk.PhotoImage(file=self.paths[pathIndex])
            self.configure(image=self.photoImage)
        except tk.TclError as tce:
            print(tce)

    """
    
    Play(invoke) will update the state of @see self.playing if it is false. And otherwise, will do nothing.
    If invoke is set to true, it will explicitly invoke AudioPlayerComponent.propogatePlay(). Otherwise,
    this method does not get invoked.

    """

    def play(self, invoke=True) -> None:
        if not self.playing:
            self.playing = True
            self.paused = False
            if self.caller and invoke:
                self.caller.propagatePlay(False)

    """
    
    Pause() will update the state of @see self.playing if it is true. And otherwise, will do nothing.

    """

    def pause(self) -> None:
        if self.playing:
            self.playing = False
            self.paused = True
            if self.caller:
                self.caller.propagatePause()