from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status


def add_exception_handlers(app: FastAPI) -> None:
    """
    PUBLIC_INTERFACE
    Register global exception handlers for consistent error responses.
    """

    @app.exception_handler(ValueError)
    async def value_error_handler(_: Request, exc: ValueError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc) or "Invalid value."},
        )

    @app.exception_handler(Exception)
    async def generic_error_handler(_: Request, exc: Exception):
        # In production, avoid leaking details; log internally instead.
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error."},
        )
