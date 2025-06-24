import bcrypt
import pymongo
from flask import Flask, jsonify, request

app = Flask(__name__)

client = pymongo.MongoClient()
my_db = client["password_manager"]
collection = my_db["users"]

class Password:
    def __init__(self):
        self.password_hash = []

    def hash_password(self, password):
        salt_rounds = 13
        salt = bcrypt.gensalt(salt_rounds)
        password = bcrypt.hashpw(password=password.encode(),salt=salt)
        self.password_hash.append(password)
        return password

@app.route('/create_password',methods=['POST'])
def create_password():
    password_manager = Password()
    response = request.get_json()
    saved_site = {
        "site": response.get('site'),
        "password": password_manager.hash_password(response.get('password'))
    }
    try:
        collection.insert_one({"saved_passwords": saved_site})
        return jsonify("Password for " + saved_site['site'] + " saved."), 201
    except Exception as e:
        return jsonify(e), 400


@app.route('/register',methods=['POST'])
def register_user():
    password_manager = Password()
    response = request.get_json()
    user_dict = {
       "username": response.get("username"),
        "hashed_password": password_manager.hash_password(response.get("password")),
        "saved_passwords": {

        }
    }
    try:
        collection.insert_one(user_dict)
        return jsonify("User Successfully Created"), 201
    except Exception as e:
        return jsonify(e), 400


@app.route('/login', methods=['POST'])
def login_user():
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
    register_user()
    login_user()
    create_password()

if __name__ == "__main__":
    app.run('0.0.0.0', 5001)