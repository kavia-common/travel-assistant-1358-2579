from functools import lru_cache
from typing import List


class Settings:
    """
    PUBLIC_INTERFACE
    Application settings. Currently uses sane defaults since .env is empty.
    Add environment variable parsing here in the future if needed.
    """

    def __init__(self) -> None:
        # Base URL for the backend service; adjust when the backend is available.
        # For local dev, you might run backend on http://localhost:8101 for example.
        self.backend_base_url: str = "http://localhost:8101"
        self.backend_timeout_seconds: float = 10.0

        # CORS settings
        self.cors_allow_origins: List[str] = ["*"]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    PUBLIC_INTERFACE
    Cached accessor for application settings.
    """
    return Settings()
