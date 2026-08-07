# Items Frontend

Angular app for the Week 3 exercise: a list screen and create form for the
Week 2 FastAPI `/items` API.

## Prerequisites

The **Week 2 FastAPI backend must already be running on `http://localhost:8000`**
before you use this app (the list screen and create form both call it directly).

```bash
cd Week2/fastapi-items
python -m venv venv
source venv/Scripts/activate      # Windows Git Bash; PowerShell: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload      # http://localhost:8000
```

See `Week2/fastapi-items/README.md` for database setup (`.env`, PostgreSQL).

## Install and run

```bash
npm install
ng serve
```

Open `http://localhost:4200`.

- `/` — list screen, loads items from `GET /items`.
- `/new` — create form, posts to `POST /items` and returns to the list.

## CORS

The Angular dev server runs on `http://localhost:4200`, a different origin than
the API on `http://localhost:8000`, so the backend must explicitly allow it.
`Week2/fastapi-items/app/main.py` should have:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

If requests from the Angular app fail with a CORS error in the browser console,
add this to `main.py` (before `app.include_router(...)`) and restart `uvicorn`.

## Project structure

```
src/app/
├─ models/item.model.ts       # Item, ItemCreate interfaces
├─ services/item.service.ts   # HttpClient calls to the API
└─ components/
   ├─ item-list/              # list screen (GET /items)
   └─ item-form/               # create form (POST /items)
```

The API base URL lives in `src/environments/environment.ts` /
`environment.development.ts` (`apiUrl`).

## Tests

```bash
ng test
```
