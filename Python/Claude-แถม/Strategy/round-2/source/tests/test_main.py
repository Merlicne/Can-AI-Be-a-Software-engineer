import pytest
import json
import base64
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_protected_route_no_auth(client):
    response = client.get('/protected')
    assert response.status_code == 401
    assert json.loads(response.data)['message'] == 'Access denied'

def test_protected_route_basic_auth(client):
    credentials = base64.b64encode(b'user1:password1').decode('utf-8')
    headers = {'Authorization': f'Basic {credentials}'}
    response = client.get('/protected', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Access granted'

def test_protected_route_session_auth(client):
    # First, login to get a session
    login_response = client.post('/login', json={'username': 'user1', 'password': 'password1'})
    assert login_response.status_code == 200
    session_id = json.loads(login_response.data)['session_id']
    
    # Then, access protected route with session
    with client.session_transaction() as sess:
        sess['session_id'] = session_id
    response = client.get('/protected')
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Access granted'

def test_protected_route_jwt_auth(client):
    # First, login to get a JWT token
    login_response = client.post('/login', json={'username': 'user1', 'password': 'password1'})
    assert login_response.status_code == 200
    jwt_token = json.loads(login_response.data)['jwt_token']
    
    # Then, access protected route with JWT token
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = client.get('/protected', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Access granted'

def test_protected_route_api_key_auth(client):
    headers = {'X-API-Key': 'key1'}
    response = client.get('/protected', headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Access granted'

def test_login_valid_credentials(client):
    response = client.post('/login', json={'username': 'user1', 'password': 'password1'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'session_id' in data
    assert 'jwt_token' in data

def test_login_invalid_credentials(client):
    response = client.post('/login', json={'username': 'user1', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert json.loads(response.data)['message'] == 'Invalid credentials'

def test_logout(client):
    # First, login to get a session
    login_response = client.post('/login', json={'username': 'user1', 'password': 'password1'})
    assert login_response.status_code == 200
    session_id = json.loads(login_response.data)['session_id']
    
    # Then, logout
    logout_response = client.post('/logout', json={'session_id': session_id})
    assert logout_response.status_code == 200
    assert json.loads(logout_response.data)['message'] == 'Logged out successfully'
    
    # Verify that the session is no longer valid
    with client.session_transaction() as sess:
        sess['session_id'] = session_id
    response = client.get('/protected')
    assert response.status_code == 401