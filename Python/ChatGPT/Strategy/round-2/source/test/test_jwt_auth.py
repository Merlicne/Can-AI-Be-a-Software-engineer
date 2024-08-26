import pytest
import jwt
from flask import Flask, request
from strategies.jwt_auth import JWTAuth

@pytest.fixture
def jwt_auth():
    secret_key = 'supersecretkey'
    return JWTAuth(secret_key)

def test_valid_token(jwt_auth):
    secret_key = 'supersecretkey'
    token = jwt.encode({'some': 'payload'}, secret_key, algorithm='HS256')
    request = Flask(__name__).test_request_context(headers={'Authorization': f'Bearer {token}'})
    assert jwt_auth.authenticate(request) == True

def test_invalid_token(jwt_auth):
    token = 'invalidtoken'
    request = Flask(__name__).test_request_context(headers={'Authorization': f'Bearer {token}'})
    assert jwt_auth.authenticate(request) == False

def test_expired_token(jwt_auth):
    expired_token = jwt.encode({'some': 'payload', 'exp': 0}, 'supersecretkey', algorithm='HS256')
    request = Flask(__name__).test_request_context(headers={'Authorization': f'Bearer {expired_token}'})
    assert jwt_auth.authenticate(request) == False

def test_missing_authorization_header(jwt_auth):
    request = Flask(__name__).test_request_context(headers={})
    assert jwt_auth.authenticate(request) == False
