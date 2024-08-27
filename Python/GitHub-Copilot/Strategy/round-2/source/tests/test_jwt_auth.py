import pytest
from auth_strategies.jwt_auth import JWTAuth
from flask import Flask, request

app = Flask(__name__)
jwt_auth = JWTAuth()

@app.route('/test-jwt-auth', methods=['GET'])
def test_jwt_auth_route():
    try:
        jwt_auth.authenticate(request)
        return "Authenticated", 200
    except Exception as e:
        return str(e), 401

def test_jwt_auth():
    with app.test_client() as client:
        # Test successful login and authentication
        token = jwt_auth.login('admin', 'password')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = client.get('/test-jwt-auth', headers=headers)
        assert response.status_code == 200

        # Test missing Authorization header
        response = client.get('/test-jwt-auth')
        assert response.status_code == 401

        # Test invalid auth type
        headers = {
            'Authorization': f'Basic {token}'
        }
        response = client.get('/test-jwt-auth', headers=headers)
        assert response.status_code == 401

        # Test invalid token
        headers = {
            'Authorization': 'Bearer invalid'
        }
        response = client.get('/test-jwt-auth', headers=headers)
        assert response.status_code == 401

        # Test expired token
        import time
        time.sleep(2)  # Assuming token expiration is set to 1 second for testing
        response = client.get('/test-jwt-auth', headers=headers)
        assert response.status_code == 401

        # Test invalid login credentials
        with pytest.raises(Exception, match="Invalid credentials"):
            jwt_auth.login('invalid', 'invalid')