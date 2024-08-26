from flask import session
from auth.authenticator import Authenticator
from auth.exceptions import AuthenticationError

class SessionAuthenticator(Authenticator):
    """
    Session-based authentication strategy.
    """

    def authenticate(self, request):
        user_id = session.get('user_id')
        if not user_id:
            raise AuthenticationError('Not logged in.')

        # Retrieve user from database based on session (replace with your logic)
        user = {'user_id': user_id}
        return user