# auth_system/tests/test_base_auth.py
import base64
import pytest
from strategies.base_auth import BasicAuth

@pytest.fixture
def users():
    return {'user1': 'password1'}

@pytest.fixture
def auth(users):
    return BasicAuth(users)

def test_basic_auth_success(auth):
    request = type('Request', (object,), {'headers': {'Authorization': 'Basic ' + base64.b64encode(b'user1:password1').decode('utf-8')}})()
    assert auth.authenticate(request) == True

def test_basic_auth_invalid_password(auth):
    request = type('Request', (object,), {'headers': {'Authorization': 'Basic ' + base64.b64encode(b'user1:wrongpassword').decode('utf-8')}})()
    assert auth.authenticate(request) == False

def test_basic_auth_no_header(auth):
    request = type('Request', (object,), {'headers': {}})
    assert auth.authenticate(request) == False

def test_basic_auth_invalid_auth_type(auth):
    request = type('Request', (object,), {'headers': {'Authorization': 'Bearer ' + base64.b64encode(b'user1:password1').decode('utf-8')}})()
    assert auth.authenticate(request) == False