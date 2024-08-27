from authentication.authenticator import Authenticator
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from datetime import datetime, timedelta
import jwt

class JWTAuth(Authenticator):
    """
    JWT Authentication strategy.
    """

    def __init__(self, private_key, public_key, token_expiry_minutes=30):
        """
        Initializes the JWTAuth strategy with private and public keys for signing and verifying the token.
        Args:
            private_key: The private key for signing the token.
            public_key: The public key for verifying the token.
            token_expiry_minutes: The token expiry time in minutes.
        """
        self.private_key = load_pem_private_key(private_key, None, default_backend())
        self.public_key = public_key
        self.token_expiry_minutes = token_expiry_minutes

    def authenticate(self, request):
        """
        Authenticates the request using JWT Authentication.
        Args:
            request: The request object.
        Returns:
            bool: True if the request is authenticated, False otherwise.
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(' ')[1]
            try:
                decoded_token = jwt.decode(
                    token,
                    self.public_key,
                    algorithms=['RS256'],
                    options={'verify_exp': True}
                )
                return True
            except jwt.exceptions.ExpiredSignatureError:
                return False
            except jwt.exceptions.InvalidTokenError:
                return False
            except InvalidSignature:
                return False
        return False

    def generate_token(self, user):
        """
        Generates a JWT token for a user.
        Args:
            user: The user object.
        Returns:
            str: The JWT token.
        """
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=self.token_expiry_minutes)
        }
        token = jwt.encode(payload, self.private_key, algorithm='RS256')
        return token.decode('utf-8')