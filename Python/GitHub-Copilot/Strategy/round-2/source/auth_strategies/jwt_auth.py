import jwt
import datetime

SECRET_KEY = 'your_secret_key'

class JWTAuth:
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise Exception("Missing Authorization header")

        auth_type, token = auth_header.split()
        if auth_type.lower() != 'bearer':
            raise Exception("Invalid auth type")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return True
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

    def login(self, username, password):
        # Replace with actual user verification logic
        if username == 'admin' and password == 'password':
            payload = {
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return token
        else:
            raise Exception("Invalid credentials")