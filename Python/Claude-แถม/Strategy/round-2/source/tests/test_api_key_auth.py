import pytest
from flask import Request
from auth.api_key_auth import APIKeyAuthenticator

@pytest.fixture
def api_keys():
    return ['key1', 'key2', 'key3']

@pytest.fixture
def api_key_auth(api_keys):
    return APIKeyAuthenticator(api_keys)

def test_valid_header_authentication(api_key_auth):
    headers = {'X-API-Key': 'key1'}
    request = Request.from_values(headers=headers)
    
    assert api_key_auth.authenticate(request) == True

def test_valid_query_param_authentication(api_key_auth):
    request = Request.from_values(query_string='api_key=key2')
    
    assert api_key_auth.authenticate(request) == True

def test_invalid_api_key(api_key_auth):
    headers = {'X-API-Key': 'invalid_key'}
    request = Request.from_values(headers=headers)
    
    assert api_key_auth.authenticate(request) == False

def test_missing_api_key(api_key_auth):
    request = Request.from_values()
    
    assert api_key_auth.authenticate(request) == False

def test_empty_api_key(api_key_auth):
    headers = {'X-API-Key': ''}
    request = Request.from_values(headers=headers)
    
    assert api_key_auth.authenticate(request) == False

def test_header_priority_over_query_param(api_key_auth):
    headers = {'X-API-Key': 'key1'}
    request = Request.from_values(headers=headers, query_string='api_key=invalid_key')
    
    assert api_key_auth.authenticate(request) == True