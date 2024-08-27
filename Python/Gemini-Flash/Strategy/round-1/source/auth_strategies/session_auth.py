from auth_strategies.auth_strategy import AuthenticationStrategy
from collections import defaultdict

class SessionAuthentication(AuthenticationStrategy):
    """
    Implements Session-Based Authentication strategy.
    """

    def __init__(self):
        """
        Initializes the SessionAuthentication strategy with an empty session store.
        """
        self.sessions = defaultdict(lambda: None)

    def authenticate(self, request):
        """
        Authenticates the request using Session-Based Authentication.

        Args:
            request: The incoming request object.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        session_id = request.cookies.get("session_id")
        return session_id in self.sessions and self.sessions[session_id] is not None