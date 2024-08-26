import pytest
from authentication_system.strategies import (
    basic_auth,
    SessionAuthentication,
    JWTAuthentication,
    APIKeyAuthentication,
)
from authentication_system.authenticator import Authenticator
from authentication_system.utils import users, sessions, tokens

class MockRequest:
    def __init__(self, headers=None, cookies=None, args=None):
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.args = args or {}

@pytest.fixture
def basic_auth():
    return BasicAuthentication()

@pytest.fixture
def session_auth():
    return SessionAuthentication()

@pytest.fixture
def jwt_auth():
    return JWTAuthentication()

@pytest.fixture
def api_key_auth():
    return APIKeyAuthentication()

# Basic Authentication Tests

def test_basic_auth_authenticate_success(basic_auth):
    request = MockRequest(headers={'Authorization': 'Basic dXNlcm46cGFzc3dvcmQ='})
    assert basic_auth.authenticate(request) == True

def test_basic_auth_authenticate_missing_header(basic_auth):
    request = MockRequest()
    assert basic_auth.authenticate(request) == False

def test_basic_auth_authenticate_invalid_auth_type(basic_auth):
    request = MockRequest(headers={'Authorization': 'Bearer dXNlcm46cGFzc3dvcmQ='})
    assert basic_auth.authenticate(request) == False

def test_basic_auth_authenticate_invalid_credentials(basic_auth):
    request = MockRequest(headers={'Authorization': 'Basic dXNlcm46cGFzc3dvcmQx'})
    assert basic_auth.authenticate(request) == False

# Session-Based Authentication Tests

def test_session_auth_authenticate_success(session_auth):
    sessions.SESSIONS['1'] = 'user1'
    request = MockRequest(cookies={'session_id': '1'})
    assert session_auth.authenticate(request) == True

def test_session_auth_authenticate_missing_cookie(session_auth):
    request = MockRequest()
    assert session_auth.authenticate(request) == False

def test_session_auth_authenticate_invalid_session_id(session_auth):
    request = MockRequest(cookies={'session_id': '2'})
    assert session_auth.authenticate(request) == False

# JWT Authentication Tests

def test_jwt_auth_authenticate_success(jwt_auth):
    token = tokens.generate_jwt(1)
    request = MockRequest(headers={'Authorization': f'Bearer {token}'})
    assert jwt_auth.authenticate(request) == True

def test_jwt_auth_authenticate_missing_header(jwt_auth):
    request = MockRequest()
    assert jwt_auth.authenticate(request) == False

def test_jwt_auth_authenticate_invalid_token(jwt_auth):
    request = MockRequest(headers={'Authorization': 'Bearer invalid_token'})
    assert jwt_auth.authenticate(request) == False

def test_jwt_auth_authenticate_expired_token(jwt_auth):
    token = tokens.generate_jwt(1, exp=0) # Force expiration
    request = MockRequest(headers={'Authorization': f'Bearer {token}'})
    assert jwt_auth.authenticate(request) == False

# API Key Authentication Tests

def test_api_key_auth_authenticate_success(api_key_auth):
    request = MockRequest(headers={'Authorization': 'key1'})
    assert api_key_auth.authenticate(request) == True

def test_api_key_auth_authenticate_success_query_param(api_key_auth):
    request = MockRequest(args={'api_key': 'key1'})
    assert api_key_auth.authenticate(request) == True

def test_api_key_auth_authenticate_missing_key(api_key_auth):
    request = MockRequest()
    assert api_key_auth.authenticate(request) == False

def test_api_key_auth_authenticate_invalid_key(api_key_auth):
    request = MockRequest(headers={'Authorization': 'invalid_key'})
    assert api_key_auth.authenticate(request) == False

# Utility Functions Tests

def test_decode_credentials():
    encoded_credentials = 'dXNlcm46cGFzc3dvcmQ='
    username, password = users.decode_credentials(encoded_credentials)
    assert username == 'user'
    assert password == 'password'

def test_validate_credentials():
    assert users.validate_credentials('user1', 'password1') == True
    assert users.validate_credentials('user1', 'wrong_password') == False
    assert users.validate_credentials('nonexistent_user', 'password') == False

def test_validate_api_key():
    assert users.validate_api_key('key1') == True
    assert users.validate_api_key('invalid_key') == False

def test_generate_jwt():
    token = tokens.generate_jwt(1)
    assert isinstance(token, str)
    assert 'user_id' in jwt.decode(token, tokens.SECRET_KEY, algorithms=['HS256'])

def test_validate_jwt():
    token = tokens.generate_jwt(1)
    assert tokens.validate_jwt(token) == True
    assert tokens.validate_jwt('invalid_token') == False

def test_create_session():
    session_id = sessions.create_session('user1')
    assert session_id == 'user1'
    assert session_id in sessions.SESSIONS

def test_validate_session():
    sessions.SESSIONS['user1'] = 'user1'
    assert sessions.validate_session('user1') == True
    assert sessions.validate_session('invalid_session_id') == False