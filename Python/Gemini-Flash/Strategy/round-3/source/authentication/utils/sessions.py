# Placeholder for session storage (memory or database)
SESSIONS = {}

def create_session(user_id):
    """
    Creates a new session for a user.

    Args:
        user_id: The user's ID.

    Returns:
        str: The session ID.
    """
    session_id = str(user_id)
    SESSIONS[session_id] = user_id
    return session_id

def validate_session(session_id):
    """
    Validates the session ID against the stored sessions.

    Args:
        session_id: The session ID.

    Returns:
        bool: True if the session is valid, False otherwise.
    """
    return session_id in SESSIONS