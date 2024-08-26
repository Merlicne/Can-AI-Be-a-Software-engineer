import pytest
import base64
from datetime import datetime, timedelta
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from auth_strategies.auth_strategy import AuthenticationStrategy
from auth_strategies.basic_auth import BasicAuthentication
from auth_strategies.session_auth import SessionAuthentication
from auth_strategies.jwt_auth import JWTAuthentication
from auth_strategies.api_key_auth import APIKeyAuthentication

# Mock request object for testing
class MockRequest:
    def __init__(self, headers=None, cookies=None, args=None):
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.args = args or {}

# Generate a test private key for JWT tests
def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key

# Test for AuthenticationStrategy interface
def test_authentication_strategy_interface():
    with pytest.raises(TypeError):
        AuthenticationStrategy()  # Abstract class cannot be instantiated


# Basic Authentication Tests
def test_basic_auth_success():
    users = {"john": "secret1"}
    auth = BasicAuthentication(users)
    request = MockRequest(headers={"Authorization": "Basic " + base64.b64encode("john:secret1".encode("utf-8")).decode("utf-8")})
    assert auth.authenticate(request)

def test_basic_auth_invalid_credentials():
    users = {"john": "secret1"}
    auth = BasicAuthentication(users)
    request = MockRequest(headers={"Authorization": "Basic " + base64.b64encode("john:wrong_password".encode("utf-8")).decode("utf-8")})
    assert not auth.authenticate(request)

def test_basic_auth_missing_credentials():
    users = {"john": "secret1"}
    auth = BasicAuthentication(users)
    request = MockRequest()  # No Authorization header
    assert not auth.authenticate(request)

def test_basic_auth_invalid_auth_header():
    users = {"john": "secret1"}
    auth = BasicAuthentication(users)
    request = MockRequest(headers={"Authorization": "Invalid " + base64.b64encode("john:secret1".encode("utf-8")).decode("utf-8")})
    assert not auth.authenticate(request)


# Session Authentication Tests
def test_session_auth_success():
    auth = SessionAuthentication()
    auth.sessions["valid_session_id"] = True
    request = MockRequest(cookies={"session_id": "valid_session_id"})
    assert auth.authenticate(request)

def test_session_auth_invalid_session():
    auth = SessionAuthentication()
    request = MockRequest(cookies={"session_id": "invalid_session_id"})
    assert not auth.authenticate(request)

def test_session_auth_no_session():
    auth = SessionAuthentication()
    request = MockRequest()  # No session ID in cookies
    assert not auth.authenticate(request)


# JWT Authentication Tests
def test_jwt_auth_success():
    private_key = generate_private_key()
    private_key_path = "test_private_key.pem"
    with open(private_key_path, "wb") as key_file:
        key_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    auth = JWTAuthentication(private_key_path)
    token = auth.generate_token("user123")
    request = MockRequest(headers={"Authorization": f"Bearer {token}"})
    assert auth.authenticate(request)

def test_jwt_auth_invalid_token():
    private_key = generate_private_key()
    private_key_path = "test_private_key.pem"
    with open(private_key_path, "wb") as key_file:
        key_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    auth = JWTAuthentication(private_key_path)
    request = MockRequest(headers={"Authorization": "Bearer invalid_token"})
    assert not auth.authenticate(request)

def test_jwt_auth_expired_token():
    private_key = generate_private_key()
    private_key_path = "test_private_key.pem"
    with open(private_key_path, "wb") as key_file:
        key_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    auth = JWTAuthentication(private_key_path)
    payload = {
        "user_id": "user123",
        "exp": (datetime.utcnow() - timedelta(minutes=1)).timestamp()
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    request = MockRequest(headers={"Authorization": f"Bearer {token}"})
    assert not auth.authenticate(request)

def test_jwt_auth_invalid_auth_header():
    private_key = generate_private_key()
    private_key_path = "test_private_key.pem"
    with open(private_key_path, "wb") as key_file:
        key_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    auth = JWTAuthentication(private_key_path)
    request = MockRequest(headers={"Authorization": "Invalid " + auth.generate_token("user123")})
    assert not auth.authenticate(request)

# API Key Authentication Tests
def test_api_key_auth_success():
    api_keys = {"user1": "key1"}
    auth = APIKeyAuthentication(api_keys)
    request = MockRequest(headers={"Authorization": "key1"})
    assert auth.authenticate(request)

def test_api_key_auth_invalid_key():
    api_keys = {"user1": "key1"}
    auth = APIKeyAuthentication(api_keys)
    request = MockRequest(headers={"Authorization": "invalid_key"})
    assert not auth.authenticate(request)

def test_api_key_auth_missing_key():
    api_keys = {"user1": "key1"}
    auth = APIKeyAuthentication(api_keys)
    request = MockRequest()  # No Authorization header
    assert not auth.authenticate(request)

def test_api_key_auth_key_in_query_param():
    api_keys = {"user1": "key1"}
    auth = APIKeyAuthentication(api_keys)
    request = MockRequest(args={"api_key": "key1"})
    assert auth.authenticate(request)

def test_api_key_auth_invalid_query_param():
    api_keys = {"user1": "key1"}
    auth = APIKeyAuthentication(api_keys)
    request = MockRequest(args={"api_key": "invalid_key"})
    assert not auth.authenticate(request)