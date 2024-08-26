from authentication.authenticator import Authenticator

class APIKeyAuth(Authenticator):
    """
    API Key Authentication strategy.
    """

    def __init__(self, api_keys):
        """
        Initializes the APIKeyAuth strategy with a dictionary of API keys.
        Args:
            api_keys: A dictionary mapping user IDs to API keys.
        """
        self.api_keys = api_keys

    def authenticate(self, request):
        """
        Authenticates the request using API Key Authentication.
        Args:
            request: The request object.
        Returns:
            bool: True if the request is authenticated, False otherwise.
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            api_key = auth_header.split(' ')[1]
            if api_key in self.api_keys.values():
                return True
        return False