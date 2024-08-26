# auth_system/strategies/session_auth.py
from .authenticator import Authenticator
from ..utils.session_store import SessionStore

class SessionAuth(Authenticator):
    def __init__(self, session_store: SessionStore):
        self.session_store = session_store

    def authenticate(self, request):
        session_id = request.cookies.get('session_id')
        if not session_id:
            return False
        return self.session_store.validate_session(session_id)