import pytest
from flask import Flask, request
from flask.testing import FlaskClient
from auth.api_key_auth import APIKeyAuth

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def api_key_auth():
    return APIKeyAuth()

def test_api_key_auth_success(client, api_key_auth):
    response = client.get('/login', headers={'Authorization': 'apikey123'})
    assert response.status_code == 200
    assert response.json['message'] == "Authenticated"

def test_api_key_auth_failure(client, api_key_auth):
    response = client.get('/login', headers={'Authorization': 'invalid_api_key'})
    assert response.status_code == 401
    assert response.json['message'] == "Unauthorized"

def test_api_key_auth_missing_key(client, api_key_auth):
    response = client.get('/login')
    assert response.status_code == 401
    assert response.json['message'] == "Unauthorized"
