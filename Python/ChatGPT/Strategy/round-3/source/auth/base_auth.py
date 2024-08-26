from abc import ABC, abstractmethod
from flask import request, jsonify

class Authenticator(ABC):
    
    @abstractmethod
    def authenticate(self, request) -> bool:
        pass
