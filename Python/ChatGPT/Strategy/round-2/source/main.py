from flask import Flask, request, jsonify
from strategies.basic_auth import BasicAuth
from strategies.session_auth import SessionAuth
from strategies.jwt_auth import JWTAuth
from strategies.api_key_auth import APIKeyAuth

app = Flask(__name__)

# Configuration (these would typically come from environment variables or config files)
users = {'user': 'password'}
session_store = {}  # This should be replaced with a proper session store (e.g., database)
secret_key = 'supersecretkey'
valid_api_keys = {'key123', 'key456'}

# Create instances of authentication strategies
auth_strategies = {
    'basic': BasicAuth(users),
    'session': SessionAuth(session_store),
    'jwt': JWTAuth(secret_key),
    'api_key': APIKeyAuth(valid_api_keys),
}

@app.route('/login', methods=['POST'])
def login():
    auth_type = request.args.get('auth_type')
    auth = auth_strategies.get(auth_type)
    if auth and auth.authenticate(request):
        return jsonify(message='Authenticated'), 200
    return jsonify(message='Unauthorized'), 401

if __name__ == '__main__':
    app.run(debug=True)
