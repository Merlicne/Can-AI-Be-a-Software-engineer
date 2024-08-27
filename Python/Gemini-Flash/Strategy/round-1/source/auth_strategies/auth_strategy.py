from abc import ABC, abstractmethod

class AuthenticationStrategy(ABC):
    """
    Interface for authentication strategies.
    """

    @abstractmethod
    def authenticate(self, request):
        """
        Authenticates the request based on the specific strategy.

        Args:
            request: The incoming request object.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        pass