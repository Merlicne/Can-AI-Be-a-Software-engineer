import base64
from auth_strategies.auth_strategy import AuthenticationStrategy

class BasicAuthentication(AuthenticationStrategy):
    """
    Implements Basic Authentication strategy.
    """

    def __init__(self, users):
        """
        Initializes the BasicAuthentication strategy with a predefined set of users.

        Args:
            users: A dictionary of usernames and passwords.
        """
        self.users = users

    def authenticate(self, request):
        """
        Authenticates the request using Basic Authentication.

        Args:
            request: The incoming request object.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Basic "):
            return False

        encoded_credentials = auth_header.split(" ")[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded_credentials.split(":")

        return username in self.users and self.users[username] == password