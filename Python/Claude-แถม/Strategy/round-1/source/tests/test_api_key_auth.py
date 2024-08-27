# tests/test_api_key_auth.py

import pytest
from authenticators.api_key_auth import APIKeyAuthenticator
from utils.exceptions import AuthenticationError

@pytest.fixture
def api_key_auth():
    api_keys = {"api_key_1": "alice", "api_key_2": "bob"}
    return APIKeyAuthenticator(api_keys)

def test_successful_authentication(api_key_auth):
    request = {"api_key": "api_key_1"}
    assert api_key_auth.authenticate(request) == True

def test_failed_authentication(api_key_auth):
    request = {"api_key": "invalid_api_key"}
    assert api_key_auth.authenticate(request) == False

def test_missing_api_key(api_key_auth):
    request = {}
    with pytest.raises(AuthenticationError):
        api_key_auth.authenticate(request)

def test_api_key_in_authorization_header(api_key_auth):
    request = {"Authorization": "ApiKey api_key_2"}
    assert api_key_auth.authenticate(request) == True

def test_invalid_authorization_header(api_key_auth):
    request = {"Authorization": "Bearer api_key_1"}
    assert api_key_auth.authenticate(request) == False