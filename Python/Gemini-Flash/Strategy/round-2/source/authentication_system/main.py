from strategies import BasicAuthentication, SessionAuthentication, JWTAuthentication, APIKeyAuthentication
from authenticator import Authenticator

def handle_request(request, authentication_strategy):
    """
    Handles a request with the specified authentication strategy.

    Args:
        request: The request object.
        authentication_strategy: The authentication strategy to use.
    """
    if authentication_strategy.authenticate(request):
        print("Authentication successful!")
    else:
        print("Authentication failed!")

if __name__ == "__main__":
    # Mock request object
    class MockRequest:
        def __init__(self, headers, cookies, args):
            self.headers = headers
            self.cookies = cookies
            self.args = args

    # Example usage
    # Basic Authentication
    basic_auth = BasicAuthentication()
    request1 = MockRequest(
        headers={'Authorization': 'Basic dXNlcm46cGFzc3dvcmQ='},
        cookies={},
        args={}
    )
    handle_request(request1, basic_auth)

    # Session-Based Authentication
    session_auth = SessionAuthentication()
    request2 = MockRequest(
        headers={},
        cookies={'session_id': '1'},
        args={}
    )
    handle_request(request2, session_auth)

    # JWT Authentication
    jwt_auth = JWTAuthentication()
    request3 = MockRequest(
        headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjM2MDAwfQ.4uU49m3Qh-sT8_Z1sZ1u0vU4vYc4f_u0qQ_X12b2eQ'},
        cookies={},
        args={}
    )
    handle_request(request3, jwt_auth)

    # API Key Authentication
    api_key_auth = APIKeyAuthentication()
    request4 = MockRequest(
        headers={'Authorization': 'key1'},
        cookies={},
        args={}
    )
    handle_request(request4, api_key_auth)