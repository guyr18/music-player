import tkinter as tk
import time, threading

class TimerText(tk.Label):

    """
    
    TimerText(parent, maxms) represents TimerText by deriving from a tk.Label instance. It
    enlists the following parameters:

        parent: A parent tk.Frame instance that this TimerText instance will be rendered onto.
        maxms: The maximum amount of time that we wish to count until (in milliseconds).

    """

    def __init__(self, parent : tk.Frame, maxms: int, bg: str = "#FFF"):
        super().__init__(parent)
        self.configure(text="0:00", bg=bg)
        self.maxms = maxms
        self.curSec = 0
        self.curMin = 0
        self.running = False
        self.curThreadId = 0

    """
    
    TimerThread(curms) is a method that is intended to run on a seperate thread of execution. Do not explicitly invoke
    this method. It handles timer computations and render updates.

    """

    def timerThread(self, curms: int, id: int) -> None:
        try:
            while self.running and curms < self.maxms:

                # If the id different from self.curThreadId, that means the timer was cleared. And we need to stop
                # making updates for this particular millisecond quantity and break the loop. The user is no longer
                # playing this song.
                if self.curThreadId != id: 
                    break

                time.sleep(1)
                curms += 1000
                mins = curms // 60000
                secs = (curms - (mins * 60000)) // 1000
                self.update(mins, secs)
                self.curMin, self.curSec = mins, secs

                if curms >= self.maxms: 
                    self.stop()
        except Exception:
            pass

    """
    
    Start() starts the timer for this TimerText instance. If it is already running (@see self.running),
    this method will do nothing.

    """

    def start(self) -> None:
        curms = (self.curSec * 1000) + ((self.curMin // 60) * 1000)
        if not self.running and curms < self.maxms:
            self.running = True
            thread = threading.Thread(target=self.timerThread, args=[curms, self.curThreadId])
            thread.start()
                
    """
    
    Update(mins, secs) updates the label for this TimerText instance. It takes
    the following parameters:

        mins: An integer representing the current minutes calculation.
        secs: An integer representing the current seconds calculation.

    """

    def update(self, mins: int, secs: int) -> None:
        strSecs = "0" + str(secs) if secs < 10 else str(secs)
        self.configure(text=f"{str(mins)}:{strSecs}")

    """
    
    Stop() stops the timer for this TimerText instance. If it is not currently running (@see self.running),
    this method will do nothing.

    """
    
    def stop(self) -> None:
        if self.running:
            self.running = False

    """
    
    Clear() clears the timer for this TimerText instance.

    """
    def clear(self) -> None:
        self.stop()
        self.update(0, 0)
        self.curSec = 0
        self.curMin = 0
        self.curThreadId += 1