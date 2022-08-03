import tkinter as tk
from AudioControlButton import AudioControlButton
from TimerText import TimerText
from pygame import mixer
import Song
from mutagen.mp3 import MP3
from Resources import Resources
from typing import Tuple
from json import dumps

"""

AudioPlayerComponent derives from a tk.Canvas object and represents the entire
audio player UI component / area. It encapsulates other components that can
be regarded as sub-functionality such as play, pause, progress bar, timer text, and
other important components.

"""

class AudioPlayerComponent(tk.Canvas):

    """
    
    __init__(parent, width, height, bg) accepts the following four parameters:

        parent: A inheriting Tk.Frame instance that operates as a base class.
        width: An integer representing the width of this AudioPlayerComponent object.
        height: An integer representing the height of this AudioPlayerComponent object.
        bg: A hexadecimal string representing the background color of this AudioPlayerComponent object (or tk.Canvas).

    """

    def __init__(self, parent: tk.Frame, width: int, height: int, bg: str = "#FFF"):
        super().__init__(parent)
        self.configure(bg=bg, width=width, height=height)
        self.widgets = []
        self.curSong = None
        self.lastPositionSaved = -1.0
        self.favoriteButton = None
        self.isFavorited = False
        mixer.init()

        # Audio Control Button (play / pause)
        self.audioControlButton = AudioControlButton(parent, self, ["images/play.png", "images/pause.png"], "pause")
        self.audioControlButton.place(relx=0.08, rely=0.08, anchor='center')
        self.widgets.append(self.audioControlButton)

        # Timer countdown text
        self.timerText = TimerText(parent, 10000)
        self.timerText.place(relx=0.35, rely=0.08, anchor='center')
        self.widgets.append(self.timerText)

        # Timer end goal text
        self.timerEndGoalText = tk.Label(parent, bg="#FFF", text="0:00")
        self.timerEndGoalText.place(relx=0.41, rely=0.08, anchor='center')
        self.timerText.tkraise(self.timerEndGoalText)
        self.widgets.append(self.timerEndGoalText)

        # Track text
        self.trackText = tk.Label(parent, text="No track currently selected.", bg="#FFF", fg="purple", font=("SegoeUI 12 bold"))
        self.trackText.place(relx=.70, rely=0.08, anchor='center')
        self.widgets.append(self.trackText)
    

    """
    
    SetSong(song) sets @see self.curSong to a new Song instance, song.

    """

    def setSong(self, song: Song.Song) -> None:
        mixer.music.stop()
        self.lastPositionSaved = -1.0
        self.timerText.clear()
        self.curSong = song
        if self.audioControlButton is not None:
            self.audioControlButton.bind("<Button>", self.audioControlButton.handleClick)
        self.isFavorited = Resources.REDIS_DB.redisStdGet(f"favorite:{self.curSong.id}:{Resources.ACTIVE_USER.email}")
        path = "images/heartnofill.png" if self.isFavorited is None else "images/heartfill.png"
        self.favoriteButtonImage = tk.PhotoImage(file=path)
        if self.favoriteButton is None:
            self.favoriteButton = tk.Label(Resources.TK_CLIENT, image=self.favoriteButtonImage, bd=0)
            self.favoriteButton.place(relx=0.16, rely=0.08, anchor='center')
            self.favoriteButton.bind("<Button-1>", self.handleFavoriteClick)
            self.widgets.append(self.favoriteButton)
        else:
            self.favoriteButton.configure(image=self.favoriteButtonImage)
        if self.isFavorited:
            self.curSong.favorite()
        else:
            self.curSong.unfavorite()

    """
    
    HandleFavoriteClick() is an event-binding that is executed when the favorites button is clicked. It manages
    back-end interaction with the Redis datastore by adding / deleting favorite keys as needed.

    """

    def handleFavoriteClick(self, *args) -> None:
        key = f"favorite:{self.curSong.id}:{Resources.ACTIVE_USER.email}"
        if not self.isFavorited:
            value = dumps(self.curSong.__dict__)
            Resources.REDIS_DB.redisStdSet(key, value)
            print("Added {key} as new favorite to redis datastore.")
            self.favoriteButtonImage.configure(file="images/heartfill.png")
            self.favoriteButton.configure(image=self.favoriteButtonImage)
            self.curSong.favorite()
        else:
            print("Removing {self.curSong.id} from redis datastore.")
            Resources.REDIS_DB.redisStdDel(key)
            self.favoriteButtonImage.configure(file="images/heartnofill.png")
            self.favoriteButton.configure(image=self.favoriteButtonImage)
            self.curSong.unfavorite()
        self.isFavorited = self.curSong.favorited

    """
    
    PropagatePlay() invokes the correct mixer.music functions to play or unpause the currently selected
    song.

    """

    def propagatePlay(self, switchSong) -> None:
        if self.curSong:            
            if self.audioControlButton.playing and not self.audioControlButton.paused and not switchSong:
                mixer.music.rewind()
                mixer.music.play(start=self.lastPositionSaved)

            else:
                mixer.music.load("sounds/" + self.curSong.uri)
                mixer.music.set_volume(.5)
                mixer.music.play()
                self.timerText.clear()
            
            durationData = self.getDurationString(f"sounds/{self.curSong.uri}")
            self.updateTrackText(self.curSong.name)
            self.updateTimerText(durationData[1])
            self.audioControlButton.play(invoke=False)
            self.audioControlButton.update()
            self.timerText.maxms = int((durationData[0] - 1) * 1000)
            self.timerText.start()

    """ 
    
    GetDurationString(path) returns a tuple of (int, str) where the first member represents
    the duration of the MP3 file lothcated at sounds/path and the second member represents
    the formatted duration string (m:ss); m is a single digit string representing minutes
    and ss is a two-digit string representing seconds.

    """

    def getDurationString(self, path: str) -> Tuple:
        duration = MP3(path).info.length
        mins = int(duration // 60)
        secs = int(duration - (mins * 60))
        strSecs = "0" + str(secs) if secs < 10 else str(secs)
        return (duration, f"{str(mins)}:{strSecs}")

    """
    
    UpdateTimerText(newText) sets the content of @see self.timerEndGoalText to newText.

    """
    
    def updateTimerText(self, newText: str) -> None:
        self.timerEndGoalText.configure(text=newText)

    """
    
    UpdateTrackText(newText, asError) sets the content of @see self.trackText to newText. The asError
    parameter is optional and will set the foreground color of the label to red to indicate that it
    is an error.

    """

    def updateTrackText(self, newText: str, asError=False) -> None:
        if not asError:
            self.trackText.configure(text=newText, fg="purple")
        else:
            self.trackText.configure(text=newText, fg="red")

    """
    
    PropagatePause() pauses the current song, if their is one; @see self.curSong.

    """

    def propagatePause(self) -> None:
        if self.curSong:
            print(f"Pausing {self.curSong.uri}")
            self.lastPositionSaved = self.lastPositionSaved + (mixer.music.get_pos() // 1000.0)
            print(self.lastPositionSaved)
            mixer.music.pause()
            self.timerText.stop()

    """
    
    Destroy() will destroy all widgets found in this tk.Frame instance.

    """

    def destroy(self) -> None:
        for widget in self.widgets:
            if widget:
                widget.destroy()
        mixer.music.stop()
        super().destroy()