import pytest
from flask import Request, session
from auth.session_auth import SessionAuthenticator

@pytest.fixture
def users():
    return {
        'user1': 'password1',
        'user2': 'password2'
    }

@pytest.fixture
def session_auth(users):
    return SessionAuthenticator(users)

def test_valid_authentication(session_auth):
    session_id = session_auth.login('user1', 'password1')
    with session.Session() as sess:
        sess['session_id'] = session_id
        request = Request.from_values()
        request.environ['werkzeug.session'] = sess
        
        assert session_auth.authenticate(request) == True

def test_invalid_authentication(session_auth):
    with session.Session() as sess:
        sess['session_id'] = 'invalid_session_id'
        request = Request.from_values()
        request.environ['werkzeug.session'] = sess
        
        assert session_auth.authenticate(request) == False

def test_missing_session_id(session_auth):
    request = Request.from_values()
    request.environ['werkzeug.session'] = session.Session()
    
    assert session_auth.authenticate(request) == False

def test_valid_login(session_auth):
    session_id = session_auth.login('user1', 'password1')
    assert session_id is not None
    assert session_id in session_auth.sessions

def test_invalid_login(session_auth):
    session_id = session_auth.login('user1', 'wrongpassword')
    assert session_id is None

def test_logout(session_auth):
    session_id = session_auth.login('user1', 'password1')
    assert session_id in session_auth.sessions
    
    session_auth.logout(session_id)
    assert session_id not in session_auth.sessions

def test_logout_invalid_session(session_auth):
    session_auth.logout('invalid_session_id')
    # Should not raise an exception