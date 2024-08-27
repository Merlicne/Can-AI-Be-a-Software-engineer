import pytest
import jwt
from flask import Flask, request
from flask.testing import FlaskClient
from auth.jwt_auth import JWTAuth

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
def jwt_auth():
    return JWTAuth()

def test_jwt_auth_success(client, jwt_auth):
    token = jwt_auth.generate_token('user1')
    response = client.get('/login', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['message'] == "Authenticated"

def test_jwt_auth_failure(client, jwt_auth):
    invalid_token = 'invalid_token'
    response = client.get('/login', headers={'Authorization': f'Bearer {invalid_token}'})
    assert response.status_code == 401
    assert response.json['message'] == "Unauthorized"

def test_jwt_auth_missing_token(client, jwt_auth):
    response = client.get('/login')
    assert response.status_code == 401
    assert response.json['message'] == "Unauthorized"
