import uuid
from flask import session
from .__init__ import AuthenticationStrategy
from ..exceptions import AuthenticationError

class SessionAuthStrategy(AuthenticationStrategy):
    def __init__(self):
        pass

    def authenticate(self, request):
        session_id = request.cookies.get('session_id')
        if not session_id or session.get(session_id) is None:
            raise AuthenticationError('Invalid or missing session ID')
        return True