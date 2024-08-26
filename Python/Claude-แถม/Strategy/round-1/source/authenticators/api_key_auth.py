# auth_system/authenticators/api_key_auth.py

from typing import Dict, Any
from .authenticator_interface import AuthenticatorInterface
from ..utils.exceptions import AuthenticationError

class APIKeyAuthenticator(AuthenticatorInterface):
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys

    def authenticate(self, request: Dict[str, Any]) -> bool:
        api_key = request.get('api_key') or request.get('Authorization')
        
        if not api_key:
            raise AuthenticationError("Missing API key")

        if api_key.startswith('ApiKey '):
            api_key = api_key.split(' ')[1]

        if api_key in self.api_keys:
            return True
        
        return False