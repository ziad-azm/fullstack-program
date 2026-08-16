# How to run — Week 4 Tickets

Step-by-step runbook for the two apps. Backend first, frontend second, one terminal
each. **Every command assumes you are inside the app's own folder** — most startup
errors come from running them at the repo root.

## Prerequisites

- Python 3.12+, Node 20+ / npm, and a running PostgreSQL.
- Paths below start from the repo root (`fullstack-program/`).

## 1. Backend → http://localhost:8000

### First time only

```bash
cd Week4/tickets-backend
python -m venv venv
source venv/Scripts/activate       # PowerShell: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env               # then edit DATABASE_URL to match your Postgres
createdb ticketsdb                 # or create the database with pgAdmin / psql
```

`.env` needs both values:

```
DATABASE_URL=postgresql://user:password@localhost:5432/ticketsdb
ALLOWED_ORIGINS=http://localhost:4200
```

There is no migration step — the `tickets` table is created on startup.

### Every time

```bash
cd Week4/tickets-backend            # <- required: the app package lives here
source venv/Scripts/activate        # PowerShell: .\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

If PowerShell blocks `Activate.ps1`, skip activation and use the venv's Python directly:

```powershell
cd Week4\tickets-backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Expected output:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

Check it: open http://localhost:8000/docs, or `curl http://localhost:8000/tickets`.

## 2. Frontend → http://localhost:4200

In a second terminal, with the backend still running:

```bash
cd Week4/tickets-frontend
npm install                         # first time only
ng serve                            # or: npx ng serve
```

Open http://localhost:4200. You should see the ticket list with the create form
above it.

## 3. Tests

```bash
# backend (needs PostgreSQL running)
cd Week4/tickets-backend
source venv/Scripts/activate
pytest                              # 19 passed

# frontend
cd Week4/tickets-frontend
ng test                             # 12 passed
```

## Troubleshooting

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| `ModuleNotFoundError: No module named 'app'` | uvicorn was started outside `tickets-backend` | `cd Week4/tickets-backend` first |
| `RuntimeError: DATABASE_URL is not set` | no `.env` in the working directory | `cp .env.example .env` in `tickets-backend`, and start uvicorn from there |
| Traceback paths show `AppData\Local\Programs\Python\...` | the global Python is being used, not the venv | activate the venv, or call `.\venv\Scripts\python.exe -m uvicorn ...` |
| `psycopg.OperationalError: connection failed` | Postgres is not running, or `DATABASE_URL` is wrong | start PostgreSQL; check user / password / database name |
| `database "ticketsdb" does not exist` | database not created yet | `createdb ticketsdb` |
| Browser console shows a CORS error | origin not allowed | set `ALLOWED_ORIGINS=http://localhost:4200` in `.env`, restart uvicorn |
| Frontend shows "Failed to load tickets" | backend is down or on another port | start the backend; it must be on `http://localhost:8000` (the URL lives in `src/environments/environment*.ts`) |
| `Port 4200 is already in use` | an old `ng serve` is still running | stop it, or `ng serve --port 4300` |

## What runs where

| App | Folder | Command | URL |
| --- | ------ | ------- | --- |
| API | `Week4/tickets-backend` | `uvicorn app.main:app --reload` | http://localhost:8000 (docs at `/docs`) |
| UI | `Week4/tickets-frontend` | `ng serve` | http://localhost:4200 |
