# InputHandlingService

Frontend-facing FastAPI service that:
- Exposes API endpoints to receive a user's city input
- Validates the input
- Forwards validated requests to the backend service (InputHandlingService_backend)
- Acts as the user interaction interface
- Provides simple, modular structure for future features (auth, analytics)

No environment variables are required at this time.

## Tech

- FastAPI
- httpx (async) for backend communication
- Uvicorn for local development

## Run locally

From this container root:

```bash
# Option A: python module
python -m src.run

# Option B: uvicorn directly
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Service will be available at: http://localhost:8000

## OpenAPI

To generate the OpenAPI JSON under `interfaces/openapi.json`:

```bash
python -m src.api.generate_openapi
```

Then open the generated file at `interfaces/openapi.json`.

## API

Base path: `/api`

### Health
- GET `/`  
  Returns service health.

Response:
```json
{
  "status": "ok",
  "service": "InputHandlingService"
}
```

### Submit City
- POST `/api/city/submit`
  - Summary: Submit a city
  - Description: Receives a user's city, validates it, and forwards to the backend.
  - Request body:
    - `city` (string, required, non-empty)
  - Query params:
    - `source` (string, optional): e.g., "web", "mobile"
  - Response:
    - `city` (string): original trimmed city
    - `normalized_city` (string): normalized city (from backend or mock)
    - `backend_status` (string): e.g., "ok"
    - `metadata` (object, optional)

Example request:
```bash
curl -X POST "http://localhost:8000/api/city/submit?source=web" \
  -H "Content-Type: application/json" \
  -d '{"city": "  new york  "}'
```

Example response:
```json
{
  "city": "new york",
  "normalized_city": "New York",
  "backend_status": "ok",
  "metadata": {
    "note": "Backend not reachable; returned mock response."
  }
}
```

## Backend integration

This service expects a backend endpoint at:
- Base URL: `http://localhost:8101` (default in code)
- Path: `POST /api/city/process`
- Body: `{ "city": "<string>", "source": "<optional string>" }`
- Response JSON shape (example):
```json
{
  "normalized_city": "New York",
  "status": "ok",
  "metadata": { "confidence": 0.98 }
}
```

If the backend is not available, the service returns a graceful mock response.

## Project structure

```
src/
  api/
    main.py                # FastAPI app factory and health
    generate_openapi.py    # Script to output interfaces/openapi.json
  core/
    settings.py            # App settings (future env integration)
    errors.py              # Global error handlers
  routers/
    city.py                # City endpoints
  schemas/
    city.py                # Pydantic models
  services/
    backend_client.py      # Async HTTP client for backend
  run.py                   # Local dev runner
```

## Notes

- CORS is permissive by default. Restrict origins in `src/core/settings.py` as needed.
- Ready to extend with authentication and analytics through additional routers/dependencies/middleware.
