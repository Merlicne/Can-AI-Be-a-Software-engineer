from abc import ABC, abstractmethod

class Authenticator(ABC):
    """
    Abstract class defining the interface for authentication strategies.
    """

    @abstractmethod
    def authenticate(self, request):
        """
        Authenticates the request based on the specific strategy.
        Args:
            request: The request object.
        Returns:
            bool: True if the request is authenticated, False otherwise.
        """
        pass