from typing import Dict, Optional
from pydantic import BaseModel, Field


class CityRequest(BaseModel):
    """
    PUBLIC_INTERFACE
    Request payload for city submission.
    """
    city: str = Field(..., min_length=1, description="Name of the city provided by the user.")


class BackendForwardResult(BaseModel):
    """
    PUBLIC_INTERFACE
    Internal schema representing the result returned from the backend service.
    """
    normalized_city: str = Field(..., description="Normalized/standardized city name as determined by backend.")
    status: str = Field(..., description="Backend processing status, e.g., 'ok'.")
    metadata: Optional[Dict] = Field(default=None, description="Additional metadata returned by backend.")


class CityResponse(BaseModel):
    """
    PUBLIC_INTERFACE
    Response payload returned to the client after forwarding to backend.
    """
    city: str = Field(..., description="Original city as provided by the user (trimmed).")
    normalized_city: str = Field(..., description="Normalized city returned by backend.")
    backend_status: str = Field(..., description="Backend processing status.")
    metadata: Optional[Dict] = Field(default=None, description="Optional metadata returned by backend.")
