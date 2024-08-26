# auth_system/authenticators/authenticator_interface.py

from abc import ABC, abstractmethod
from typing import Any, Dict

class AuthenticatorInterface(ABC):
    @abstractmethod
    def authenticate(self, request: Dict[str, Any]) -> bool:
        """
        Authenticate the request.
        
        Args:
            request (Dict[str, Any]): The request object containing authentication information.
        
        Returns:
            bool: True if authentication is successful, False otherwise.
        
        Raises:
            AuthenticationError: If there's an error during the authentication process.
        """
        pass