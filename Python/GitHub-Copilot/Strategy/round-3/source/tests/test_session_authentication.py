import pytest
from auth_strategies.session_authentication import SessionAuthentication

def test_session_authentication_success():
    session_auth = SessionAuthentication()
    session_id = session_auth.login('user1')
    request = type('Request', (object,), {'cookies': {'session_id': session_id}})()
    assert session_auth.authenticate(request) == True

def test_session_authentication_no_cookie():
    session_auth = SessionAuthentication()
    request = type('Request', (object,), {'cookies': {}})()
    assert session_auth.authenticate(request) == False

def test_session_authentication_invalid_session():
    session_auth = SessionAuthentication()
    request = type('Request', (object,), {'cookies': {'session_id': 'invalid'}})()
    assert session_auth.authenticate(request) == False