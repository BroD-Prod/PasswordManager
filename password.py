import bcrypt
import pymongo
from flask import Flask, jsonify, request

app = Flask(__name__)

class Password:
    def __init__(self):
        self.password_hash = []

    def hash_password(self, password):
        salt_rounds = 13
        salt = bcrypt.gensalt(salt_rounds)
        password = bcrypt.hashpw(password=password.encode(),salt=salt)
        self.password_hash.append(password)
        return password


@app.route('/register',methods=['POST'])
def register_user():
    client = pymongo.MongoClient()
    my_db = client["password_manager"]
    collection = my_db["users"]
    password_manager = Password()
    response = request.get_json()
    username = response.get("username")
    password = response.get("password")
    hashed_user_password = password_manager.hash_password(password)
    user_dict = {
       "username": username,
        "hashed_password": hashed_user_password
    }
    try:
        collection.insert_one(user_dict)
        return jsonify("User Successfully Created"), 201
    except Exception as e:
        return jsonify(e), 400


@app.route('/login', methods=['POST'])
def login_user():
    client = pymongo.MongoClient()
    my_db = client["password_manager"]
    collection = my_db["users"]

    response = request.get_json()
    username = response.get("username")
    password = response.get("password")

    if not username or not password:
        return jsonify("Username/Password Required. Please Try Again"), 400
    else:
        user = collection.find_one({"username": username})
        if not user:
            return jsonify("Invalid Username, Please Try Again"), 400
        else:
            hashed_password = user.get("hashed_password")
            if hashed_password and bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password):
                return jsonify("Welcome to Password Manager"), 201
            else:
                return jsonify("Invalid Password, Please Try Again"), 400


def main():
    response = request.get_json()
    while True:
        if response.get("yes"):
            register_user()
        else:
            login_user()

if __name__ == "__main__":
    app.run('0.0.0.0', 5001)