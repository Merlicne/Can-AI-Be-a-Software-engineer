# auth_system/tests/test_session_auth.py
import pytest
from strategies.session_auth import SessionAuth
from utils.session_store import SessionStore

@pytest.fixture
def session_store():
    store = SessionStore()
    store.sessions = {'valid_session_id': 'user1'}
    return store

@pytest.fixture
def auth(session_store):
    return SessionAuth(session_store)

def test_session_auth_success(auth):
    request = type('Request', (object,), {'cookies': {'session_id': 'valid_session_id'}})()
    assert auth.authenticate(request) == True

def test_session_auth_invalid_session(auth):
    request = type('Request', (object,), {'cookies': {'session_id': 'invalid_session_id'}})()
    assert auth.authenticate(request) == False

def test_session_auth_no_cookie(auth):
    request = type('Request', (object,), {'cookies': {}})
    assert auth.authenticate(request) == False