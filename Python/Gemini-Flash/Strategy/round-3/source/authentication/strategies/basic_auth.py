from authentication.authenticator import Authenticator
from base64 import b64decode
import re

class BasicAuth(Authenticator):
    """
    Basic Authentication strategy.
    """

    def __init__(self, users):
        """
        Initializes the BasicAuth strategy with a dictionary of users.
        Args:
            users: A dictionary mapping usernames to passwords.
        """
        self.users = users

    def authenticate(self, request):
        """
        Authenticates the request using Basic Authentication.
        Args:
            request: The request object.
        Returns:
            bool: True if the request is authenticated, False otherwise.
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            match = re.match(r'Basic\s+(.*)', auth_header)
            if match:
                encoded_credentials = match.group(1)
                credentials = b64decode(encoded_credentials).decode()
                username, password = credentials.split(':', 1)
                if username in self.users and self.users[username] == password:
                    return True
        return False