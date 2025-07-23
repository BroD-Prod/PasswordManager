import bcrypt

class Login_Password:
    def __init__(self):
        pass

    def hash_password(self, password):
        salt = bcrypt.gensalt(rounds=13)
        hash = bcrypt.hashpw(password=password.encode('utf-8'),salt=salt)
        return hash.decode('utf-8')
