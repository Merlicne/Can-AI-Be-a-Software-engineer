from ..utils import users
from ..authenticator import Authenticator

class BasicAuthentication(Authenticator):
    """
    Basic Authentication strategy.
    """

    def authenticate(self, request):
        """
        Authenticates the request using Basic Authentication.

        Args:
            request: The request object.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return False

        auth_type, encoded_credentials = auth_header.split(' ', 1)
        if auth_type.lower() != 'basic':
            return False

        username, password = users.decode_credentials(encoded_credentials)
        return users.validate_credentials(username, password)