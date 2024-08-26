import jwt
from datetime import datetime, timedelta
from .base_auth import Authenticator

SECRET_KEY = 'your_secret_key'

class JWTAuth(Authenticator):

    def generate_token(self, username: str):
        expiration = datetime.utcnow() + timedelta(hours=1)
        token = jwt.encode({'username': username, 'exp': expiration}, SECRET_KEY, algorithm='HS256')
        return token

    def authenticate(self, request) -> bool:
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return False
        
        try:
            scheme, token = auth_header.split(' ')
            if scheme.lower() != 'bearer':
                return False

            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
