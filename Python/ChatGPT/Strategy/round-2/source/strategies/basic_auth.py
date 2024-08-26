import base64
from strategies import Authenticator

class BasicAuth(Authenticator):
    
    def __init__(self, users):
        self.users = users

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Basic '):
            try:
                credentials = base64.b64decode(auth_header.split(' ')[1]).decode('utf-8')
                username, password = credentials.split(':', 1)
                if self.users.get(username) == password:
                    return True
            except Exception:
                pass
        return False
