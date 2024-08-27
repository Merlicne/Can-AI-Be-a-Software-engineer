import base64
from .base_auth import Authenticator

class BasicAuth(Authenticator):

    def __init__(self):
        # Example predefined users
        self.users = {'user1': 'password1', 'user2': 'password2'}

    def authenticate(self, request) -> bool:
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return False
        
        try:
            scheme, creds = auth_header.split(' ')
            if scheme.lower() != 'basic':
                return False
            
            decoded_creds = base64.b64decode(creds).decode('utf-8')
            username, password = decoded_creds.split(':')
            return self.users.get(username) == password
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
