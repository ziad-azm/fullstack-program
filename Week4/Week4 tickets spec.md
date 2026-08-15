# Week 4 — Final Assignment (Build Spec): Tickets Mini Module

## Context

- My primary stack is Node.js (Express/NestJS); for this program I built the backend in **FastAPI (Python) + PostgreSQL** and the frontend in **Angular**.
- This is the final assignment: one small feature delivered **end-to-end** (backend + frontend + API integration + validation + error handling + docs).
- Feature chosen: **Tickets Mini Module** — create support/task tickets, list them, view one, update status, and delete.

## Goal

A working Tickets feature: a FastAPI backend with full CRUD for tickets stored in PostgreSQL, and an Angular frontend to create, list, filter, update status, and delete tickets — connected end-to-end.

## Folder structure to produce

```
week4/
├─ tickets-backend/            # FastAPI + PostgreSQL
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ main.py               # FastAPI instance, router, validation handler, CORS, lifespan
│  │  ├─ config.py             # loads DATABASE_URL from .env
│  │  ├─ database.py           # psycopg connection + init_db()
│  │  ├─ schemas.py            # TicketIn, TicketUpdate, TicketOut
│  │  └─ routers/
│  │     ├─ __init__.py
│  │     └─ tickets.py         # CRUD routes
│  ├─ requirements.txt
│  ├─ .env.example
│  ├─ .gitignore
│  └─ README.md
├─ tickets-frontend/           # Angular app
│  └─ src/app/
│     ├─ models/ticket.model.ts
│     ├─ services/ticket.service.ts
│     └─ components/
│        ├─ ticket-list/       # list + filter by status
│        └─ ticket-form/       # create form
└─ README.md                   # top-level: how to run both together
```

## The Ticket resource

```ts
{
  id: number;
  title: string;
  description: string;
  status: "open" | "in_progress" | "closed";
  priority: "low" | "medium" | "high";
  created_at: string;
}
```

Create body: `{ title, description?, status?, priority? }`

- `status` defaults to `"open"`, `priority` defaults to `"medium"`.
- `id` and `created_at` are server-generated.

## Backend — FastAPI (`tickets-backend/`)

**Endpoints (full CRUD):**

| Method   | Path            | Behaviour                                                   |     Success code      |
| -------- | --------------- | ----------------------------------------------------------- | :-------------------: |
| `POST`   | `/tickets`      | Create a ticket; 400 on validation error                    |     `201` / `400`     |
| `GET`    | `/tickets`      | List all tickets; optional `?status=` filter                |         `200`         |
| `GET`    | `/tickets/{id}` | Get one; 404 if missing                                     |     `200` / `404`     |
| `PATCH`  | `/tickets/{id}` | Update (e.g. change status); 404 if missing, 400 on invalid | `200` / `404` / `400` |
| `DELETE` | `/tickets/{id}` | Delete; 404 if missing                                      |     `204` / `404`     |

**Requirements:**

- **Routing:** FastAPI decorators via an `APIRouter`.
- **Schemas (Pydantic):** `TicketIn`, `TicketUpdate` (all fields optional for PATCH), `TicketOut`.
- **Validation:**
  - `title`: required, non-empty, max 150 chars
  - `description`: optional string, max 2000 chars
  - `status`: one of `open` / `in_progress` / `closed` (use an Enum) — default `open`
  - `priority`: one of `low` / `medium` / `high` (Enum) — default `medium`
  - Invalid input → `400` with `{ "detail": [ { "field", "message" } ] }` (custom RequestValidationError handler)
- **Error handling:** missing id → `404` `{ "detail": "Ticket <id> not found" }`; bad JSON → `400`; delete → `204`.
- **Database (PostgreSQL):** psycopg, `DATABASE_URL` from `.env` (python-dotenv), `.env.example` + `.gitignore`. Create the `tickets` table on startup. Columns: `id SERIAL PK`, `title VARCHAR(150)`, `description TEXT`, `status VARCHAR(20)`, `priority VARCHAR(20)`, `created_at TIMESTAMPTZ DEFAULT now()`. Parameterized queries (`%s`) only.
- **CORS:** allow `http://localhost:4200` (Angular dev server) via `CORSMiddleware`.
- **requirements.txt:** fastapi, uvicorn, psycopg[binary], python-dotenv.
- **Basic test or manual testing evidence:** either a small pytest file covering create/list/get/patch/delete, or a documented set of curl checks in the README.

## Frontend — Angular (`tickets-frontend/`)

- **Model** (`ticket.model.ts`): a `Ticket` interface + a `TicketCreate` type.
- **Service** (`ticket.service.ts`): `HttpClient` calls — `getTickets(status?)`, `getTicket(id)`, `createTicket(payload)`, `updateStatus(id, status)`, `deleteTicket(id)`. Base URL in one place.
- **Ticket list** (`ticket-list`):
  - Loads tickets on init, with a **loading state** and **error handling**.
  - Shows title, status, priority, created date.
  - **Filter** by status (a dropdown: all / open / in_progress / closed).
  - Each ticket has actions: change status (e.g. a dropdown or buttons) and delete.
  - Refreshes after create / update / delete.
- **Ticket form** (`ticket-form`):
  - **Reactive form**: `title` (required), `description` (optional), `priority` (select).
  - **Validation messages** per field; submit disabled while invalid/submitting.
  - On submit: create the ticket, show loading, handle success (clear form, refresh list) and error.
- **Routing:** list is the default route; form on the same page or `/new`.

## Documentation (required by the assignment)

- **Backend README:** setup `.env` + database, run (`uvicorn app.main:app --reload`), endpoint list, curl examples, and the testing evidence.
- **Frontend README:** `npm install`, `ng serve`, note that the backend must be running, CORS note.
- **Top-level `week4/README.md`:** what the feature is, how to run both together, and a short **AI usage note** (how AI was used, and that all code was reviewed and tested).

## Definition of done

- Backend runs on `http://localhost:8000`; all CRUD endpoints + filter return correct status codes (create 201, invalid 400, get 200/404, patch 200/404, delete 204/404, `?status=` filter works).
- Frontend runs on `http://localhost:4200`, loads tickets from the live API with loading/error states, creates a ticket via the validated form, filters by status, changes a ticket's status, and deletes a ticket — all reflected in the list.
- READMEs explain how to run everything; testing evidence is included.

---

### How to run (after building)

```bash
# 1. backend
cd week4/tickets-backend
python -m venv venv
source venv/Scripts/activate          # PowerShell: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                    # set DATABASE_URL, then: createdb ticketsdb
uvicorn app.main:app --reload           # http://localhost:8000  (docs at /docs)

# 2. frontend
cd week4/tickets-frontend
npm install
ng serve                                # http://localhost:4200
```
