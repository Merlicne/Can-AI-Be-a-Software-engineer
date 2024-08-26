from flask import Flask, request, jsonify
from authenticator import Authenticator
from strategies import *
from exceptions import AuthenticationError

app = Flask(__name__)
app.secret_key = "your_secret_key" # For session based auth

# Define users for basic auth
users = {
    "user1": "password1",
    "user2": "password2",
}

# Define API keys for API key auth
api_keys = ["key1", "key2"]

# Initialize authenticator with default strategy (e.g., Basic Authentication)
authenticator = Authenticator(BasicAuthStrategy(users))

@app.route('/login', methods=['POST'])
def login():
    # ... Login logic ...
    # On successful login, set the desired authentication strategy:
    if request.form.get('auth_type') == 'session':
        authenticator.set_strategy(SessionAuthStrategy())
        session['user'] = request.form.get('username')
        return jsonify({'message': 'Logged in successfully'}), 200
    elif request.form.get('auth_type') == 'jwt':
        authenticator.set_strategy(JWTAuthStrategy("your_secret_key"))
        # Generate and return JWT token
    elif request.form.get('auth_type') == 'api_key':
        authenticator.set_strategy(APIKeyAuthStrategy(api_keys))
        return jsonify({'api_key': 'your_generated_api_key'}), 200

@app.route('/protected')
def protected_resource():
    try:
        authenticator.authenticate(request)
        return jsonify({'message': 'Access granted'}), 200
    except AuthenticationError as e:
        return jsonify({'error': str(e)}), 401

if __name__ == "__main__":
    app.run(debug=True)