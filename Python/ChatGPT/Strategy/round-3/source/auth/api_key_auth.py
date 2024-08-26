from .base_auth import Authenticator

class APIKeyAuth(Authenticator):

    def __init__(self):
        self.valid_api_keys = {'apikey123', 'apikey456'}

    def authenticate(self, request) -> bool:
        api_key = request.headers.get('Authorization') or request.args.get('api_key')
        return api_key in self.valid_api_keys
