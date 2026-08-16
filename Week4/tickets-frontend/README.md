# Tickets Frontend (Angular)

The Angular app for the Week 4 Tickets mini module: create tickets, list them,
filter by status, change a ticket's status, and delete — all against the
FastAPI backend in `Week4/tickets-backend`.

## Prerequisites

The **backend must already be running on `http://localhost:8000`** — every screen
in this app calls it directly.

```bash
cd Week4/tickets-backend
python -m venv venv
source venv/Scripts/activate      # Windows Git Bash; PowerShell: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload      # http://localhost:8000
```

See `Week4/tickets-backend/README.md` for database setup (`.env`, PostgreSQL).

## Install and run

```bash
npm install
ng serve
```

Open `http://localhost:4200`. The whole feature lives on one route (`/`): the
create form sits above the list, and the list refreshes after every create,
status change, and delete. Any other URL redirects back to `/`.

## What the screen does

- **Loads** tickets on init via `GET /tickets`, with a loading state and an error
  message if the API is unreachable.
- **Filter** dropdown (all / open / in progress / closed) re-queries with
  `GET /tickets?status=…`.
- **Create form** — reactive form with `title` (required, max 150, rejects
  whitespace-only), `description` (optional, max 2000), and a `priority` select.
  Submit is disabled while the form is invalid or a request is in flight, and
  validation errors returned by the API are shown above the button.
- **Row actions** — a status dropdown (`PATCH /tickets/{id}`) and a delete button
  (`DELETE /tickets/{id}`), both disabled while that row's request is in flight.

## CORS

The Angular dev server runs on `http://localhost:4200`, a different origin than
the API on `http://localhost:8000`, so the backend must explicitly allow it.
`tickets-backend/app/main.py` registers `CORSMiddleware` with the origins from
`ALLOWED_ORIGINS` in `.env`:

```
ALLOWED_ORIGINS=http://localhost:4200
```

If requests fail with a CORS error in the browser console, check that value and
restart `uvicorn`.

## Project structure

```
src/app/
├─ models/ticket.model.ts       # Ticket / TicketCreate types, status + priority unions
├─ services/ticket.service.ts   # HttpClient calls (getTickets, getTicket, createTicket,
│                               #   updateStatus, deleteTicket)
└─ components/
   ├─ ticket-list/              # list, status filter, row actions — hosts the form
   └─ ticket-form/              # reactive create form, emits `created` on success
```

The API base URL lives in one place: `src/environments/environment.ts` /
`environment.development.ts` (`apiUrl`).

## Tests

```bash
ng test
```

12 tests covering the list (load, empty state, error state, status filter, status
patch, delete, and that each row's dropdown preselects the ticket's real status)
and the form (submit disabled until valid, whitespace-only title rejected,
successful create clears the form and emits, API validation errors surfaced).

```
 Test Files  3 passed (3)
      Tests  12 passed (12)
```

### Note on `<select>` bindings

Options rendered with `@for` are created *after* the `<select>`'s own property
bindings run, so `[value]="ticket.status"` silently loses its value and every row
falls back to the first option. The selected option is therefore marked on the
option itself (`[selected]="option === ticket.status"`); the spec
`preselects each ticket's current status in its dropdown` guards against a
regression.
