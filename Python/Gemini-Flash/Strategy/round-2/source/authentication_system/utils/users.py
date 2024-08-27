import base64

# Placeholder for user database or storage
USERS = {
    "user1": {"password": "password1", "api_key": "key1"},
    "user2": {"password": "password2", "api_key": "key2"},
}

def decode_credentials(encoded_credentials):
    """
    Decodes Base64 encoded credentials.

    Args:
        encoded_credentials: Base64 encoded username and password.

    Returns:
        tuple: (username, password)
    """
    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    username, password = decoded_credentials.split(':', 1)
    return username, password

def validate_credentials(username, password):
    """
    Validates user credentials against the stored database.

    Args:
        username: The username.
        password: The password.

    Returns:
        bool: True if credentials are valid, False otherwise.
    """
    user = USERS.get(username)
    if user and user["password"] == password:
        return True
    return False

def validate_api_key(api_key):
    """
    Validates the API key against the stored database.

    Args:
        api_key: The API key.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    for user in USERS.values():
        if user["api_key"] == api_key:
            return True
    return False