import pytest
from auth_strategies.api_key_auth import APIKeyAuth
from flask import Flask, request

app = Flask(__name__)
api_key_auth = APIKeyAuth()

@app.route('/test-api-key-auth', methods=['GET'])
def test_api_key_auth_route():
    try:
        api_key_auth.authenticate(request)
        return "Authenticated", 200
    except Exception as e:
        return str(e), 401

def test_api_key_auth():
    with app.test_client() as client:
        # Test successful authentication with header
        headers = {
            'Authorization': 'key1'
        }
        response = client.get('/test-api-key-auth', headers=headers)
        assert response.status_code == 200

        # Test successful authentication with query parameter
        response = client.get('/test-api-key-auth?api_key=key1')
        assert response.status_code == 200

        # Test missing API key
        response = client.get('/test-api-key-auth')
        assert response.status_code == 401

        # Test invalid API key
        headers = {
            'Authorization': 'invalid'
        }
        response = client.get('/test-api-key-auth', headers=headers)
        assert response.status_code == 401