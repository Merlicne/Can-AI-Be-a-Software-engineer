# auth_system/authenticators/basic_auth.py

import base64
from typing import Dict, Any
from .authenticator_interface import AuthenticatorInterface
from ..utils.exceptions import AuthenticationError

class BasicAuthenticator(AuthenticatorInterface):
    def __init__(self, users: Dict[str, str]):
        self.users = users

    def authenticate(self, request: Dict[str, Any]) -> bool:
        auth_header = request.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            raise AuthenticationError("Missing or invalid Authorization header")

        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':')

        if username in self.users and self.users[username] == password:
            return True
        return False