from abc import ABC, abstractmethod
import base64
import jwt
from datetime import datetime, timedelta
from flask import request, jsonify

# ... (Import necessary modules for JWT, sessions, etc.)

class AuthenticationStrategy(ABC):
    """Abstract base class for authentication strategies."""
    
    @abstractmethod
    def authenticate(self, request):
        """Authenticates the request and returns the authenticated user or None."""
        pass


class BasicAuthenticationStrategy(AuthenticationStrategy):
    """Basic authentication strategy using username and password."""
    def __init__(self, users):
        self.users = users

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Basic "):
            return None

        auth_parts = base64.b64decode(auth_header[6:]).decode("utf-8").split(":")
        if len(auth_parts) != 2:
            return None

        username, password = auth_parts
        if username in self.users and self.users[username] == password:
            return username
        return None


class SessionAuthenticationStrategy(AuthenticationStrategy):
    """Session-based authentication strategy."""
    def __init__(self, session_manager):
        self.session_manager = session_manager

    def authenticate(self, request):
        session_id = request.cookies.get("session_id")
        if not session_id:
            return None

        user = self.session_manager.get_session(session_id)
        return user


class JWTAuthenticationStrategy(AuthenticationStrategy):
    """JWT authentication strategy."""
    def __init__(self, secret_key, algorithm="HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return None
        
        token = token.split(" ")[1]

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload.get("user")
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


class APIKeyAuthenticationStrategy(AuthenticationStrategy):
    """API key authentication strategy."""
    def __init__(self, api_keys):
        self.api_keys = api_keys

    def authenticate(self, request):
        api_key = request.headers.get("X-API-Key") or request.args.get("api_key")
        if not api_key:
            return None

        if api_key in self.api_keys:
            return self.api_keys[api_key]  # Return user associated with the API key
        return None