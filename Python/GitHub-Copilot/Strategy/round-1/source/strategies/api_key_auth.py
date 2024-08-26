# auth_system/strategies/api_key_auth.py
from .authenticator import Authenticator
from ..utils.api_key_store import APIKeyStore

class APIKeyAuth(Authenticator):
    def __init__(self, api_key_store: APIKeyStore):
        self.api_key_store = api_key_store

    def authenticate(self, request):
        api_key = request.headers.get('Authorization') or request.args.get('api_key')
        if not api_key:
            return False
        return self.api_key_store.validate_key(api_key)