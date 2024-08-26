import base64

class BasicAuthentication(Authenticator):
    def __init__(self, users):
        self.users = users

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return False
        auth_type, credentials = auth_header.split()
        if auth_type.lower() != 'basic':
            return False
        decoded_credentials = base64.b64decode(credentials).decode('utf-8')
        username, password = decoded_credentials.split(':')
        return self.users.get(username) == password