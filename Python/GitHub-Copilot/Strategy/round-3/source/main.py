from flask import Flask, request, jsonify
from auth_strategies.basic_authentication import BasicAuthentication
from auth_strategies.session_authentication import SessionAuthentication
from auth_strategies.jwt_authentication import JWTAuthentication
from auth_strategies.api_key_authentication import APIKeyAuthentication

app = Flask(__name__)

# Example users and API keys
users = {'user1': 'password1'}
api_keys = {'valid_api_key'}

# Initialize authentication strategies
basic_auth = BasicAuthentication(users)
session_auth = SessionAuthentication()
jwt_auth = JWTAuthentication('secret')
api_key_auth = APIKeyAuthentication(api_keys)

# Example route
@app.route('/protected')
def protected():
    if not basic_auth.authenticate(request):
        return jsonify({'message': 'Unauthorized'}), 401
    return jsonify({'message': 'Welcome!'})

if __name__ == '__main__':
    app.run(debug=True)