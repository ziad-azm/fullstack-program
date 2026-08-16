# Week 4 — Tickets Mini Module (final assignment)

One small feature delivered end-to-end: **support/task tickets**, with a FastAPI +
PostgreSQL backend and an Angular frontend talking to it over HTTP.

Create a ticket, list them, filter by status, change a ticket's status, and delete
it — every action goes through the real API and is reflected in the list.

```
Week4/
├─ tickets-backend/     # FastAPI + PostgreSQL — full CRUD on /tickets
├─ tickets-frontend/    # Angular — list + filter + create form + row actions
├─ HOW_TO_RUN.md        # setup + startup runbook, troubleshooting
└─ README.md            # this file
```

## The feature

A ticket is `{ id, title, description, status, priority, created_at }`, where
`status` is `open | in_progress | closed` (default `open`) and `priority` is
`low | medium | high` (default `medium`). `id` and `created_at` are
server-generated.

| Method   | Path            | Behaviour                                   |     Success code      |
| -------- | --------------- | ------------------------------------------- | :-------------------: |
| `POST`   | `/tickets`      | Create a ticket                              |     `201` / `400`     |
| `GET`    | `/tickets`      | List all tickets; optional `?status=` filter |         `200`         |
| `GET`    | `/tickets/{id}` | Get one                                      |     `200` / `404`     |
| `PATCH`  | `/tickets/{id}` | Update (e.g. change status)                  | `200` / `404` / `400` |
| `DELETE` | `/tickets/{id}` | Delete                                       |     `204` / `404`     |

Validation errors come back as `{ "detail": [ { "field", "message" } ] }` with a
`400` (a custom `RequestValidationError` handler replaces FastAPI's default `422`);
a missing id returns `404 { "detail": "Ticket <id> not found" }`.

## How to run both together

Two terminals, backend first. Step-by-step setup, the test commands, and a
troubleshooting table are in [HOW_TO_RUN.md](HOW_TO_RUN.md).

```bash
# 1. backend  →  http://localhost:8000  (docs at /docs)
cd Week4/tickets-backend
python -m venv venv
source venv/Scripts/activate          # PowerShell: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                  # set DATABASE_URL, then: createdb ticketsdb
uvicorn app.main:app --reload

# 2. frontend  →  http://localhost:4200
cd Week4/tickets-frontend
npm install
ng serve
```

The `tickets` table is created on startup, so there is no migration step. The
backend allows `http://localhost:4200` via `ALLOWED_ORIGINS` in `.env`, which is
what lets the browser call it from the Angular dev server.

Details live in the two sub-READMEs:
[tickets-backend/README.md](tickets-backend/README.md) (env, endpoints, curl
examples, test evidence) and
[tickets-frontend/README.md](tickets-frontend/README.md) (screens, CORS note,
tests).

## Testing evidence

- **Backend** — `pytest`: **19 passed**. `tests/test_tickets.py` runs against the
  real database and covers create (defaults, explicit values), the validation
  failures (missing / blank / over-long title, invalid status, malformed JSON,
  explicit null), list, `?status=` filter, get, patch, and delete — including the
  `404` and `400` paths. A full curl transcript is in the backend README.
- **Frontend** — `ng test`: **12 passed**, covering the list (loading, empty,
  error, filter, patch, delete) and the reactive form (validation gating, payload,
  clearing on success, surfacing API errors) with `HttpTestingController`.
- **End-to-end** — the running Angular app was driven in a headless browser
  against the live API: the list loads real tickets, the form creates one (and
  stays disabled for an empty or whitespace-only title), the status dropdown
  patches and the list refreshes, the filter shows/hides the right rows, delete
  removes the ticket, and stopping the API shows the load-error message.

That end-to-end pass caught one real bug: because `@for`-generated `<option>`s are
created after the `<select>`'s own bindings run, `[value]="ticket.status"` was
being dropped and every row's dropdown showed "Open" regardless of the ticket's
actual status. Marking the option instead (`[selected]="option === ticket.status"`)
fixed it, and a unit test now guards it.

## AI usage note

AI (Claude) was used as a pair-programming assistant throughout this week:

- Scaffolding the FastAPI app and the Angular components from the spec, following
  the same structure and conventions as the Week 2 and Week 3 projects.
- Talking through design details — turning FastAPI's `422` into the required `400`
  shape, using Enums for `status`/`priority`, keeping every query parameterized,
  and where to put the create form relative to the list.
- Writing the first draft of the pytest and Angular test suites, and this
  documentation.

Everything was reviewed and run before being committed: the backend test suite and
the Angular test suite both pass, the endpoints were exercised by hand with curl
(transcript in the backend README), and the two apps were run together and driven
in a browser. The `<select>` binding bug above is a good example of why — it was
found by running the real thing, not by reading the generated code.
