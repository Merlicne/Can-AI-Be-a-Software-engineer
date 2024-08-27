import uuid
from flask import Request, session
from .authenticator import Authenticator

class SessionAuthenticator(Authenticator):
    def __init__(self, users):
        self.users = users
        self.sessions = {}

    def authenticate(self, request: Request) -> bool:
        session_id = session.get('session_id')
        if session_id and session_id in self.sessions:
            return True
        return False

    def login(self, username: str, password: str) -> str:
        if self.users.get(username) == password:
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = username
            return session_id
        return None

    def logout(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]