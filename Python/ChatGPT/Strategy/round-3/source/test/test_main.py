import pytest
from flask import Flask, jsonify, request
from flask.testing import FlaskClient
from auth.basic_auth import BasicAuth
from auth.session_auth import SessionAuth
from auth.jwt_auth import JWTAuth
from auth.api_key_auth import APIKeyAuth

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['TESTING'] = True

    # Define routes
    @app.route('/login', methods=['GET'])
    def login():
        if auth.authenticate(request):
            return jsonify(message="Authenticated"), 200
        return jsonify(message="Unauthorized"), 401

    @app.route('/create-session', methods=['POST'])
    def create_session():
        if isinstance(auth, SessionAuth):
            session_id = auth.create_session(request.json.get('username'))
            resp = jsonify(message="Session created")
            resp.set_cookie('session_id', session_id)
            return resp
        return jsonify(message="Not supported"), 400

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def basic_auth():
    return BasicAuth()

@pytest.fixture
def session_auth():
    return SessionAuth()

@pytest.fixture
def jwt_auth():
    return JWTAuth()

@pytest.fixture
def api_key_auth():
    return APIKeyAuth()

def test_login_with_basic_auth(client, basic_auth):
    global auth
    auth = basic_auth
    auth_header = 'Basic ' + 'dXNlcjE6cGFzc3dvcmQx'  # Base64 encoding of 'user1:password1'
    response = client.get('/login', headers={'Authorization': auth_header})
    assert response.status_code == 200
    assert response.json['message'] == "Authenticated"

def test_create_session(client, session_auth):
    global auth
    auth = session_auth
    response = client.post('/create-session', json={'username': 'user1'})
    session_cookie = response.cookies.get('session_id')

    response = client.get('/login', cookies={'session_id': session_cookie})
    assert response.status_code == 200
    assert response.json['message'] == "Authenticated"

def test_login_with_jwt_auth(client, jwt_auth):
    global auth
    auth = jwt_auth
    token = jwt_auth.generate_token('user1')
    response = client.get('/login', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['message'] == "Authenticated"

def test_login_with_api_key_auth(client, api_key_auth):
    global auth
    auth = api_key_auth
    response = client.get('/login', headers={'Authorization': 'apikey123'})
    assert response.status_code == 200
    assert response.json['message'] == "Authenticated"
