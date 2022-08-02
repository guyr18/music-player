class User:

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.nickname = None
        left, right = 0, 0

        while self.email[right] != '@':
            right += 1
        self.nickname = self.email[left:right]