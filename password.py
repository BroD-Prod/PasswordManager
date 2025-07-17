import bcrypt

class Password:
    def __init__(self):
        self.password_hash = []

    def hash_password(self, password):
        salt_rounds = 13
        salt = bcrypt.gensalt(salt_rounds)
        hash = bcrypt.hashpw(password=password.encode(),salt=salt)
        self.password_hash.append(hash)
        return hash
