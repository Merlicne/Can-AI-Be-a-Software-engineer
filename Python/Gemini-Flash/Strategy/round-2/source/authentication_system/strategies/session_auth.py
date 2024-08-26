from ..authenticator import Authenticator
from ..utils import users, sessions

class SessionAuthentication(Authenticator):
    """
    Session-Based Authentication strategy.
    """

    def authenticate(self, request):
        """
        Authenticates the request using Session-Based Authentication.

        Args:
            request: The request object.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        session_id = request.cookies.get('session_id')
        if not session_id:
            return False

        return sessions.validate_session(session_id)