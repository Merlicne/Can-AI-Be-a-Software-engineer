import jwt
from .__init__ import AuthenticationStrategy
from ..exceptions import AuthenticationError

class JWTAuthStrategy(AuthenticationStrategy):
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationError('Missing Authorization header')

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            # Further validation of payload can be done here
            return True
        except jwt.ExpiredSignatureError:
            raise AuthenticationError('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationError('Invalid token')