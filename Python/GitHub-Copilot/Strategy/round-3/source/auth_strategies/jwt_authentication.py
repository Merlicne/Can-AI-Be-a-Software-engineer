import jwt
import datetime

class JWTAuthentication(Authenticator):
    def __init__(self, secret):
        self.secret = secret

    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return False
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['exp'] > datetime.datetime.utcnow()
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def generate_token(self, username):
        payload = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')