# auth_strategies/jwt_auth.py
import jwt
from flask import Request
from datetime import datetime, timedelta
from .authenticator import Authenticator

SECRET_KEY = 'your_secret_key'

class JWTAuth(Authenticator):
    def authenticate(self, request: Request) -> bool:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False

        token = auth_header.split(' ')[1]
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return decoded_token['exp'] > datetime.utcnow().timestamp()
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def create_token(self, user_id: str) -> str:
        expiration = datetime.utcnow() + timedelta(hours=1)
        payload = {
            'user_id': user_id,
            'exp': expiration.timestamp()
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
