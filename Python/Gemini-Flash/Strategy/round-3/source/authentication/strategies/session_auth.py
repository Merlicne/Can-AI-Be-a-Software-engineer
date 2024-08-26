from authentication.authenticator import Authenticator
from uuid import uuid4

class SessionAuth(Authenticator):
    """
    Session-based Authentication strategy.
    """

    def __init__(self, storage):
        """
        Initializes the SessionAuth strategy with a storage mechanism.
        Args:
            storage: A storage object (e.g., in-memory dictionary, database) to store sessions.
        """
        self.storage = storage

    def authenticate(self, request):
        """
        Authenticates the request using Session-based Authentication.
        Args:
            request: The request object.
        Returns:
            bool: True if the request is authenticated, False otherwise.
        """
        session_id = request.cookies.get('session_id')
        if session_id:
            if session_id in self.storage:
                return True
        return False

    def create_session(self, user):
        """
        Creates a new session for a user.
        Args:
            user: The user object.
        Returns:
            str: The session ID.
        """
        session_id = str(uuid4())
        self.storage[session_id] = user
        return session_id