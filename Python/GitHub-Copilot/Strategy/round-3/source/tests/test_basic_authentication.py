import pytest
from auth_strategies.basic_authentication import BasicAuthentication

def test_basic_authentication_success():
    users = {'user1': 'password1'}
    basic_auth = BasicAuthentication(users)
    request = type('Request', (object,), {'headers': {'Authorization': 'Basic dXNlcjE6cGFzc3dvcmQx'}})()
    assert basic_auth.authenticate(request) == True

def test_basic_authentication_no_header():
    users = {'user1': 'password1'}
    basic_auth = BasicAuthentication(users)
    request = type('Request', (object,), {'headers': {}})()
    assert basic_auth.authenticate(request) == False

def test_basic_authentication_invalid_auth_type():
    users = {'user1': 'password1'}
    basic_auth = BasicAuthentication(users)
    request = type('Request', (object,), {'headers': {'Authorization': 'Bearer dXNlcjE6cGFzc3dvcmQx'}})()
    assert basic_auth.authenticate(request) == False

def test_basic_authentication_invalid_credentials():
    users = {'user1': 'password1'}
    basic_auth = BasicAuthentication(users)
    request = type('Request', (object,), {'headers': {'Authorization': 'Basic invalid'}})()
    assert basic_auth.authenticate(request) == False