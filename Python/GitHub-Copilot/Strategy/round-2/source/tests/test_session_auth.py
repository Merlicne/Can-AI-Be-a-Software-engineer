import pytest
from auth_strategies.session_auth import SessionAuth
from flask import Flask, request

app = Flask(__name__)
session_auth = SessionAuth()

@app.route('/test-session-auth', methods=['GET'])
def test_session_auth_route():
    try:
        session_auth.authenticate(request)
        return "Authenticated", 200
    except Exception as e:
        return str(e), 401

def test_session_auth():
    with app.test_client() as client:
        # Test successful login and authentication
        session_id = session_auth.login('admin', 'password')
        cookies = {
            'session_id': session_id
        }
        response = client.get('/test-session-auth', cookies=cookies)
        assert response.status_code == 200

        # Test missing session ID
        response = client.get('/test-session-auth')
        assert response.status_code == 401

        # Test invalid session ID
        cookies = {
            'session_id': 'invalid'
        }
        response = client.get('/test-session-auth', cookies=cookies)
        assert response.status_code == 401

        # Test invalid login credentials
        with pytest.raises(Exception, match="Invalid credentials"):
            session_auth.login('invalid', 'invalid')