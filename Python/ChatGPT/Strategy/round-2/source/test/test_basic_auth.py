import base64
import pytest
from flask import Flask, request
from strategies.basic_auth import BasicAuth

@pytest.fixture
def basic_auth():
    return BasicAuth({'user': 'password'})

def test_valid_credentials(basic_auth):
    auth_header = 'Basic ' + base64.b64encode(b'user:password').decode('utf-8')
    request = Flask(__name__).test_request_context(headers={'Authorization': auth_header})
    assert basic_auth.authenticate(request) == True

def test_invalid_credentials(basic_auth):
    auth_header = 'Basic ' + base64.b64encode(b'user:wrongpassword').decode('utf-8')
    request = Flask(__name__).test_request_context(headers={'Authorization': auth_header})
    assert basic_auth.authenticate(request) == False

def test_missing_authorization_header(basic_auth):
    request = Flask(__name__).test_request_context(headers={})
    assert basic_auth.authenticate(request) == False

def test_invalid_authorization_header(basic_auth):
    auth_header = 'Bearer ' + base64.b64encode(b'user:password').decode('utf-8')
    request = Flask(__name__).test_request_context(headers={'Authorization': auth_header})
    assert basic_auth.authenticate(request) == False
