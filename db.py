class ProfileDAO:
    def __init__(self):
        self.db = dict()

    def has(self, token):
        return token in self.db

    def get(self, token):
        return self.db[token]

    def set(self, token, profile):
        self.db[token] = profile

    def remove(self, token):
        del self.db[token]
