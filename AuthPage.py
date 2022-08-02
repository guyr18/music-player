import tkinter as tk
from PlaceholderEntry import PlaceholderEntry
from PasswordPlaceholderEntry import PasswordPlaceholderEntry
from Resources import Resources
from User import User
from hashlib import md5
from json import dumps, loads
from PortalPage import PortalPage
from Page import Page

class AuthPage(Page):

    """
    
    __init__(parent) takes one parameter, parent. Parent is a tk.Frame instance indicating
    the parent container for this AuthPage instance.
    """
    def __init__(self, parent: tk.Frame):
        super().__init__(parent)

    """
    
    Layout(*args) is an overridden abstract method intended to layout the UI components for this AuthPage instance.
    """
    def layout(self, *args):

        # Setup UI
        self.configure(background="#FFF")

        # App name.
        self.title = tk.Label(text="Play It!", font=("SegoeUI", 36), bg="#FFF", fg="purple")
        self.title.place(relx=.5, rely=0.15, anchor='center')
        self.widgets.append(self.title)

        # Login container
        self.loginContainer = tk.Canvas(Resources.TK_CLIENT, width=450, height=350, bg="#FFF")
        self.loginContainer.place(relx=.5, rely=.5, anchor='center')
        self.widgets.append(self.loginContainer)

        # Login prompt.
        self.prompt = tk.Label(text="Please enter your login details", font=("SegoeUI", 12), bg="#FFF", fg="#CCC")
        self.prompt.place(relx=.5, rely=0.29, anchor='center')
        self.widgets.append(self.prompt)

        # Username prompt.
        self.promptUser = tk.Label(text="Email Address", font=("SegoeUI", 10), bg="#FFF", fg="purple")
        self.promptUser.place(relx=.38, rely=0.35, anchor='center')
        self.widgets.append(self.promptUser)

        # Email text box
        self.emailEntry = PlaceholderEntry(placeholder="<Enter email address>", master=Resources.TK_CLIENT, textColor="#CCC")
        self.emailEntry.applyPlaceholder()
        self.emailEntry.place(width=300, height=30, relx=.5, rely=0.4, anchor='center')
        self.widgets.append(self.emailEntry)

        # Password prompt.
        self.promptPassword = tk.Label(text="Password", font=("SegoeUI", 10), bg="#FFF", fg="purple")
        self.promptPassword.place(relx=.37, rely=.5, anchor='center')
        self.widgets.append(self.promptPassword)

        # Password text box
        self.passwordEntry = PasswordPlaceholderEntry(placeholder="<Enter your password>", master=Resources.TK_CLIENT, textColor="#CCC")
        self.passwordEntry.applyPlaceholder()
        self.passwordEntry.place(width=300, height=30, relx=.5, rely=0.55, anchor='center')
        self.widgets.append(self.passwordEntry)

        # Login button
        self.loginButton = tk.Button(Resources.TK_CLIENT, command=self.handleLoginClick, borderwidth=1, bg="purple", activebackground="#FF5733", activeforeground="#FFF", fg="#FFF", text="Login", font=("SegoeUI", 12))
        self.loginButton.place(width=200, relx=.5, rely=.66, anchor='center')
        self.widgets.append(self.loginButton)

        # Error message label
        self.errorMessageLabel = tk.Label(Resources.TK_CLIENT, text="", bg="#FFF", font=("SegoeUI 10 bold"), fg="red")
        self.errorMessageLabel.place(relx=.5, rely=.82, anchor='center')
        self.widgets.append(self.errorMessageLabel)

    """
    
    HandleLoginClick() is an event-binded method that invokes when the login button (@see self.loginButton) is clicked.
    """
    def handleLoginClick(self):
        if Resources.REDIS_DB == None:
            self.errorMessageLabel.configure(text="Server down, please try again later!")
        else:
            users = Resources.REDIS_DB.redisStdGet(f"user:{self.emailEntry.get()}")
            if not users:
                self.errorMessageLabel.configure(text="This email address does not exist in our system.")
            else:
                user = dict(loads(users))
                encrypted = md5(self.passwordEntry.get().encode('utf-8')).hexdigest()
                if encrypted == user['password']:
                    print("Logged in successfully")
                    activeUser = User(user['email'], user['password'])
                    Resources.ACTIVE_USER = activeUser
                    Resources.TK_CLIENT.showFrame(PortalPage)
                else:
                    self.errorMessageLabel.configure(text="Invalid email/password combination!")
                
    """
    
    HandleCreateAccountClick() is an event-binded method that invokes when the create account button (@see self.createAccountButton) is clicked.
    """
    def handleCreateAccountClick(self):
        print("Create new account")