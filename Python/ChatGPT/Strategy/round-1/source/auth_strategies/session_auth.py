# auth_strategies/session_auth.py
from flask import Request, session
from .authenticator import Authenticator

class SessionAuth(Authenticator):
    def __init__(self):
        self.sessions = {}

    def authenticate(self, request: Request) -> bool:
        session_id = request.cookies.get('session_id')
        return session_id in self.sessions

    def create_session(self, user_id: str) -> str:
        import uuid
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = user_id
        return session_id
