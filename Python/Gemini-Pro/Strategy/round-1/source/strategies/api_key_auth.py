from .__init__ import AuthenticationStrategy
from ..exceptions import AuthenticationError

class APIKeyAuthStrategy(AuthenticationStrategy):
    def __init__(self, api_keys):
        self.api_keys = api_keys

    def authenticate(self, request):
        api_key = request.headers.get('Authorization') or request.args.get('api_key')
        if not api_key:
            raise AuthenticationError('Missing API Key')

        if api_key in self.api_keys:
            return True
        else:
            raise AuthenticationError('Invalid API Key')