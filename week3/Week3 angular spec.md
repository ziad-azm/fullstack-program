# Week 3 — Frontend Exercise (Build Spec)

## Context
- My primary stack is Node.js (Express/NestJS); I'm learning **Angular** as my frontend track for this program.
- This connects to the **FastAPI `/items` API** I built in Week 2 (full CRUD, PostgreSQL). Build the Angular frontend only.

## Goal
A simple Angular screen that talks to the `/items` API: a **list screen** and a **create form**, with loading state, error handling, and validation messages.

## Folder structure to produce
```
week3/
└─ items-frontend/         # Angular app
   └─ src/app/
      ├─ models/
      │  └─ item.model.ts        # Item interface
      ├─ services/
      │  └─ item.service.ts      # HttpClient calls to the API
      └─ components/
         ├─ item-list/           # list screen (GET /items)
         └─ item-form/           # create form (POST /items)
```
(Use the standard Angular CLI project layout; the folders above are what to add inside it.)

## API it connects to (from Week 2)
Base URL: `http://localhost:8000`

| Method | Path | Use |
|--------|------|-----|
| `GET` | `/items` | Load the list |
| `POST` | `/items` | Create a new item |

Item shape:
```ts
{ id: number; name: string; price: number; in_stock: boolean; created_at: string }
```
Create body: `{ name: string; price: number; in_stock?: boolean }`

## Requirements

1. **Model** (`item.model.ts`)
   - An `Item` interface matching the API response.
   - An `ItemCreate` type for the create payload (`name`, `price`, optional `in_stock`).

2. **Service** (`item.service.ts`)
   - Use Angular `HttpClient`.
   - `getItems()` → `GET /items`, returns `Observable<Item[]>`.
   - `createItem(payload)` → `POST /items`, returns `Observable<Item>`.
   - Put the base URL in one place (a constant or environment file).

3. **List screen** (`item-list` component)
   - Calls `getItems()` on init.
   - Shows a **loading state** (spinner or "Loading…") while the request is in flight.
   - Renders the items (name, price, in-stock) in a list or table.
   - Shows an **error message** if the request fails.
   - Shows an "empty" message when there are no items.
   - Refreshes the list after a new item is created.

4. **Create form** (`item-form` component)
   - Use Angular **Reactive Forms** (`FormGroup` / `FormControl`).
   - Fields: `name` (required), `price` (required, must be > 0), `in_stock` (checkbox, default true).
   - Show **validation messages** under each field (e.g. "Name is required", "Price must be greater than 0").
   - Disable the submit button while the form is invalid or while submitting.
   - On submit: call `createItem()`, show a **loading state**, handle success (clear the form, refresh the list) and **error** (show a message).

5. **Routing**
   - Set up basic routing so the list screen is the default route (`/`) — the form can be on the same page or its own route (`/new`), your choice.

6. **CORS note**
   - The FastAPI backend must allow requests from the Angular dev server (`http://localhost:4200`). If it doesn't already, enable CORS in FastAPI with `CORSMiddleware` allowing that origin.

7. **README** (`week3/items-frontend/README.md`)
   - How to install (`npm install`) and run (`ng serve`, opens on `http://localhost:4200`).
   - A note that the Week 2 FastAPI backend must be running on `http://localhost:8000` first.
   - How to enable CORS on the backend if needed.

## Definition of done
- `ng serve` runs the app on `http://localhost:4200`.
- The list screen loads items from the live API, with visible loading and error states.
- The create form validates input (required name, price > 0) with messages, and successfully creates an item that then appears in the list.
- The README explains how to run both the frontend and backend together.

---

### How to run (after building)
```bash
# 1. start the Week 2 backend first
cd week2/fastapi-items
uvicorn app.main:app --reload      # http://localhost:8000

# 2. start the Angular app
cd week3/items-frontend
npm install
ng serve                            # http://localhost:4200
```