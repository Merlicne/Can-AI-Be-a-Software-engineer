# tests/test_session_auth.py

import pytest
from authenticators.session_auth import SessionAuthenticator
from storage.in_memory_storage import InMemoryStorage
from utils.exceptions import AuthenticationError

@pytest.fixture
def session_auth():
    users = {"alice": "password123", "bob": "securepass456"}
    storage = InMemoryStorage()
    return SessionAuthenticator(users, storage)

def test_successful_authentication(session_auth):
    request = {"username": "alice", "password": "password123"}
    assert session_auth.authenticate(request) == True
    assert "session_id" in request

def test_failed_authentication(session_auth):
    request = {"username": "alice", "password": "wrongpassword"}
    with pytest.raises(AuthenticationError):
        session_auth.authenticate(request)

def test_successful_session_authentication(session_auth):
    request = {"username": "alice", "password": "password123"}
    session_auth.authenticate(request)
    session_id = request["session_id"]

    new_request = {"session_id": session_id}
    assert session_auth.authenticate(new_request) == True

def test_invalid_session_id(session_auth):
    request = {"session_id": "invalid_session_id"}
    assert session_auth.authenticate(request) == False

def test_missing_credentials(session_auth):
    request = {}
    with pytest.raises(AuthenticationError):
        session_auth.authenticate(request)

def test_nonexistent_user(session_auth):
    request = {"username": "eve", "password": "password123"}
    with pytest.raises(AuthenticationError):
        session_auth.authenticate(request)