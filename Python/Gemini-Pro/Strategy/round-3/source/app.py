from flask import Flask, request, jsonify
from auth.strategies import (
    BasicAuthenticationStrategy,
    SessionAuthenticationStrategy,
    JWTAuthenticationStrategy,
    APIKeyAuthenticationStrategy,
)

app = Flask(__name__)

# --- Configure your authentication strategy here ---
# Example:
auth_strategy = BasicAuthenticationStrategy(
    users={"admin": "password"}
)
# ------------------------------------------------

@app.route("/api/resource", methods=["GET"])
def protected_resource():
    user = auth_strategy.authenticate(request)
    if user:
        return jsonify({"message": f"Welcome, {user}!"}), 200
    else:
        return jsonify({"message": "Authentication required"}), 401

if __name__ == "__main__":
    app.run(debug=True)