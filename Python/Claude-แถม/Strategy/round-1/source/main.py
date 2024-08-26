# auth_system/main.py

from authenticators.basic_auth import BasicAuthenticator
from authenticators.session_auth import SessionAuthenticator
from authenticators.jwt_auth import JWTAuthenticator
from authenticators.api_key_auth import APIKeyAuthenticator
from storage.in_memory_storage import InMemoryStorage
from utils.exceptions import AuthenticationError

# Sample user data and API keys
users = {
    "alice": "password123",
    "bob": "securepass456"
}

api_keys = {
    "api_key_1": "alice",
    "api_key_2": "bob"
}

# Initialize storage
session_storage = InMemoryStorage()

# Initialize authenticators
basic_auth = BasicAuthenticator(users)
session_auth = SessionAuthenticator(users, session_storage)
jwt_auth = JWTAuthenticator("your-secret-key", users)
api_key_auth = APIKeyAuthenticator(api_keys)

def authenticate_request(auth_type: str, request: dict) -> bool:
    authenticators = {
        "basic": basic_auth,
        "session": session_auth,
        "jwt": jwt_auth,
        "api_key": api_key_auth
    }

    authenticator = authenticators.get(auth_type)
    if not authenticator:
        raise ValueError(f"Invalid authentication type: {auth_type}")

    try:
        return authenticator.authenticate(request)
    except AuthenticationError as e:
        print(f"Authentication failed: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    # Basic Auth
    basic_request = {
        "Authorization": "Basic YWxpY2U6cGFzc3dvcmQxMjM="  # Base64 encoded "alice:password123"
    }
    print("Basic Auth:", authenticate_request("basic", basic_request))

    # Session Auth
    session_request = {
        "username": "alice",
        "password": "password123"
    }
    print("Session Auth:", authenticate_request("session", session_request))
    
    # JWT Auth
    jwt_token = jwt_auth.generate_token("alice")
    jwt_request = {
        "Authorization": f"Bearer {jwt_token}"
    }
    print("JWT Auth:", authenticate_request("jwt", jwt_request))

    # API Key Auth
    api_key_request = {
        "api_key": "api_key_1"
    }
    print("API Key Auth:", authenticate_request("api_key", api_key_request))