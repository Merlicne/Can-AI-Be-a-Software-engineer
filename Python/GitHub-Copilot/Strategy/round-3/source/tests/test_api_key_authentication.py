import pytest
from auth_strategies.api_key_authentication import APIKeyAuthentication

def test_api_key_authentication_success():
    api_keys = {'valid_api_key'}
    api_key_auth = APIKeyAuthentication(api_keys)
    request = type('Request', (object,), {'headers': {'Authorization': 'valid_api_key'}})()
    assert api_key_auth.authenticate(request) == True

def test_api_key_authentication_no_key():
    api_keys = {'valid_api_key'}
    api_key_auth = APIKeyAuthentication(api_keys)
    request = type('Request', (object,), {'headers': {}})()
    assert api_key_auth.authenticate(request) == False

def test_api_key_authentication_invalid_key():
    api_keys = {'valid_api_key'}
    api_key_auth = APIKeyAuthentication(api_keys)
    request = type('Request', (object,), {'headers': {'Authorization': 'invalid'}})()
    assert api_key_auth.authenticate(request) == False

def test_api_key_authentication_query_param():
    api_keys = {'valid_api_key'}
    api_key_auth = APIKeyAuthentication(api_keys)
    request = type('Request', (object,), {'headers': {}, 'args': {'api_key': 'valid_api_key'}})()
    assert api_key_auth.authenticate(request) == True