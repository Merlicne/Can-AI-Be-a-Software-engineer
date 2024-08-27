import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from auth_strategies.auth_strategy import AuthenticationStrategy

class JWTAuthentication(AuthenticationStrategy):
    """
    Implements JWT Authentication strategy.
    """

    def __init__(self, private_key_path):
        """
        Initializes the JWTAuthentication strategy with the path to the private key.

        Args:
            private_key_path: Path to the private key file.
        """
        with open(private_key_path, "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

    def generate_token(self, user_id):
        """
        Generates a JWT token for the given user ID.

        Args:
            user_id: The ID of the user.

        Returns:
            str: The generated JWT token.
        """
        payload = {
            "user_id": user_id,
            "exp": (datetime.utcnow() + timedelta(minutes=30)).timestamp(),  # Token expiration in 30 minutes
        }
        return jwt.encode(payload, self.private_key, algorithm="RS256")

    def authenticate(self, request):
        """
        Authenticates the request using JWT Authentication.

        Args:
            request: The incoming request object.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return False

        token = auth_header.split(" ")[1]

        try:
            decoded_token = jwt.decode(token, self.private_key, algorithms=["RS256"])
            return True
        except jwt.InvalidTokenError:
            return False