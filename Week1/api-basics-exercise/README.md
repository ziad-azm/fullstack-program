# API Basics Exercise — FastAPI

A minimal REST API built for the Week 1 practical exercise. It demonstrates the core backend basics in one small file.

## What it demonstrates
| Concept | Where |
|---------|-------|
| Routing | `@app.get` / `@app.post` decorators |
| Models / schemas | `ItemIn` / `ItemOut` (Pydantic) |
| Validation | `Field(..., min_length=1, gt=0)` on the schema |
| API development | `/items` resource: list, get one, create |
| Error handling | `HTTPException` (404) + clean `400` on validation |

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/items` | List all items |
| `GET` | `/items/{id}` | Get one item (404 if missing) |
| `POST` | `/items` | Create an item (400 on validation error) |

Storage is an in-memory list — no database needed, so it runs anywhere. Data resets when the server restarts.

## Setup & run
```bash
python3 -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
- API: `http://localhost:8000`
- Interactive docs (Swagger): `http://localhost:8000/docs`

## Try it
```bash
# create an item
curl -X POST localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Notebook","price":25.5,"in_stock":true}'

# list items
curl localhost:8000/items

# get one
curl localhost:8000/items/1

# validation error (empty name, negative price -> 400)
curl -X POST localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"","price":-5}'

# not found -> 404
curl localhost:8000/items/999
```

## Verified behaviour
- `GET /items` → `200` with the list
- `POST /items` (valid) → `201` with the created item
- `POST /items` (invalid) → `400` with `{ "detail": [{ "field", "message" }] }`
- `GET /items/{id}` (missing) → `404`
