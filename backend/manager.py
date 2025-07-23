import os
import pymongo
import src.manager_password_hash as hasher
from dotenv import load_dotenv
from flask import Flask, jsonify, request, session, Blueprint

client = pymongo.MongoClient()
my_db = client["password_manager"]
collection = my_db["users"]

manager_bp = Blueprint('manager',__name__,'/api/manager')

hasher = hasher.Manager_Password()

@manager_bp.route('/create_password',methods=['POST'])
def create_password():
    username = session.get("username")
    if not username:
        return jsonify("Unauthorized"), 401
    response = request.get_json()
    saved_site = {
        "site": response.get('site'),
        "username":response.get('username'),
        "password": hasher.encrypt_site_password(response.get('password'), session.get("hashed_password"))
    }
    try:
        collection.update_one({"username": username},
            {"$push": {"saved_passwords": saved_site}},
            upsert=True
            )
        return jsonify(f"Password & Username for {saved_site['site']} saved."), 201
    except Exception as e:
        return jsonify(e), 400

@manager_bp.route('/change_password',methods=['POST'])
def change_password():
    username = session.get("username")
    if not username:
        return jsonify("Unauthorized"), 401
    response = request.get_json()
    new_password = response.get("password")
    site = response.get("site")
    if not new_password or site:
        return jsonify("Missing New Password or Site")
    encypted_password = hasher.encrypt_site_password(new_password)
    try:
        collection.update_one(
            {
                "username": username,
                "saved_passwords.site": site
                },
                {
                    "$set": {
                        "saved_passwords.$.password": encypted_password
                    }
                }
        )
        return jsonify(f"Passwords for successfully changed")
    except Exception as e:
        return jsonify(e), 500

@manager_bp.route('/passwords', methods=['GET'])
def display_password():
    username = session.get("username")
    if not username:
        return jsonify('Unauthorized'), 401
    collection.find(
        {"username": username},
        {"_id:": 0, "saved_passwords": 1}
                    )
    for doc in collection:
        print(doc)

def main():
    display_password()
    create_password()
    change_password()