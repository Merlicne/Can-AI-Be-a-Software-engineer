# main.py
from flask import Flask, request, jsonify
from auth_strategies.basic_auth import BasicAuth
from auth_strategies.session_auth import SessionAuth
from auth_strategies.jwt_auth import JWTAuth
from auth_strategies.api_key_auth import APIKeyAuth

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Choose your authentication strategy
authenticator = BasicAuth()  # Replace with SessionAuth(), JWTAuth(), or APIKeyAuth()

@app.route('/login', methods=['POST'])
def login():
    if authenticator.authenticate(request):
        # Handle login success (e.g., create session or generate JWT token)
        return jsonify({'message': 'Authenticated'}), 200
    return jsonify({'message': 'Unauthorized'}), 401

@app.route('/secure-endpoint', methods=['GET'])
def secure_endpoint():
    if authenticator.authenticate(request):
        return jsonify({'message': 'You have access'}), 200
    return jsonify({'message': 'Unauthorized'}), 401

if __name__ == '__main__':
    app.run(debug=True)
