from flask import Flask, request, jsonify
from auth.basic_auth import BasicAuth
from auth.session_auth import SessionAuth
from auth.jwt_auth import JWTAuth
from auth.api_key_auth import APIKeyAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Example: Initialize with a strategy
authenticator = BasicAuth()  # You can switch to another strategy like SessionAuth()

@app.route('/login', methods=['POST'])
def login():
    if authenticator.authenticate(request):
        return jsonify(message="Authenticated"), 200
    return jsonify(message="Unauthorized"), 401

@app.route('/create-session', methods=['POST'])
def create_session():
    if isinstance(authenticator, SessionAuth):
        session_auth = authenticator
        username = request.json.get('username')
        session_id = session_auth.create_session(username)
        resp = jsonify(message="Session created")
        resp.set_cookie('session_id', session_id)
        return resp
    return jsonify(message="Not supported"), 400

if __name__ == "__main__":
    app.run(debug=True)
