from flask import Flask, request, jsonify
from auth.basic_auth import BasicAuthenticator
from auth.session_auth import SessionAuthenticator
from auth.jwt_auth import JWTAuthenticator
from auth.api_key_auth import APIKeyAuthenticator

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Mock user database
users = {
    'user1': 'password1',
    'user2': 'password2'
}

# Mock API keys
api_keys = ['key1', 'key2', 'key3']

# Initialize authenticators
basic_auth = BasicAuthenticator(users)
session_auth = SessionAuthenticator(users)
jwt_auth = JWTAuthenticator(app.secret_key, users)
api_key_auth = APIKeyAuthenticator(api_keys)

@app.route('/protected')
def protected():
    if basic_auth.authenticate(request) or session_auth.authenticate(request) or jwt_auth.authenticate(request) or api_key_auth.authenticate(request):
        return jsonify({"message": "Access granted"}), 200
    return jsonify({"message": "Access denied"}), 401

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if users.get(username) == password:
        session_id = session_auth.login(username, password)
        jwt_token = jwt_auth.generate_token(username, password)
        return jsonify({
            "message": "Login successful",
            "session_id": session_id,
            "jwt_token": jwt_token
        }), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session_auth.logout(request.json.get('session_id'))
    return jsonify({"message": "Logged out successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)