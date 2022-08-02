from PlaceholderEntry import PlaceholderEntry

class PasswordPlaceholderEntry(PlaceholderEntry):

    """
    
    __init__(placeholder, master, textColor) passes its corresponding parameters
    to its base class. 

        placeholder -> A string representing the default text content for this instance.
        master -> A master or parent tk.Frame container.
        textColor -> The color of the text content represented as a hexadecimal string.
            
    """
    def __init__(self, placeholder, master, textColor):
        super().__init__(placeholder, master, textColor)
        self.configure(show='*')