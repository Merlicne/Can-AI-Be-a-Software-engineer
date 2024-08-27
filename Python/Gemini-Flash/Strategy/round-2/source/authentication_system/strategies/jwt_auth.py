from ..authenticator import Authenticator
from ..utils import tokens

class JWTAuthentication(Authenticator):
    """
    JWT Authentication strategy.
    """

    def authenticate(self, request):
        """
        Authenticates the request using JWT Authentication.

        Args:
            request: The request object.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return False

        token = auth_header.split(' ', 1)[1]
        return tokens.validate_jwt(token)