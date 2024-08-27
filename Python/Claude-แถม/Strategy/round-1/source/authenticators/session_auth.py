# auth_system/authenticators/session_auth.py

import uuid
from typing import Dict, Any
from .authenticator_interface import AuthenticatorInterface
from ..utils.exceptions import AuthenticationError
from ..storage.in_memory_storage import InMemoryStorage

class SessionAuthenticator(AuthenticatorInterface):
    def __init__(self, users: Dict[str, str], session_storage: InMemoryStorage):
        self.users = users
        self.session_storage = session_storage

    def authenticate(self, request: Dict[str, Any]) -> bool:
        if 'session_id' in request:
            session_id = request['session_id']
            return self.session_storage.exists(session_id)
        
        username = request.get('username')
        password = request.get('password')

        if username in self.users and self.users[username] == password:
            session_id = str(uuid.uuid4())
            self.session_storage.set(session_id, username)
            request['session_id'] = session_id
            return True
        
        raise AuthenticationError("Invalid credentials")