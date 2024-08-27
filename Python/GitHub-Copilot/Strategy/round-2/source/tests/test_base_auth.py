import pytest
from auth_strategies.base_auth import BaseAuth
from flask import Flask, request

app = Flask(__name__)
base_auth = BaseAuth()

@app.route('/test-base-auth', methods=['GET'])
def test_base_auth_route():
    try:
        base_auth.authenticate(request)
        return "Authenticated", 200
    except Exception as e:
        return str(e), 401

def test_base_auth():
    with app.test_client() as client:
        # Test successful authentication
        headers = {
            'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='  # Base64 for 'admin:password'
        }
        response = client.get('/test-base-auth', headers=headers)
        assert response.status_code == 200

        # Test missing Authorization header
        response = client.get('/test-base-auth')
        assert response.status_code == 401

        # Test invalid auth type
        headers = {
            'Authorization': 'Bearer YWRtaW46cGFzc3dvcmQ='
        }
        response = client.get('/test-base-auth', headers=headers)
        assert response.status_code == 401

        # Test invalid credentials
        headers = {
            'Authorization': 'Basic aW52YWxpZDppbnZhbGlk'  # Base64 for 'invalid:invalid'
        }
        response = client.get('/test-base-auth', headers=headers)
        assert response.status_code == 401