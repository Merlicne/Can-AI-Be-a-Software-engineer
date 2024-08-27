# auth_system/authenticators/jwt_auth.py

import jwt
from typing import Dict, Any
from datetime import datetime, timedelta
from .authenticator_interface import AuthenticatorInterface
from ..utils.exceptions import AuthenticationError

class JWTAuthenticator(AuthenticatorInterface):
    def __init__(self, secret_key: str, users: Dict[str, str], token_expiry: int = 3600):
        self.secret_key = secret_key
        self.users = users
        self.token_expiry = token_expiry

    def authenticate(self, request: Dict[str, Any]) -> bool:
        auth_header = request.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationError("Missing or invalid Authorization header")

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            username = payload['username']
            if username in self.users:
                return True
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")

        return False

    def generate_token(self, username: str) -> str:
        if username not in self.users:
            raise AuthenticationError("Invalid username")

        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(seconds=self.token_expiry)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')