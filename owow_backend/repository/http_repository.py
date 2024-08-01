from abc import ABC, abstractmethod
from typing import Any, Optional


class HTTPRepository(ABC):
    @abstractmethod
    def set_base_url(self, base_url: str) -> None:
        pass

    @abstractmethod
    def get(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> Any:
        pass

    @abstractmethod
    def post(self, endpoint: str, data: Optional[dict[str, Any]] = None, json: Optional[dict[str, Any]] = None) -> Any:
        pass

    @abstractmethod
    def put(self, endpoint: str, data: Optional[dict[str, Any]] = None, json: Optional[dict[str, Any]] = None) -> Any:
        pass

    @abstractmethod
    def delete(self, endpoint: str) -> Any:
        pass
