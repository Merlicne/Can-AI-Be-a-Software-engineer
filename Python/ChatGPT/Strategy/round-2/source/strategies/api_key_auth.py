from strategies import Authenticator

class APIKeyAuth(Authenticator):
    
    def __init__(self, valid_keys):
        self.valid_keys = valid_keys

    def authenticate(self, request):
        api_key = request.headers.get('Authorization') or request.args.get('api_key')
        if api_key in self.valid_keys:
            return True
        return False
