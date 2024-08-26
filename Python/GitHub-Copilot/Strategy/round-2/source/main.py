from flask import Flask, request, jsonify
from auth_strategies.base_auth import BaseAuth
from auth_strategies.session_auth import SessionAuth
from auth_strategies.jwt_auth import JWTAuth
from auth_strategies.api_key_auth import APIKeyAuth

app = Flask(__name__)

# Initialize authentication strategies
base_auth = BaseAuth()
session_auth = SessionAuth()
jwt_auth = JWTAuth()
api_key_auth = APIKeyAuth()

# Example route using BaseAuth
@app.route('/base-auth', methods=['GET'])
def base_auth_route():
    try:
        base_auth.authenticate(request)
        return jsonify({"message": "Authenticated with Basic Auth"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

# Example route using SessionAuth
@app.route('/session-auth', methods=['GET'])
def session_auth_route():
    try:
        session_auth.authenticate(request)
        return jsonify({"message": "Authenticated with Session Auth"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

# Example route using JWTAuth
@app.route('/jwt-auth', methods=['GET'])
def jwt_auth_route():
    try:
        jwt_auth.authenticate(request)
        return jsonify({"message": "Authenticated with JWT Auth"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

# Example route using APIKeyAuth
@app.route('/api-key-auth', methods=['GET'])
def api_key_auth_route():
    try:
        api_key_auth.authenticate(request)
        return jsonify({"message": "Authenticated with API Key Auth"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True)