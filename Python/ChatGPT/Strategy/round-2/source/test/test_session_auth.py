import pytest
from flask import Flask, request, make_response
from strategies.session_auth import SessionAuth

@pytest.fixture
def session_auth():
    return SessionAuth({'valid_session_id': 'user_data'})

def test_valid_session(session_auth):
    request = Flask(__name__).test_request_context(cookies={'session_id': 'valid_session_id'})
    assert session_auth.authenticate(request) == True

def test_invalid_session(session_auth):
    request = Flask(__name__).test_request_context(cookies={'session_id': 'invalid_session_id'})
    assert session_auth.authenticate(request) == False

def test_missing_session_cookie(session_auth):
    request = Flask(__name__).test_request_context(cookies={})
    assert session_auth.authenticate(request) == False
