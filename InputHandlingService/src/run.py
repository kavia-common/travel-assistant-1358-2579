"""
PUBLIC_INTERFACE
Entrypoint for running the InputHandlingService using uvicorn.

Usage:
    python -m src.run
or
    uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
"""
import uvicorn


def main() -> None:
    """
    PUBLIC_INTERFACE
    Start the FastAPI server using uvicorn with auto-reload for development.
    """
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
