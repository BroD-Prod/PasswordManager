import os
import pymongo
import src.manager_password_hash as hasher
from dotenv import load_dotenv
from flask import Flask, jsonify, request, session, Blueprint

client = pymongo.MongoClient()
my_db = client["password_manager"]
collection = my_db["users"]

manager_bp = Blueprint('manager',__name__,'/manager')

hasher = hasher.Manager_Password()

@manager_bp.route('/create_password',methods=['POST'])
def create_password():
    response = request.get_json()
    saved_site = {
        "site": response.get('site'),
        "password": hasher.encrypt_site_password(response.get('password'))
    }
    try:
        collection.insert_one({"saved_passwords": saved_site})
        return jsonify(f"Password for {saved_site['site']} saved."), 201
    except Exception as e:
        return jsonify(e), 400

@manager_bp.route('/change_password',methods=['POST'])
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

@manager_bp.route('/register',methods=['POST'])
def register_user():
    response = request.get_json()
    user_dict = {
       "username": response.get("username"),
        "hashed_password": hasher.encrypt_site_password(response.get("password")),
        "saved_passwords": {
        }
    }
    try:
        collection.insert_one(user_dict)
        return jsonify("User Successfully Created"), 201
    except Exception as e:
        return jsonify(e), 400