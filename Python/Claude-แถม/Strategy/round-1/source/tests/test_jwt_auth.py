# tests/test_jwt_auth.py

import pytest
import jwt
import time
from authenticators.jwt_auth import JWTAuthenticator
from utils.exceptions import AuthenticationError

@pytest.fixture
def jwt_auth():
    secret_key = "test_secret_key"
    users = {"alice": "password123", "bob": "securepass456"}
    return JWTAuthenticator(secret_key, users, token_expiry=1)

def test_successful_authentication(jwt_auth):
    token = jwt_auth.generate_token("alice")
    request = {"Authorization": f"Bearer {token}"}
    assert jwt_auth.authenticate(request) == True

def test_invalid_token(jwt_auth):
    request = {"Authorization": "Bearer invalid_token"}
    with pytest.raises(AuthenticationError):
        jwt_auth.authenticate(request)

def test_expired_token(jwt_auth):
    token = jwt_auth.generate_token("alice")
    time.sleep(2)  # Wait for token to expire
    request = {"Authorization": f"Bearer {token}"}
    with pytest.raises(AuthenticationError):
        jwt_auth.authenticate(request)

def test_missing_authorization_header(jwt_auth):
    request = {}
    with pytest.raises(AuthenticationError):
        jwt_auth.authenticate(request)

def test_invalid_authorization_header(jwt_auth):
    request = {"Authorization": "Invalid header"}
    with pytest.raises(AuthenticationError):
        jwt_auth.authenticate(request)

def test_generate_token_invalid_user(jwt_auth):
    with pytest.raises(AuthenticationError):
        jwt_auth.generate_token("eve")

def test_token_payload(jwt_auth):
    token = jwt_auth.generate_token("alice")
    payload = jwt.decode(token, jwt_auth.secret_key, algorithms=['HS256'])
    assert payload['username'] == "alice"
    assert 'exp' in payload