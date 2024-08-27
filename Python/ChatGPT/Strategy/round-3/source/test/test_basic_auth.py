import pytest
from flask import Flask, request
from flask.testing import FlaskClient
from auth.basic_auth import BasicAuth

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def basic_auth():
    return BasicAuth()

def test_basic_auth_success(client, basic_auth):
    # Use a valid username and password encoded in base64
    auth_header = 'Basic ' + 'dXNlcjE6cGFzc3dvcmQx'  # Base64 encoding of 'user1:password1'
    response = client.get('/login', headers={'Authorization': auth_header})
    assert response.status_code == 200
    assert response.json['message'] == "Authenticated"

def test_basic_auth_failure(client, basic_auth):
    # Use an invalid username and password encoded in base64
    auth_header = 'Basic ' + 'dXNlcjI6aW52YWxpZA=='  # Base64 encoding of 'user2:invalid'
    response = client.get('/login', headers={'Authorization': auth_header})
    assert response.status_code == 401
    assert response.json['message'] == "Unauthorized"

def test_basic_auth_missing_header(client, basic_auth):
    response = client.get('/login')
    assert response.status_code == 401
    assert response.json['message'] == "Unauthorized"
