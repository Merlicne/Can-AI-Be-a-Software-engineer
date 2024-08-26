from flask import Flask, request, jsonify

from auth_strategies.basic_auth import BasicAuthentication
from auth_strategies.session_auth import SessionAuthentication
from auth_strategies.jwt_auth import JWTAuthentication
from auth_strategies.api_key_auth import APIKeyAuthentication

app = Flask(__name__)

# Define users for Basic Authentication
users = {
    "john": "secret1",
    "jane": "secret2"
}

# Define API keys for API Key Authentication
api_keys = {
    "user1": "key1",
    "user2": "key2"
}

# Define a private key for JWT Authentication
private_key_path = "private_key.pem"

# Create instances of each authentication strategy
basic_auth = BasicAuthentication(users)
session_auth = SessionAuthentication()
jwt_auth = JWTAuthentication(private_key_path)
api_key_auth = APIKeyAuthentication(api_keys)

# Choose an authentication strategy (this can be modified dynamically)
current_strategy = basic_auth  # Start with Basic Authentication

@app.route("/protected")
def protected_resource():
    if current_strategy.authenticate(request):
        return jsonify({"message": "Access granted!"})
    else:
        return jsonify({"error": "Authentication failed!"}), 401

if __name__ == "__main__":
    app.run(debug=True)