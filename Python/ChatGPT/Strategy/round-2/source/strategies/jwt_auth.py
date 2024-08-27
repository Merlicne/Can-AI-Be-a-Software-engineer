import jwt
from strategies import Authenticator

class JWTAuth(Authenticator):
    
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                decoded = jwt.decode(token, self.secret_key, algorithms=["HS256"])
                return True
            except jwt.ExpiredSignatureError:
                pass
            except jwt.InvalidTokenError:
                pass
        return False
