import base64
from .__init__ import AuthenticationStrategy
from ..exceptions import AuthenticationError

class BasicAuthStrategy(AuthenticationStrategy):
    def __init__(self, users):
        self.users = users

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationError('Missing Authorization header')

        auth_parts = auth_header.split(' ')
        if len(auth_parts) != 2 or auth_parts[0].lower() != 'basic':
            raise AuthenticationError('Invalid Authorization header format')

        try:
            username, password = base64.b64decode(auth_parts[1]).decode().split(':')
        except Exception:
            raise AuthenticationError('Invalid credentials encoding')

        if self.users.get(username) == password:
            return True
        else:
            raise AuthenticationError('Invalid username or password')