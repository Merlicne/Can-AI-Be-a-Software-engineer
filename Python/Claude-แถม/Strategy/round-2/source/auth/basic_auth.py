import base64
from flask import Request
from .authenticator import Authenticator

class BasicAuthenticator(Authenticator):
    def __init__(self, users):
        self.users = users

    def authenticate(self, request: Request) -> bool:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return False
        
        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':')
        
        return self.users.get(username) == password