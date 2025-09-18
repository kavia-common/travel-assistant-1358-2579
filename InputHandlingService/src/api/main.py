from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.settings import get_settings
from src.routers.city import router as city_router
from src.core.errors import add_exception_handlers

# Initialize settings (currently defaults; no env vars required)
settings = get_settings()


def create_app() -> FastAPI:
    """
    Factory to create and configure the FastAPI application.
    """
    app = FastAPI(
        title="InputHandlingService",
        description=(
            "Frontend-facing API that receives a user's city input, validates it, "
            "and forwards it to the backend (InputHandlingService_backend). "
            "Designed to be easily extensible for authentication, analytics, etc."
        ),
        version="1.0.0",
        openapi_tags=[
            {"name": "health", "description": "Service health and meta endpoints"},
            {"name": "city", "description": "City input endpoints for user interaction"},
        ],
    )

    # CORS - currently permissive for simplicity; can be restricted later.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health endpoints
    @app.get("/", tags=["health"], summary="Health check", description="Returns service health status.")
    def health_check():
        """
        PUBLIC_INTERFACE
        Returns service health status to indicate the service is running.
        """
        return {"status": "ok", "service": "InputHandlingService"}

    # Register routers
    app.include_router(city_router, prefix="/api")

    # Errors
    add_exception_handlers(app)

    return app


app = create_app()
