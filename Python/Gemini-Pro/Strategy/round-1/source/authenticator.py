from strategies import (
    BasicAuthStrategy,
    SessionAuthStrategy,
    JWTAuthStrategy,
    APIKeyAuthStrategy,
)

class Authenticator:
    def __init__(self, strategy):
        self.strategy = strategy

    def authenticate(self, request):
        return self.strategy.authenticate(request)

    def set_strategy(self, strategy):
        self.strategy = strategy