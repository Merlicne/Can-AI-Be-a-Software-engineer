# auth_system/strategies/jwt_auth.py
import jwt
from .authenticator import Authenticator
from ..utils.jwt_utils import JWTUtils

class JWTAuth(Authenticator):
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return False
        auth_type, token = auth_header.split()
        if auth_type.lower() != 'bearer':
            return False
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False