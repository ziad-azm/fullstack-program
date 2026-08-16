# Tickets API (FastAPI)

The backend for the Week 4 Tickets mini module: full CRUD over `/tickets`, with
Pydantic validation, PostgreSQL storage, and CORS for the Angular frontend.

## 1. Set up the database

Create the Postgres database (adjust host/user as needed):

```bash
createdb ticketsdb
```

Copy the example env file and set your connection string:

```bash
cp .env.example .env
# then edit .env, e.g.:
# DATABASE_URL=postgresql://user:password@localhost:5432/ticketsdb
# ALLOWED_ORIGINS=http://localhost:4200
```

The `tickets` table is created automatically on startup (`CREATE TABLE IF NOT EXISTS`
inside the FastAPI lifespan hook) — no manual migration needed:

| Column        | Type                              |
| ------------- | --------------------------------- |
| `id`          | `SERIAL PRIMARY KEY`              |
| `title`       | `VARCHAR(150) NOT NULL`           |
| `description` | `TEXT`                            |
| `status`      | `VARCHAR(20) NOT NULL`            |
| `priority`    | `VARCHAR(20) NOT NULL`            |
| `created_at`  | `TIMESTAMPTZ NOT NULL DEFAULT now()` |

All queries are parameterized (`%s`) — no string-interpolated values.

## 2. Install dependencies and run

```bash
python -m venv venv
source venv/Scripts/activate      # Windows Git Bash; PowerShell: venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

The API runs on **http://localhost:8000**. Interactive docs (Swagger UI) are at
**http://localhost:8000/docs**.

## The Ticket resource

```jsonc
{
  "id": 1,                       // server-generated
  "title": "Printer is jammed",  // required, 1–150 chars
  "description": "2nd floor",    // optional, max 2000 chars
  "status": "open",              // open | in_progress | closed   (default: open)
  "priority": "high",            // low | medium | high           (default: medium)
  "created_at": "2026-08-16T22:03:51.948440+03:00"
}
```

## Endpoints

| Method   | Path            | Behaviour                                                    |     Success code      |
| -------- | --------------- | ------------------------------------------------------------ | :-------------------: |
| `POST`   | `/tickets`      | Create a ticket; `400` on validation error                    |     `201` / `400`     |
| `GET`    | `/tickets`      | List all tickets; optional `?status=` filter                  |         `200`         |
| `GET`    | `/tickets/{id}` | Get one; `404` if missing                                     |     `200` / `404`     |
| `PATCH`  | `/tickets/{id}` | Update (e.g. change status); `404` if missing, `400` on invalid | `200` / `404` / `400` |
| `DELETE` | `/tickets/{id}` | Delete; `404` if missing                                      |     `204` / `404`     |

### Error shapes

Validation errors (a custom `RequestValidationError` handler turns FastAPI's
default `422` into `400`):

```json
{ "detail": [{ "field": "title", "message": "title is required" }] }
```

Missing resource:

```json
{ "detail": "Ticket 9999 not found" }
```

## curl examples

The commands below are written for bash (Git Bash on Windows). In PowerShell the
inner double quotes get stripped from `-d`, so put the JSON body in a file and use
`-d "@body.json"` instead.

**Create**

```bash
curl -i -X POST http://localhost:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{"title": "Printer is jammed", "description": "2nd floor printer will not feed paper", "priority": "high"}'
# 201 Created
```

**List, and filter by status**

```bash
curl -i http://localhost:8000/tickets
curl -i "http://localhost:8000/tickets?status=in_progress"
# 200 OK
```

**Get one**

```bash
curl -i http://localhost:8000/tickets/1
# 200 OK
```

**Change the status**

```bash
curl -i -X PATCH http://localhost:8000/tickets/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
# 200 OK
```

**Delete**

```bash
curl -i -X DELETE http://localhost:8000/tickets/1
# 204 No Content
```

## Tests

`tests/test_tickets.py` covers create / list / filter / get / patch / delete plus the
validation and 404 paths. The tests run against the real database in `DATABASE_URL`
(they clean up every row they create), so PostgreSQL must be running:

```bash
pytest
```

Result:

```
...................                                                      [100%]
19 passed, 1 warning in 2.88s
```

## Manual testing evidence

Recorded against a live `uvicorn app.main:app` on 2026-08-16 (bodies trimmed for width):

```
### CREATE (expect 201)
{"id":10,"title":"Printer is jammed","description":"2nd floor printer will not feed paper","status":"open","priority":"high","created_at":"2026-08-16T22:03:51.948440+03:00"}
HTTP 201

### CREATE with defaults (expect 201)
{"id":11,"title":"VPN drops every hour","description":null,"status":"open","priority":"medium",...}
HTTP 201

### CREATE missing title (expect 400)
{"detail":[{"field":"title","message":"title is required"}]}
HTTP 400

### CREATE blank title (expect 400)
{"detail":[{"field":"title","message":"title must not be empty"}]}
HTTP 400

### CREATE invalid status (expect 400)
{"detail":[{"field":"status","message":"status must be one of 'open', 'in_progress' or 'closed'"}]}
HTTP 400

### CREATE malformed JSON (expect 400)
{"detail":[{"field":"body","message":"request body must be valid JSON"}]}
HTTP 400

### GET one (expect 200)
{"id":10,"title":"Printer is jammed",...,"status":"open","priority":"high"}
HTTP 200

### GET missing (expect 404)
{"detail":"Ticket 9999 not found"}
HTTP 404

### PATCH status (expect 200)
{"id":10,...,"status":"in_progress","priority":"high"}
HTTP 200

### PATCH missing (expect 404)
{"detail":"Ticket 9999 not found"}
HTTP 404

### PATCH invalid status (expect 400)
{"detail":[{"field":"status","message":"status must be one of 'open', 'in_progress' or 'closed'"}]}
HTTP 400

### PATCH title:null (expect 400)
{"detail":[{"field":"title","message":"title must not be null"}]}
HTTP 400

### FILTER ?status=in_progress (expect 200)
[{"id":10,...,"status":"in_progress"}]
HTTP 200

### FILTER ?status=open (expect 200)
[{"id":11,...,"status":"open"}]
HTTP 200

### FILTER ?status=bogus (expect 400)
{"detail":[{"field":"status","message":"status must be one of 'open', 'in_progress' or 'closed'"}]}
HTTP 400

### DELETE (expect 204)
HTTP/1.1 204 No Content

### DELETE missing (expect 404)
{"detail":"Ticket 9999 not found"}
HTTP 404

### CORS preflight from :4200 (expect 200)
HTTP/1.1 200 OK
access-control-allow-origin: http://localhost:4200
access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
HTTP 200
```

## Project structure

```
app/
├─ main.py               # FastAPI instance, CORS, lifespan, validation handler
├─ config.py             # DATABASE_URL + ALLOWED_ORIGINS from .env
├─ database.py           # psycopg connection + init_db()
├─ schemas.py            # TicketIn, TicketUpdate, TicketOut, status/priority enums
└─ routers/tickets.py    # CRUD routes
tests/test_tickets.py    # end-to-end CRUD tests
```
