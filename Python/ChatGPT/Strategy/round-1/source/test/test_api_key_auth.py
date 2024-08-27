# tests/test_api_key_auth.py
import pytest
from flask import Flask, Request
from flask.testing import FlaskClient
from auth_strategies.api_key_auth import APIKeyAuth

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@pytest.fixture
def api_key_auth():
    return APIKeyAuth()

def test_valid_api_key_auth(client, api_key_auth):
    api_key_auth.api_keys = {'key1': 'user1'}
    headers = {
        'Authorization': 'key1'
    }
    response = client.get('/secure-endpoint', headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == 'You have access'

def test_invalid_api_key_auth(client, api_key_auth):
    headers = {
        'Authorization': 'invalid_key'
    }
    response = client.get('/secure-endpoint', headers=headers)
    assert response.status_code == 401
    assert response.json['message'] == 'Unauthorized'
