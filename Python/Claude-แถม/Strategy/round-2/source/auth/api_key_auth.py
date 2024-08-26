from flask import Request
from .authenticator import Authenticator

class APIKeyAuthenticator(Authenticator):
    def __init__(self, api_keys):
        self.api_keys = api_keys

    def authenticate(self, request: Request) -> bool:
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        return api_key in self.api_keys