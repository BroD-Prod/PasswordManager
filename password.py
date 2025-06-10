import hashlib


class Password:
    def __init__(self):
        self.passwords = []
        self.password_hash = []

    def hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.password_hash.append(hashed_password)
        return hashed_password


def main():
    username = input("Please create a username: ")
    password = input("Please create a Password: ")
    password_manager = Password()
    hashed_password = password_manager.hash_password(password)
    user = {
        username : hashed_password
    }
    print(user)

if __name__ == "__main__":
    main()