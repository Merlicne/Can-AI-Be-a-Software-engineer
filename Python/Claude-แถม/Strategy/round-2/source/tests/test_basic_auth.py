import base64
import pytest
from flask import Request
from auth.basic_auth import BasicAuthenticator

@pytest.fixture
def users():
    return {
        'user1': 'password1',
        'user2': 'password2'
    }

@pytest.fixture
def basic_auth(users):
    return BasicAuthenticator(users)

def test_valid_authentication(basic_auth):
    credentials = base64.b64encode(b'user1:password1').decode('utf-8')
    headers = {'Authorization': f'Basic {credentials}'}
    request = Request.from_values(headers=headers)
    
    assert basic_auth.authenticate(request) == True

def test_invalid_authentication(basic_auth):
    credentials = base64.b64encode(b'user1:wrongpassword').decode('utf-8')
    headers = {'Authorization': f'Basic {credentials}'}
    request = Request.from_values(headers=headers)
    
    assert basic_auth.authenticate(request) == False

def test_missing_authorization_header(basic_auth):
    request = Request.from_values()
    
    assert basic_auth.authenticate(request) == False

def test_invalid_authorization_header(basic_auth):
    headers = {'Authorization': 'Invalid'}
    request = Request.from_values(headers=headers)
    
    assert basic_auth.authenticate(request) == False

def test_non_basic_auth_header(basic_auth):
    headers = {'Authorization': 'Bearer token'}
    request = Request.from_values(headers=headers)
    
    assert basic_auth.authenticate(request) == False

def test_invalid_base64_encoding(basic_auth):
    headers = {'Authorization': 'Basic invalid_base64'}
    request = Request.from_values(headers=headers)
    
    assert basic_auth.authenticate(request) == False

def test_missing_colon_in_credentials(basic_auth):
    credentials = base64.b64encode(b'invalidcredentials').decode('utf-8')
    headers = {'Authorization': f'Basic {credentials}'}
    request = Request.from_values(headers=headers)
    
    assert basic_auth.authenticate(request) == False