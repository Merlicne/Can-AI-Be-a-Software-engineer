# tests/test_session_auth.py
import pytest
from flask import Flask, Request, session
from flask.testing import FlaskClient
from auth_strategies.session_auth import SessionAuth

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.secret_key = 'super_secret_key'

    with app.test_client() as client:
        yield client

@pytest.fixture
def session_auth(client):
    session_auth = SessionAuth()
    session_auth.create_session('user1')
    return session_auth

def test_valid_session_auth(client, session_auth):
    session_auth.sessions['session_id'] = 'user1'
    response = client.get('/secure-endpoint', cookies={'session_id': 'session_id'})
    assert response.status_code == 200
    assert response.json['message'] == 'You have access'

def test_invalid_session_auth(client):
    response = client.get('/secure-endpoint', cookies={'session_id': 'invalid_session_id'})
    assert response.status_code == 401
    assert response.json['message'] == 'Unauthorized'
