from abc import ABC, abstractmethod

class Authenticator(ABC):
    """
    Abstract base class for authentication strategies.
    """

    @abstractmethod
    def authenticate(self, request):
        """
        Authenticates the given request.

        Args:
            request: The incoming request object.

        Returns:
            The authenticated user object if successful, otherwise None.
        Raises:
            AuthenticationError: If authentication fails.
        """
        pass