import os
import pymongo
import src.login_password_hash as login_password_hash
import bcrypt
from flask import Blueprint, jsonify, request, session

client = pymongo.MongoClient()
my_db = client["password_manager"]
collection = my_db["users"]

login_bp = Blueprint('login',__name__,url_prefix='/api/auth')

@login_bp.route('/register',methods=['POST'])
def register_user():
    login_hasher = login_password_hash.Login_Password()
    response = request.get_json()
    user_dict = {
       "username": response.get("username"),
        "hashed_password": login_hasher.hash_password(response.get("password")),
        "saved_passwords": {
        }
    }
    try:
        collection.insert_one(user_dict)
        return jsonify("User Successfully Created"), 201
    except Exception as e:
        return jsonify(e), 400


@login_bp.route('/', methods=['POST'])
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
            if hashed_password and bcrypt.checkpw(password=password.encode('utf-8'), hashed_password=hashed_password):
                session["username"] = username
                return jsonify("Welcome to Password Manager"), 201
            else:
                return jsonify("Invalid Password, Please Try Again"), 400
            
def main():
    register_user()
    login_user()