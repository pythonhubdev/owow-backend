from abc import ABC, abstractmethod
from typing import Any


class HTTPRepository(ABC):
	@abstractmethod
	def set_base_url(self, base_url: str) -> None:
		pass

	@abstractmethod
	def get(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
		pass

	@abstractmethod
	def post(self, endpoint: str, data: dict[str, Any] | None = None, json: dict[str, Any] | None = None) -> Any:
		pass

	@abstractmethod
	def put(self, endpoint: str, data: dict[str, Any] | None = None, json: dict[str, Any] | None = None) -> Any:
		pass

	@abstractmethod
	def delete(self, endpoint: str) -> Any:
		pass
