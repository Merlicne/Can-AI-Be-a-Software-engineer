import pytest
import jwt
import datetime
from auth_strategies.jwt_authentication import JWTAuthentication

def test_jwt_authentication_success():
    jwt_auth = JWTAuthentication('secret')
    token = jwt_auth.generate_token('user1')
    request = type('Request', (object,), {'headers': {'Authorization': token}})()
    assert jwt_auth.authenticate(request) == True

def test_jwt_authentication_no_token():
    jwt_auth = JWTAuthentication('secret')
    request = type('Request', (object,), {'headers': {}})()
    assert jwt_auth.authenticate(request) == False

def test_jwt_authentication_expired_token():
    jwt_auth = JWTAuthentication('secret')
    payload = {
        'username': 'user1',
        'exp': datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    request = type('Request', (object,), {'headers': {'Authorization': token}})()
    assert jwt_auth.authenticate(request) == False

def test_jwt_authentication_invalid_token():
    jwt_auth = JWTAuthentication('secret')
    request = type('Request', (object,), {'headers': {'Authorization': 'invalid'}})()
    assert jwt_auth.authenticate(request) == False