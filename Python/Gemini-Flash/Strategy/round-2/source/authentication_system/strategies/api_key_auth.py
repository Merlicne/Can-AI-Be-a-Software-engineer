from ..authenticator import Authenticator
from ..utils import users

class APIKeyAuthentication(Authenticator):
    """
    API Key Authentication strategy.
    """

    def authenticate(self, request):
        """
        Authenticates the request using API Key Authentication.

        Args:
            request: The request object.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        api_key = request.headers.get('Authorization') or request.args.get('api_key')
        if not api_key:
            return False

        return users.validate_api_key(api_key)