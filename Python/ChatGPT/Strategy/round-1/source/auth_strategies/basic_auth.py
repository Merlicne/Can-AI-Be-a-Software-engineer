# auth_strategies/basic_auth.py
import base64
from flask import Request
from .authenticator import Authenticator

class BasicAuth(Authenticator):
    def __init__(self):
        # Predefined credentials (for simplicity)
        self.users = {
            'user1': 'password1',
            'user2': 'password2',
        }

    def authenticate(self, request: Request) -> bool:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return False

        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)

        return self.users.get(username) == password
