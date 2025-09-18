import asyncio
from typing import Optional, Dict, Any

import httpx

from src.core.settings import get_settings
from src.schemas.city import BackendForwardResult


class BackendClient:
    """
    PUBLIC_INTERFACE
    HTTP client wrapper to communicate with the InputHandlingService_backend.
    """

    def __init__(self, base_url: str, timeout_seconds: float = 10.0) -> None:
        """
        Initialize the backend client.

        Args:
            base_url: Base URL of the backend service.
            timeout_seconds: Request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout_seconds

    async def _post_json(self, path: str, json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Helper to POST JSON to backend and return parsed JSON.
        """
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, json=json)
            resp.raise_for_status()
            return resp.json()

    # PUBLIC_INTERFACE
    async def forward_city(self, city: str, source: Optional[str] = None) -> BackendForwardResult:
        """
        Forward the validated city to the backend service.

        Args:
            city: Validated city string.
            source: Optional annotation for request origin.

        Returns:
            BackendForwardResult containing normalized city and status.

        Notes:
            - This assumes the backend exposes POST /api/city/process with JSON body {city, source}
              and responds with JSON containing normalized_city, status, and optional metadata.
            - If the backend is not yet available, a fallback mock is used to keep this service functional.
        """
        payload = {"city": city}
        if source:
            payload["source"] = source

        # Attempt real backend call; if it fails (connection error, 404, etc.), gracefully fallback to mock
        try:
            data = await self._post_json("/api/city/process", json=payload)
            normalized_city = data.get("normalized_city") or city.strip().title()
            status = data.get("status", "ok")
            metadata = data.get("metadata")
            return BackendForwardResult(
                normalized_city=normalized_city,
                status=status,
                metadata=metadata,
            )
        except Exception:
            # Fallback mock response - keeps the container usable without the backend.
            await asyncio.sleep(0)  # yield control
            return BackendForwardResult(
                normalized_city=city.strip().title(),
                status="ok",
                metadata={"note": "Backend not reachable; returned mock response."},
            )


def get_backend_client() -> BackendClient:
    """
    Dependency provider for BackendClient using current settings.
    """
    settings = get_settings()
    return BackendClient(base_url=settings.backend_base_url, timeout_seconds=settings.backend_timeout_seconds)
