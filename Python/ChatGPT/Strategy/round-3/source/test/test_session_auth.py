import pytest
from flask import Flask, request, jsonify
from flask.testing import FlaskClient
from auth.session_auth import SessionAuth

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def session_auth():
    return SessionAuth()

def test_session_auth_success(client, session_auth):
    session_auth.create_session('user1')  # Create a session for testing
    response = client.post('/create-session', json={'username': 'user1'})
    session_cookie = response.cookies.get('session_id')

    response = client.get('/login', cookies={'session_id': session_cookie})
    assert response.status_code == 200
    assert response.json['message'] == "Authenticated"

def test_session_auth_failure(client, session_auth):
    response = client.get('/login', cookies={'session_id': 'invalid_session_id'})
    assert response.status_code == 401
    assert response.json['message'] == "Unauthorized"

def test_session_auth_no_cookie(client):
    response = client.get('/login')
    assert response.status_code == 401
    assert response.json['message'] == "Unauthorized"
