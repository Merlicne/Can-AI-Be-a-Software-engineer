import pytest
from flask import Flask, request
from strategies.api_key_auth import APIKeyAuth

@pytest.fixture
def api_key_auth():
    return APIKeyAuth({'key123', 'key456'})

def test_valid_api_key(api_key_auth):
    request = Flask(__name__).test_request_context(headers={'Authorization': 'key123'})
    assert api_key_auth.authenticate(request) == True

def test_invalid_api_key(api_key_auth):
    request = Flask(__name__).test_request_context(headers={'Authorization': 'invalidkey'})
    assert api_key_auth.authenticate(request) == False

def test_api_key_as_query_param(api_key_auth):
    request = Flask(__name__).test_request_context(query_string={'api_key': 'key123'})
    assert api_key_auth.authenticate(request) == True

def test_missing_api_key(api_key_auth):
    request = Flask(__name__).test_request_context(headers={})
    assert api_key_auth.authenticate(request) == False
