# tests/test_main.py

import pytest
import base64
from main import authenticate_request, basic_auth, session_auth, jwt_auth, api_key_auth

def test_basic_auth():
    credentials = base64.b64encode(b"alice:password123").decode("utf-8")
    request = {"Authorization": f"Basic {credentials}"}
    assert authenticate_request("basic", request) == True

def test_session_auth():
    request = {"username": "alice", "password": "password123"}
    assert authenticate_request("session", request) == True
    assert "session_id" in request

    session_id = request["session_id"]
    new_request = {"session_id": session_id}
    assert authenticate_request("session", new_request) == True

def test_jwt_auth():
    token = jwt_auth.generate_token("alice")
    request = {"Authorization": f"Bearer {token}"}
    assert authenticate_request("jwt", request) == True

def test_api_key_auth():
    request = {"api_key": "api_key_1"}
    assert authenticate_request("api_key", request) == True

def test_invalid_auth_type():
    with pytest.raises(ValueError):
        authenticate_request("invalid_type", {})

def test_failed_authentication():
    request = {"api_key": "invalid_key"}
    assert authenticate_request("api_key", request) == False