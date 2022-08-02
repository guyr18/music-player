class User:

    """
    
    __init__(email, password) takes the following two parameters:

        email: A string representing the email address of this User instance.
        password: A string representing the encrypted password of this User instance.

        Additionally, this method assigns the variable @see self.nickname by extracting
        the prefix (characters before '@' symbol) in @see self.email.
        
    """

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.nickname = None
        left, right = 0, 0

        while self.email[right] != '@':
            right += 1
        self.nickname = self.email[left:right]