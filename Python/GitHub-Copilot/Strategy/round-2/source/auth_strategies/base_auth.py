import base64

class BaseAuth:
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise Exception("Missing Authorization header")

        auth_type, credentials = auth_header.split()
        if auth_type.lower() != 'basic':
            raise Exception("Invalid auth type")

        decoded_credentials = base64.b64decode(credentials).decode('utf-8')
        username, password = decoded_credentials.split(':')
        
        # Replace with actual user verification logic
        if username == 'admin' and password == 'password':
            return True
        else:
            raise Exception("Invalid credentials")  