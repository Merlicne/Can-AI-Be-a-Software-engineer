import uuid

class SessionAuth:
    sessions = {}

    def authenticate(self, request):
        session_id = request.cookies.get('session_id')
        if not session_id or session_id not in self.sessions:
            raise Exception("Invalid session")

        return True

    def login(self, username, password):
        # Replace with actual user verification logic
        if username == 'admin' and password == 'password':
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = username
            return session_id
        else:
            raise Exception("Invalid credentials")