import bcrypt
import pymongo

class Password:
    def __init__(self):
        self.password_hash = []

    def hash_password(self, password):
        salt_rounds = 13
        salt = bcrypt.gensalt(salt_rounds)
        password = bcrypt.hashpw(password=password.encode(),salt=salt)
        self.password_hash.append(password)
        return password


def register_user():
    client = pymongo.MongoClient()
    my_db = client["password_manager"]
    collection = my_db["users"]
    password_manager = Password()
    username = input("Please create a username: ")
    password = input("Please create a Password: ")
    hashed_user_password = password_manager.hash_password(password)
    user_dict = {
       "username": username,
        "hashed_password": hashed_user_password
    }
    collection.insert(user_dict)

def login_user():
    client = pymongo.MongoClient()
    my_db = client["password_manager"]
    collection = my_db["users"]
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    user = collection.find_one({"username":username})

    if not user:
        print("Username Not Found, Please Try Again")
        return
    else:
        hashed_password = user.get("hashed_password")
        if hashed_password and bcrypt.checkpw(password=password.encode(),hashed_password=hashed_password):
            print("Welcome to Password Manager")
        else:
            print("Password Invalid")

def main():
    while True:
        user_status = input("Welcome to Password Manager, Are You a New User? (Y/N)")
        if user_status == "Y":
           register_user()
        else:
            login_user()


if __name__ == "__main__":
    main()