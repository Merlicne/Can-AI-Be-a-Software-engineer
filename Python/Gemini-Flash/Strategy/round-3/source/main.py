from authentication.strategies import BasicAuth, SessionAuth, JWTAuth, APIKeyAuth
from authentication.authenticator import Authenticator

# Example usage with Basic Authentication
users = {'user1': 'password1', 'user2': 'password2'}
basic_auth = BasicAuth(users)

# Example usage with Session Authentication
storage = {}
session_auth = SessionAuth(storage)

# Example usage with JWT Authentication
private_key = b'-----BEGIN PRIVATE KEY-----\n-----END PRIVATE KEY-----'
public_key = b'-----BEGIN PUBLIC KEY-----\n-----END PUBLIC KEY-----'
jwt_auth = JWTAuth(private_key, public_key)

# Example usage with API Key Authentication
api_keys = {'user1': 'key1', 'user2': 'key2'}
api_key_auth = APIKeyAuth(api_keys)

# Switching authentication strategies
authenticator = Authenticator  # Use the appropriate strategy class