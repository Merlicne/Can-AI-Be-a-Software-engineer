import base64
from auth.authenticator import Authenticator
from auth.exceptions import AuthenticationError

class BasicAuthenticator(Authenticator):
    """
    Basic authentication strategy.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            raise AuthenticationError('Missing or invalid Authorization header.')

        auth_data = base64.b64decode(auth_header[6:]).decode('utf-8')
        username, password = auth_data.split(':', 1)

        # Authenticate user against predefined set (replace with your logic)
        if username == 'user' and password == 'password':
            return {'username': username}

        raise AuthenticationError('Invalid username or password.')