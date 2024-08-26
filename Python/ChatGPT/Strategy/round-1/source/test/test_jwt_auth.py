# tests/test_jwt_auth.py
import pytest
import jwt
from flask import Flask, Request
from flask.testing import FlaskClient
from auth_strategies.jwt_auth import JWTAuth, SECRET_KEY
from datetime import datetime, timedelta

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@pytest.fixture
def jwt_auth():
    return JWTAuth()

def create_jwt_token(user_id, jwt_auth):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {
        'user_id': user_id,
        'exp': expiration.timestamp()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def test_valid_jwt_auth(client, jwt_auth):
    token = create_jwt_token('user1', jwt_auth)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = client.get('/secure-endpoint', headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == 'You have access'

def test_invalid_jwt_auth(client, jwt_auth):
    headers = {
        'Authorization': 'Bearer invalid_token'
    }
    response = client.get('/secure-endpoint', headers=headers)
    assert response.status_code == 401
    assert response.json['message'] == 'Unauthorized'
