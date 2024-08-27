# tests/test_basic_auth.py
import pytest
from flask import Flask, Request
from flask.testing import FlaskClient
from auth_strategies.basic_auth import BasicAuth

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@pytest.fixture
def basic_auth():
    return BasicAuth()

def test_valid_basic_auth(client, basic_auth):
    basic_auth.users = {'user1': 'password1'}
    headers = {
        'Authorization': 'Basic dXNlcjE6cGFzc3dvcmQx'  # base64 encoded 'user1:password1'
    }
    response = client.get('/secure-endpoint', headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == 'You have access'

def test_invalid_basic_auth(client, basic_auth):
    headers = {
        'Authorization': 'Basic invalid_credentials'
    }
    response = client.get('/secure-endpoint', headers=headers)
    assert response.status_code == 401
    assert response.json['message'] == 'Unauthorized'
