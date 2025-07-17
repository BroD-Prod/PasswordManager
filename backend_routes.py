import os
import pymongo
import password
import bcrypt
from dotenv import load_dotenv
from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = os.getenv("KEY")

client = pymongo.MongoClient()
my_db = client["password_manager"]
collection = my_db["users"]

@app.route('/create_password',methods=['POST'])
def create_password():
    password_manager = password.Password()
    response = request.get_json()
    saved_site = {
        "site": response.get('site'),
        "password": password_manager.hash_password(response.get('password'))
    }
    try:
        collection.insert_one({"saved_passwords": saved_site})
        return jsonify(f"Password for {saved_site['site']} saved."), 201
    except Exception as e:
        return jsonify(e), 400

@app.route('/change_password',methods=['POST'])
def change_password():
    username = session.get("username")
    if not username:
        return jsonify("Unauthorized"), 401
    response = request.get_json()
    site = response.get("site")
    new_password = response.get("password")
    if not site or not new_password:
        return jsonify("Missing Site or New Password")
    try:
        user = collection.find_one({
            "username": username,
            "saved_passwords": site
        })
        if not user:
            return jsonify("Site Not Found"), 404
        collection.update_one(
            {
                "username": username,
                "saved_passwords.site": site
            },
            {
                "$set": {
                    "saved_passwords.$.password": new_password
                }
            }
        )
        return jsonify(f"Passwords for {site} successfully changed")
    
    except Exception as e:
        return jsonify(e), 500

@app.route('/register',methods=['POST'])
def register_user():
    password_manager = password.Password()
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
    create_password()
    change_password()

if __name__ == "__main__":
    app.run('0.0.0.0', 5001)