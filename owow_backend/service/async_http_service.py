from typing import Any, Optional

import httpx

from owow_backend.repository import HTTPRepository


class AsyncHttpxRepository(HTTPRepository):
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def set_base_url(self, base_url: str) -> None:  # type: ignore
        """Change the base URL for API calls."""
        self.base_url = base_url

    async def _make_request(self, method: str, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Make an asynchronous HTTP request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return await self.client.request(method, url, **kwargs)

    async def get(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> httpx.Response:
        """Make an asynchronous GET request."""
        return await self._make_request("GET", endpoint, params=params)

    async def post(
        self,
        endpoint: str,
        data: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> httpx.Response:
        """Make an asynchronous POST request."""
        return await self._make_request("POST", endpoint, data=data, json=json)

    async def put(
        self,
        endpoint: str,
        data: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> httpx.Response:
        """Make an asynchronous PUT request."""
        return await self._make_request("PUT", endpoint, data=data, json=json)

    async def delete(self, endpoint: str) -> httpx.Response:
        """Make an asynchronous DELETE request."""
        return await self._make_request("DELETE", endpoint)

    async def __aenter__(self) -> "AsyncHttpxRepository":
        return self

    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        await self.client.aclose()
