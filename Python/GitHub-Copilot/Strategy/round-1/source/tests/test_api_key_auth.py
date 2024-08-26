# auth_system/tests/test_api_key_auth.py
import pytest
from strategies.api_key_auth import APIKeyAuth
from utils.api_key_store import APIKeyStore

@pytest.fixture
def api_key_store():
    store = APIKeyStore()
    store.api_keys = {'valid_api_key': 'user1'}
    return store

@pytest.fixture
def auth(api_key_store):
    return APIKeyAuth(api_key_store)

def test_api_key_auth_success(auth):
    request = type('Request', (object,), {'headers': {'Authorization': 'valid_api_key'}})()
    assert auth.authenticate(request) == True

def test_api_key_auth_invalid_key(auth):
    request = type('Request', (object,), {'headers': {'Authorization': 'invalid_api_key'}})()
    assert auth.authenticate(request) == False

def test_api_key_auth_no_header(auth):
    request = type('Request', (object,), {'headers': {}})
    assert auth.authenticate(request) == False

def test_api_key_auth_query_param(auth):
    request = type('Request', (object,), {'headers': {}, 'args': {'api_key': 'valid_api_key'}})()
    assert auth.authenticate(request) == True

def test_api_key_auth_invalid_query_param(auth):
    request = type('Request', (object,), {'headers': {}, 'args': {'api_key': 'invalid_api_key'}})()
    assert auth.authenticate(request) == False