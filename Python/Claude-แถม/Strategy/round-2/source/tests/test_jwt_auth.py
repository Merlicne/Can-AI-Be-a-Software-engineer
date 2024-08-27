import pytest
import jwt
from flask import Request
from auth.jwt_auth import JWTAuthenticator
from datetime import datetime, timedelta

@pytest.fixture
def secret_key():
    return 'test_secret_key'

@pytest.fixture
def users():
    return {
        'user1': 'password1',
        'user2': 'password2'
    }

@pytest.fixture
def jwt_auth(secret_key, users):
    return JWTAuthenticator(secret_key, users)

def test_valid_authentication(jwt_auth):
    token = jwt_auth.generate_token('user1', 'password1')
    headers = {'Authorization': f'Bearer {token}'}
    request = Request.from_values(headers=headers)
    
    assert jwt_auth.authenticate(request) == True

def test_invalid_authentication(jwt_auth):
    headers = {'Authorization': 'Bearer invalid_token'}
    request = Request.from_values(headers=headers)
    
    assert jwt_auth.authenticate(request) == False

def test_missing_authorization_header(jwt_auth):
    request = Request.from_values()
    
    assert jwt_auth.authenticate(request) == False

def test_non_bearer_token(jwt_auth):
    headers = {'Authorization': 'Basic token'}
    request = Request.from_values(headers=headers)
    
    assert jwt_auth.authenticate(request) == False

def test_expired_token(jwt_auth, secret_key):
    payload = {
        'username': 'user1',
        'exp': datetime.utcnow() - timedelta(hours=1)
    }
    expired_token = jwt.encode(payload, secret_key, algorithm='HS256')
    headers = {'Authorization': f'Bearer {expired_token}'}
    request = Request.from_values(headers=headers)
    
    assert jwt_auth.authenticate(request) == False

def test_invalid_signature(jwt_auth):
    payload = {
        'username': 'user1',
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    invalid_token = jwt.encode(payload, 'wrong_secret', algorithm='HS256')
    headers = {'Authorization': f'Bearer {invalid_token}'}
    request = Request.from_values(headers=headers)
    
    assert jwt_auth.authenticate(request) == False

def test_generate_valid_token(jwt_auth):
    token = jwt_auth.generate_token('user1', 'password1')
    assert token is not None
    
    payload = jwt.decode(token, jwt_auth.secret_key, algorithms=['HS256'])
    assert payload['username'] == 'user1'

def test_generate_invalid_token(jwt_auth):
    token = jwt_auth.generate_token('user1', 'wrongpassword')
    assert token is None