from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from src.schemas.city import CityRequest, CityResponse
from src.services.backend_client import BackendClient, get_backend_client

router = APIRouter(prefix="/city", tags=["city"])


# PUBLIC_INTERFACE
@router.post(
    "/submit",
    response_model=CityResponse,
    summary="Submit a city",
    description="""
Receive a user's city, validate it (non-empty string), and forward the request to the backend
(InputHandlingService_backend). Returns a normalized representation and any backend echo or metadata.
""",
    responses={
        400: {"description": "Invalid city input"},
        502: {"description": "Failed to communicate with backend"},
    },
)
async def submit_city(
    payload: CityRequest,
    source: Optional[str] = None,
    backend: BackendClient = Depends(get_backend_client),
) -> CityResponse:
    """
    PUBLIC_INTERFACE
    Submit a city for processing.

    Parameters:
    - payload: CityRequest body containing the user's city string.
    - source: Optional query parameter to annotate where the request originated (e.g., 'web', 'mobile').
    - backend: Injected backend client used to forward validated requests to the backend service.

    Returns:
    - CityResponse containing normalized city and backend status.

    Raises:
    - HTTPException 400 if the city is invalid after schema validation checks.
    - HTTPException 502 if communication with backend fails.
    """
    # Additional guard (Pydantic already validates string + min length)
    city = payload.city.strip()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City must be a non-empty string.",
        )

    try:
        backend_result = await backend.forward_city(city=city, source=source)
    except Exception as exc:
        # Map to a 502 Bad Gateway to reflect upstream error
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Backend communication failed: {exc}",
        ) from exc

    return CityResponse(
        city=city,
        normalized_city=backend_result.normalized_city,
        backend_status=backend_result.status,
        metadata=backend_result.metadata,
    )
