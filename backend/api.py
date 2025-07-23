from flask import Flask, request, jsonify
from backend.login import login_bp
from backend.manager import manager_bp
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("KEY")

app = Flask(__name__)
CORS(app)

@app.before_request
def global_api_key_check():
    open_routes = ['/auth/login/register', '/auth/login/']
    if request.path in open_routes:
        return
    
    key = request.headers.get('X-API-KEY')
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401 

app.register_blueprint(login_bp)
app.register_blueprint(manager_bp)

if __name__ == "__main__":
    app.run(debug=True)