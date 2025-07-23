import os
import pymongo
import src.login_password_hash as login_password_hash
import bcrypt
from dotenv import load_dotenv
from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = os.getenv("KEY")

client = pymongo.MongoClient()
my_db = client["password_manager"]
collection = my_db["users"]

@app.route('/register',methods=['POST'])
def register_user():
    password_manager = login_password_hash.Login_Password()
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
                session["username"] = username
                return jsonify("Welcome to Password Manager"), 201
            else:
                return jsonify("Invalid Password, Please Try Again"), 400
            
def main():
    register_user()
    login_user()

if __name__ == "__main__":
    app.run('0.0.0.0', 5001)