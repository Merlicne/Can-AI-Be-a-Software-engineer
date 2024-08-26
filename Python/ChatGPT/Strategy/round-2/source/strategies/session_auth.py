from strategies import Authenticator
from flask import session

class SessionAuth(Authenticator):

    def __init__(self, session_store):
        self.session_store = session_store

    def authenticate(self, request):
        session_id = request.cookies.get('session_id')
        if session_id and self.session_store.get(session_id):
            return True
        return False
