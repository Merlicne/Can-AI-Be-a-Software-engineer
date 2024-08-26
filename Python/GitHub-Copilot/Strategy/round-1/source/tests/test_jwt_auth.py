# auth_system/tests/test_jwt_auth.py
import pytest
import jwt
from strategies.jwt_auth import JWTAuth

@pytest.fixture
def secret_key():
    return 'your_jwt_secret'

@pytest.fixture
def auth(secret_key):
    return JWTAuth(secret_key)

def test_jwt_auth_success(auth, secret_key):
    token = jwt.encode({'user': 'user1'}, secret_key, algorithm='HS256')
    request = type('Request', (object,), {'headers': {'Authorization': 'Bearer ' + token}})()
    assert auth.authenticate(request) == True

def test_jwt_auth_invalid_token(auth):
    request = type('Request', (object,), {'headers': {'Authorization': 'Bearer invalid_token'}})()
    assert auth.authenticate(request) == False

def test_jwt_auth_no_header(auth):
    request = type('Request', (object,), {'headers': {}})
    assert auth.authenticate(request) == False

def test_jwt_auth_invalid_auth_type(auth, secret_key):
    token = jwt.encode({'user': 'user1'}, secret_key, algorithm='HS256')
    request = type('Request', (object,), {'headers': {'Authorization': 'Basic ' + token}})()
    assert auth.authenticate(request) == False