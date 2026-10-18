# Backend

## Setup & Run

```bash
uv sync
uv run python seed.py
uv run uvicorn main:app --reload
```

- Server: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Bruno

### Run Existing Collection

```bash
cd ../bruno
npx @usebruno/cli run
```

Or open `bruno/` folder in Bruno Desktop.

### Import OpenAPI into Bruno

CLI:
```bash
npx @usebruno/cli import openapi --source http://127.0.0.1:8000/openapi.json --output ../bruno --collection-name "Video Catalogs API" --collection-format bru --group-by tags
```

GUI:
1. Bruno Desktop -> **Import Collection** -> **OpenAPI V3**
2. URL: `http://127.0.0.1:8000/openapi.json`
