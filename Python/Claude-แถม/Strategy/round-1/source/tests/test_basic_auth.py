# tests/test_basic_auth.py

import pytest
import base64
from authenticators.basic_auth import BasicAuthenticator
from utils.exceptions import AuthenticationError

@pytest.fixture
def basic_auth():
    users = {"alice": "password123", "bob": "securepass456"}
    return BasicAuthenticator(users)

def test_successful_authentication(basic_auth):
    credentials = base64.b64encode(b"alice:password123").decode("utf-8")
    request = {"Authorization": f"Basic {credentials}"}
    assert basic_auth.authenticate(request) == True

def test_failed_authentication(basic_auth):
    credentials = base64.b64encode(b"alice:wrongpassword").decode("utf-8")
    request = {"Authorization": f"Basic {credentials}"}
    assert basic_auth.authenticate(request) == False

def test_missing_authorization_header(basic_auth):
    request = {}
    with pytest.raises(AuthenticationError):
        basic_auth.authenticate(request)

def test_invalid_authorization_header(basic_auth):
    request = {"Authorization": "Invalid header"}
    with pytest.raises(AuthenticationError):
        basic_auth.authenticate(request)

def test_nonexistent_user(basic_auth):
    credentials = base64.b64encode(b"eve:password123").decode("utf-8")
    request = {"Authorization": f"Basic {credentials}"}
    assert basic_auth.authenticate(request) == False