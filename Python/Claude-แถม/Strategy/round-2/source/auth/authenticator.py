from abc import ABC, abstractmethod
from flask import Request

class Authenticator(ABC):
    @abstractmethod
    def authenticate(self, request: Request) -> bool:
        pass