# auth_system/main.py
from flask import Flask, request, jsonify
from strategies.base_auth import BasicAuth
from strategies.session_auth import SessionAuth
from strategies.jwt_auth import JWTAuth
from strategies.api_key_auth import APIKeyAuth
from utils.session_store import SessionStore
from utils.jwt_utils import JWTUtils
from utils.api_key_store import APIKeyStore

app = Flask(__name__)

# Example users and keys
users = {'user1': 'password1', 'user2': 'password2'}
session_store = SessionStore()
api_key_store = APIKeyStore()
jwt_secret = 'your_jwt_secret'

# Initialize strategies
basic_auth = BasicAuth(users)
session_auth = SessionAuth(session_store)
jwt_auth = JWTAuth(jwt_secret)
api_key_auth = APIKeyAuth(api_key_store)

# Set the current strategy
current_strategy = basic_auth

@app.route('/login', methods=['POST'])
def login():
    if current_strategy.authenticate(request):
        return jsonify({"message": "Authenticated"}), 200
    return jsonify({"message": "Unauthorized"}), 401

if __name__ == '__main__':
    app.run(debug=True)