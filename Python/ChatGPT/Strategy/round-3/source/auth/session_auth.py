from .base_auth import Authenticator
from flask import session

class SessionAuth(Authenticator):

    def __init__(self):
        self.sessions = {}

    def authenticate(self, request) -> bool:
        session_id = request.cookies.get('session_id')
        if session_id and session_id in self.sessions:
            return True
        return False

    def create_session(self, username: str):
        import uuid
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = username
        return session_id
