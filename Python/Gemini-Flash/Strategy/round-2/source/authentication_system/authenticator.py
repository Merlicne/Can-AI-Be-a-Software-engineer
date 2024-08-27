class Authenticator:
    """
    Interface for Authentication strategies.
    """

    def authenticate(self, request):
        raise NotImplementedError