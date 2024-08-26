class APIKeyAuthentication(Authenticator):
    def __init__(self, api_keys):
        self.api_keys = api_keys

    def authenticate(self, request):
        api_key = request.headers.get('Authorization') or request.args.get('api_key')
        return api_key in self.api_keys