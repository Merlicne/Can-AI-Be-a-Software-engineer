import uuid

class SessionAuthentication(Authenticator):
    def __init__(self):
        self.sessions = {}

    def authenticate(self, request):
        session_id = request.cookies.get('session_id')
        return session_id in self.sessions

    def login(self, username):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = username
        return session_id