# auth_strategies/api_key_auth.py
from flask import Request
from .authenticator import Authenticator

class APIKeyAuth(Authenticator):
    def __init__(self):
        self.api_keys = {
            'key1': 'user1',
            'key2': 'user2',
        }

    def authenticate(self, request: Request) -> bool:
        api_key = request.headers.get('Authorization') or request.args.get('api_key')
        return api_key in self.api_keys
