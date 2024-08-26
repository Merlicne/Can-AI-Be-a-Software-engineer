import jwt

# Secret key for JWT
SECRET_KEY = "your_secret_key"

def generate_jwt(user_id):
    """
    Generates a JWT token for a user.

    Args:
        user_id: The user's ID.

    Returns:
        str: The JWT token.
    """
    payload = {
        "user_id": user_id,
        "exp": 3600
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def validate_jwt(token):
    """
    Validates a JWT token.

    Args:
        token: The JWT token.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return True
    except jwt.InvalidTokenError:
        return False