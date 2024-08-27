import jwt
from datetime import datetime, timedelta
from flask import Request
from .authenticator import Authenticator

class JWTAuthenticator(Authenticator):
    def __init__(self, secret_key, users):
        self.secret_key = secret_key
        self.users = users

    def authenticate(self, request: Request) -> bool:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False
        
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['username'] in self.users
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def generate_token(self, username: str, password: str) -> str:
        if self.users.get(username) == password:
            payload = {
                'username': username,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }
            return jwt.encode(payload, self.secret_key, algorithm='HS256')
        return None