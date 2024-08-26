import base64
import unittest
from unittest.mock import Mock
import pytest
from auth.authenticator import Authenticator
from auth.strategies.basic_auth import BasicAuthenticator
from auth.strategies.session_auth import SessionAuthenticator
from auth.strategies.jwt_auth import JWTAuthenticator
from auth.strategies.api_key_auth import APIKeyAuthenticator
from auth.exceptions import AuthenticationError

# Mock JWT decoding (replace with actual implementation if needed)
def mock_jwt_decode(token):
    if token == "valid.jwt.token":
        return {"user_id": 1}
    else:
        raise Exception("Invalid token")

class TestBasicAuthenticator(unittest.TestCase):
    def test_authenticate_valid_credentials(self):
        request = Mock(headers={'Authorization': 'Basic dXNlcjpwYXNzd29yZA=='})
        authenticator = BasicAuthenticator()
        user = authenticator.authenticate(request)
        assert user['username'] == 'user'

    def test_authenticate_invalid_credentials(self):
        request = Mock(headers={'Authorization': 'Basic invalid'})
        authenticator = BasicAuthenticator()
        with pytest.raises(AuthenticationError):
            authenticator.authenticate(request)

    def test_authenticate_missing_header(self):
        request = Mock(headers={})
        authenticator = BasicAuthenticator()
        with pytest.raises(AuthenticationError):
            authenticator.authenticate(request)

    def test_authenticate_invalid_header_format(self):
        request = Mock(headers={'Authorization': 'InvalidFormat'})
        authenticator = BasicAuthenticator()
        with pytest.raises(AuthenticationError):
            authenticator.authenticate(request)


class TestSessionAuthenticator(unittest.TestCase):
    def test_authenticate_valid_session(self):
        request = Mock()
        session = {'user_id': 1}
        authenticator = SessionAuthenticator()
        user = authenticator.authenticate(request, session)  # Pass session to the method
        assert user['user_id'] == 1

    def test_authenticate_invalid_session(self):
        request = Mock()
        session = {}
        authenticator = SessionAuthenticator()
        with pytest.raises(AuthenticationError):
            authenticator.authenticate(request, session)  # Pass session to the method


class TestJWTAuthenticator(unittest.TestCase):
    def test_authenticate_valid_token(self, monkeypatch):
        monkeypatch.setattr("auth.strategies.jwt_auth.jwt.decode", mock_jwt_decode)
        request = Mock(headers={'Authorization': 'Bearer valid.jwt.token'})
        authenticator = JWTAuthenticator("secret")
        user = authenticator.authenticate(request)
        assert user['user_id'] == 1

    def test_authenticate_invalid_token(self, monkeypatch):
        monkeypatch.setattr("auth.strategies.jwt_auth.jwt.decode", mock_jwt_decode)
        request = Mock(headers={'Authorization': 'Bearer invalid.jwt.token'})
        authenticator = JWTAuthenticator("secret")
        with pytest.raises(AuthenticationError):
            authenticator.authenticate(request)

    def test_authenticate_missing_header(self):
        request = Mock(headers={})
        authenticator = JWTAuthenticator("secret")
        with pytest.raises(AuthenticationError):
            authenticator.authenticate(request)

    def test_authenticate_invalid_header_format(self):
        request = Mock(headers={'Authorization': 'InvalidFormat'})
        authenticator = JWTAuthenticator("secret")
        with pytest.raises(AuthenticationError):
            authenticator.authenticate(request)


class TestAPIKeyAuthenticator(unittest.TestCase):
    def test_authenticate_valid_key(self):
        request = Mock(headers={'Authorization': 'ApiKey valid_api_key'})
        authenticator = APIKeyAuthenticator({"valid_api_key": 1})
        user = authenticator.authenticate(request)
        assert user['user_id'] == 1

    def test_authenticate_invalid_key(self):
        request = Mock(headers={'Authorization': 'ApiKey invalid_api_key'})
        authenticator = APIKeyAuthenticator({"valid_api_key": 1})
        with pytest.raises(AuthenticationError):
            authenticator.authenticate(request)

    def test_authenticate_missing_header(self):
        request = Mock(headers={})
        authenticator = APIKeyAuthenticator({"valid_api_key": 1})
        with pytest.raises(AuthenticationError):
            authenticator.authenticate(request)

    def test_authenticate_invalid_header_format(self):
        request = Mock(headers={'Authorization': 'InvalidFormat'})
        authenticator = APIKeyAuthenticator({"valid_api_key": 1})
        with pytest.raises(AuthenticationError):
            authenticator.authenticate(request)