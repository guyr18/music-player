import tkinter as tk
from Page import Page
from Resources import Resources
from PageIndex import PageIndex
from PlayListEntry import PlayListEntry
from json import loads
import PortalPage
import math

class FavoritesPage(Page):

    ITEMS_PER_PAGE = 13
    PAGE_CAPACITY = 5

    """
    
    __init__(parent) takes one parameter, parent. Parent is a tk.Frame instance indicating
    the parent container for this FavoritesPage instance.

    """

    def __init__(self, parent: tk.Frame):
        super().__init__(parent)
        self.configure(bg="#FFF")

    """
    
    Layout() is an overridden abstract method intended to layout the UI components for this PortalPage instance.

    """

    def layout(self, *args) -> None:

        # Place AudioPlayerComponent.
        self.audioPlayerComponent = Resources.AUDIO_PLAYER_CMP
        self.audioPlayerComponent.place()
        self.audioPlayerComponent.place(relx=.5, rely=0, anchor='center')
        
        # Screen label.
        self.screenLabel = tk.Label(text="Your Favorites", bg="#FFF", font=("SegoeUI 18 bold"))
        self.screenLabel.place(relx=0.05, rely=.2)
        self.widgets.append(self.screenLabel)

        # Go back button
        self.goBackButton = tk.Button(Resources.TK_CLIENT, command=lambda: Resources.TK_CLIENT.showFrame(PortalPage.PortalPage), borderwidth=1, bg="purple", activebackground="#FF5733", activeforeground="#FFF", fg="#FFF", text="Go Back", font=("SegoeUI", 12))
        self.goBackButton.place(width=200, relx=.4, rely=.22, anchor='center')
        self.widgets.append(self.goBackButton)

        self.entries = []
        prefix = "favorite:*:*"
        self.favorites = list(Resources.REDIS_DB.redisStdGetAll_StartingWith(prefix))
        pagesNeeded = 0
        self.pageItems = []
        lastX = 0.0

        if self.favorites != []:
            self.lengthOfFavorites = len(self.favorites)
            if self.lengthOfFavorites <= FavoritesPage.ITEMS_PER_PAGE:
                pagesNeeded = 1
            else:
                pagesNeeded = math.ceil(self.lengthOfFavorites / FavoritesPage.ITEMS_PER_PAGE)
        else:
            self.alertLabel = tk.Label(Resources.TK_CLIENT, text="You have no favorites currently!", font=("SegoeUI 12 bold"), bg="#FFF")
            self.alertLabel.place(relx=.21, rely=.30, anchor='center')
            self.widgets.append(self.alertLabel)

        for i in range(pagesNeeded):
            if i == FavoritesPage.PAGE_CAPACITY - 1:
                break
            pageIndex = i + 1
            newPageIndex = PageIndex(Resources.TK_CLIENT, self, 1, 1, str(pageIndex))
            self.pageItems.append(newPageIndex)
            if pageIndex == 1:
                self.pageItems[-1].activate()
            lastX = lastX + 0.05
            self.pageItems[-1].place(relx=lastX, rely=.95, anchor='center')
            self.widgets.append(self.pageItems[-1])

        if pagesNeeded > 0:
            self.renderPageByIndex(0)

    """
    
    RenderPageByIndex(index) performs cleanup on the current list of PageIndex instances (@see self.entries). Additionally,
    it renders the new list of PageIndex instances based on @param index.

    """

    def renderPageByIndex(self, index: int) -> None:
        if index < 0 or index >= self.lengthOfFavorites: return
    
        for entry in self.entries:
            if entry is not None:
                entry.destroy()
            self.entries = []

        # 14
        startIndex = index * FavoritesPage.ITEMS_PER_PAGE
        endIndex = startIndex + FavoritesPage.ITEMS_PER_PAGE
        print(startIndex, endIndex)
        lastY = -1

        while startIndex < endIndex:
            if startIndex >= self.lengthOfFavorites: break
            
            key = self.favorites[startIndex]
            data = loads(Resources.REDIS_DB.redisStdGet(key))
            title = data['name']
            uri = f"spotify:track:{data['id']}"
            entry = PlayListEntry(self, 300, 25, "#FFF", title, title, "", "", uri)
            self.entries.append(entry)
            self.widgets.append(entry)
            lastY = .28 if lastY == -1 else lastY + 0.05
            self.entries[-1].pack(side=tk.TOP)
            self.entries[-1].place(relx=.9, rely=lastY, anchor='center')
            self.entries[-1].render(lastY, [.15, 1.0, 1.0])
            startIndex += 1

    """
    
    UnselectOtherEntries() modifies the foreground color of all members of @see self.entries except @param exclude.
    This makes @param exclude appear selected, while the others are not.

    """

    def unselectOtherEntries(self, exclude: PlayListEntry) -> None:
        for entry in self.entries:
            if entry != exclude:
                entry.titleLabel.configure(fg="#000", font=("SegoeUI", 10))
                entry.artistLabel.configure(fg="#000", font=("SegoeUI", 10))
                entry.durationLabel.configure(fg="#000", font=("SegoeUI", 10))
                self.selected = False

    """
    
    UnselectPagesExcept(exclude) unselects all pages except for @param exclude.

    """

    def unselectPagesExcept(self, exclude: PageIndex) -> None:
        for page in self.pageItems:
            if page != exclude and page.active:
                page.deactivate()
