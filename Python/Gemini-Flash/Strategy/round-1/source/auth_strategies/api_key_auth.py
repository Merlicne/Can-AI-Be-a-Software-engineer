from auth_strategies.auth_strategy import AuthenticationStrategy

class APIKeyAuthentication(AuthenticationStrategy):
    """
    Implements API Key Authentication strategy.
    """

    def __init__(self, api_keys):
        """
        Initializes the APIKeyAuthentication strategy with a dictionary of API keys.

        Args:
            api_keys: A dictionary of user IDs and API keys.
        """
        self.api_keys = api_keys

    def authenticate(self, request):
        """
        Authenticates the request using API Key Authentication.

        Args:
            request: The incoming request object.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        api_key = request.headers.get("Authorization") or request.args.get("api_key")

        if not api_key:
            return False

        return api_key in self.api_keys.values()