import hashlib
import pymongo

class Password:
    def __init__(self):
        self.passwords = []
        self.password_hash = []

    def hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.password_hash.append(hashed_password)
        return hashed_password


def register_user():
    client = pymongo.MongoClient()
    my_db = client["password_manager"]
    collection = my_db["users"]
    password_manager = Password()
    username = input("Please create a username: ")
    password = input("Please create a Password: ")
    hashed_password = password_manager.hash_password(password)
    user_dict = {
       "username": username,
        "hashed_password": hashed_password
    }
    collection.insert_one(user_dict)

def login_user():
    client = pymongo.MongoClient()
    my_db = client["password_manager"]
    collection = my_db["users"]
    password_manager = Password()
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    if not collection.find({"username": username}):
        print("Username Not Found, Please Try Again")
        return
    if not collection.find({"hashed_password": password_manager.hash_password(password)}):
        print("Password Invalid")
    else:
        print("Welcome to Password Manager")

def main():
    client = pymongo.MongoClient()
    my_db = client["password_manager"]
    collection = my_db["users"]
    while True:
        user_status = input("Welcome to Password Manager, Are You a New User? (Y/N)")
        if user_status == "Y":
           register_user()
        else:
            login_user()


if __name__ == "__main__":
    main()