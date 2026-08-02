# Week 1 — Engineering Foundations (Study Guide)
**Stack focus:** Python + PostgreSQL

A single guide covering every Week 1 self-study topic. The goal is a common baseline before moving into backend and frontend stacks. Read it top to bottom, and run the small snippets as you go.

---

## 1. REST API concepts

REST is a style for building web APIs where clients and servers talk over HTTP using **resources**. A resource is any "thing" the API exposes (an item, a user), identified by a URL like `/items` or `/items/5`.

Key ideas:
- **Resources are nouns, not actions.** Use `/items`, not `/getItems`. The HTTP method decides the action.
- **Stateless.** Each request carries everything the server needs (like an auth token). The server keeps no memory of previous requests.
- **Uniform interface.** The same methods behave consistently across all resources.

A resource has a collection URL (`/items`) and a member URL (`/items/{id}`). You act on them with HTTP methods (next section).

---

## 2. HTTP methods and status codes

**Methods (verbs):**

| Method | Purpose | Example |
|--------|---------|---------|
| `GET` | Read | `GET /items` → list, `GET /items/5` → one |
| `POST` | Create | `POST /items` |
| `PUT` | Replace fully | `PUT /items/5` |
| `PATCH` | Update partially | `PATCH /items/5` |
| `DELETE` | Remove | `DELETE /items/5` |

**Status codes** — the first digit tells you the category:
- `2xx` success · `3xx` redirect · `4xx` client error · `5xx` server error

| Code | Meaning | When |
|------|---------|------|
| `200 OK` | Success with body | GET/PATCH succeeded |
| `201 Created` | Resource created | POST succeeded |
| `204 No Content` | Success, no body | DELETE succeeded |
| `400 Bad Request` | Invalid input | Validation failed |
| `401 Unauthorized` | Not authenticated | Missing/invalid token |
| `403 Forbidden` | Authenticated but not allowed | No permission |
| `404 Not Found` | Doesn't exist | Wrong ID |
| `409 Conflict` | State conflict | Duplicate unique value |
| `500 Internal Server Error` | Server crashed | Unhandled exception |

Rule of thumb: return the most specific correct code. A missing item is `404`, not `400`.

---

## 3. JSON request and response structure

JSON is the default data format for REST, sent with the header `Content-Type: application/json`.

**Request body (POST /items):**
```json
{
  "name": "Notebook",
  "price": 25.5,
  "in_stock": true
}
```

**Success response (201):**
```json
{
  "id": 12,
  "name": "Notebook",
  "price": 25.5,
  "in_stock": true,
  "created_at": "2026-07-31T10:15:00Z"
}
```

**Error response (400):**
```json
{
  "detail": [
    { "field": "price", "message": "price must be greater than 0" }
  ]
}
```

JSON types map cleanly to Python: object→`dict`, array→`list`, string→`str`, number→`int`/`float`, `true/false`→`bool`, `null`→`None`.

---

## 4. Authentication and authorization basics

Two different things people often confuse:
- **Authentication** = *who are you?* (verifying identity)
- **Authorization** = *what are you allowed to do?* (checking permissions)

The most common API pattern is a **bearer token**: the client sends a credential in a header on every request (REST is stateless, so nothing is remembered between requests):
```
Authorization: Bearer <token>
```

The server validates the token; if it's missing/invalid → `401`. If the token is valid but the user lacks permission for that action → `403`.

Minimal example (FastAPI dependency that guards write endpoints):
```python
from fastapi import Header, HTTPException

API_TOKEN = "secret-token"

def require_token(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or malformed Authorization header")
    if authorization.split(" ", 1)[1] != API_TOKEN:
        raise HTTPException(401, "Invalid token")
```
> Real systems hash passwords and use JWT/OAuth. This simple token is enough to understand the concept.

---

## 5. SQL basics (PostgreSQL)

SQL is how you talk to a relational database. The four core operations (CRUD):

```sql
-- CREATE
INSERT INTO items (name, price) VALUES ('Notebook', 25.5);

-- READ
SELECT * FROM items;
SELECT * FROM items WHERE price > 10 ORDER BY price DESC LIMIT 5;

-- UPDATE
UPDATE items SET price = 30 WHERE id = 1;

-- DELETE
DELETE FROM items WHERE id = 1;
```

Useful pieces you'll use constantly:
- `WHERE` filters rows, `ORDER BY` sorts, `LIMIT`/`OFFSET` paginate.
- Aggregations: `COUNT(*)`, `SUM(price)`, `AVG(price)`, with `GROUP BY`.
- `JOIN` combines rows from related tables (see next section).

**Running SQL from Python** with `psycopg` (always use parameters — never string-format values in, that's how SQL injection happens):
```python
import psycopg

with psycopg.connect("postgresql://postgres@localhost:5432/mydb") as conn:
    with conn.cursor() as cur:
        cur.execute("INSERT INTO items (name, price) VALUES (%s, %s)", ("Pen", 3.0))
        cur.execute("SELECT id, name FROM items WHERE price > %s", (2.0,))
        print(cur.fetchall())
```

---

## 6. Tables, relations, indexes, and migrations (PostgreSQL)

**Tables** hold rows; each column has a type.
```sql
CREATE TABLE categories (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE notes (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(100) NOT NULL,
    body        TEXT NOT NULL DEFAULT '',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    category_id INTEGER NOT NULL REFERENCES categories(id)  -- the relation
);
```

**Relations** link tables with a **foreign key**. Above, each note belongs to one category (`category_id REFERENCES categories(id)`), and one category can have many notes — a **one-to-many** relation. You read across the relation with a `JOIN`:
```sql
SELECT notes.title, categories.name
FROM notes
JOIN categories ON categories.id = notes.category_id;
```

**Indexes** speed up lookups on columns you filter/sort by often. Without one, Postgres scans every row.
```sql
CREATE INDEX ix_notes_title ON notes (title);
```
Primary keys and `UNIQUE` columns are indexed automatically. Don't over-index — each index costs write speed and storage.

**Migrations** are versioned, ordered changes to your schema, kept in code so every environment (yours, a teammate's, production) can be brought to the same structure. Instead of editing the DB by hand, you write a migration. With **Alembic** (the standard for Python/SQLAlchemy):
```bash
alembic revision --autogenerate -m "create categories and notes"  # generate
alembic upgrade head     # apply
alembic downgrade -1     # roll back one step
```

---

## 7. Git branching, commits, and pull requests

Git tracks the history of your code. The everyday feature-branch flow:
```bash
git checkout main
git pull origin main                    # get the latest

git checkout -b feature/notes-endpoint  # branch off for your work

git add .
git commit -m "Add GET and POST /notes endpoints"

git push origin feature/notes-endpoint  # publish the branch
# open a Pull Request on GitHub: feature/notes-endpoint -> main
# review -> approve -> merge
```

Good habits:
- **Branch per feature/fix** — keep `main` always working.
- **Small, focused commits**, imperative message ("Add validation", not "added validation").
- **Pull Requests** are where code gets reviewed before it lands in `main`.

---

## 8. Debugging using logs, stack traces, dev tools, and API tools

- **Logs:** print structured messages at the right level. Prefer the `logging` module over `print`:
  ```python
  import logging
  log = logging.getLogger("app")
  log.info("Created note id=%s", note_id)
  log.warning("Duplicate category name: %s", name)
  ```
- **Stack traces:** read them **bottom-up** — the last line is the actual error type/message; the lines above show the call path that led there. Look for the first line pointing at *your* file.
- **Browser dev tools:** the Network tab shows each request's URL, method, status code, and response body — essential for frontend/API issues. The Console shows JS errors.
- **API tools:** use Postman, `curl`, or FastAPI's auto-generated `/docs` to send requests and inspect responses without a frontend:
  ```bash
  curl -X POST localhost:8000/items \
    -H "Content-Type: application/json" \
    -d '{"name":"Pen","price":3.0}'
  ```

Debugging mindset: reproduce it, read the actual error, isolate the smallest failing case, form one hypothesis at a time.

---

## 9. Basic testing concepts

A test checks that code behaves as expected — automatically. The common shape is **Arrange → Act → Assert**.

- **Unit test:** one small piece in isolation.
- **Integration test:** several pieces together (e.g. an endpoint hitting the DB).

Example with `pytest` + FastAPI's test client:
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    # Arrange + Act
    r = client.post("/items", json={"name": "Pen", "price": 3.0})
    # Assert
    assert r.status_code == 201
    assert r.json()["name"] == "Pen"

def test_validation_error():
    r = client.post("/items", json={"name": "", "price": -5})
    assert r.status_code == 400
```
Run with `pytest -q`. Aim to test the happy path **and** the error paths (validation, 404, auth).

---

## 10. Safe and effective AI usage for developers

**Effective** — good things to ask AI for:
- A mental model of a new stack or library.
- Explaining unfamiliar code line by line.
- Generating a learning plan, boilerplate, or test cases.
- Suggesting where error handling is missing.

**Safe** — the rules:
- **Never share** secrets, credentials, tokens, or production data.
- **Never** use AI code in security, authentication, or payment logic without careful review.
- **Always read and understand** generated code before using it — don't copy blindly.
- **Always test** the generated code.
- **Document** how you used AI (a short usage log).

Good prompt pattern: give context (your level, the stack), state the goal, and ask for a small concrete example.
> "I'm an experienced developer new to FastAPI. Give me a 10-minute mental model of project structure with one GET and one POST example."

---

## Suggested order to study
1. REST + HTTP methods/status codes (1–2)
2. JSON structure (3)
3. SQL + tables/relations/indexes/migrations (5–6) — the biggest chunk
4. Auth basics (4)
5. Git (7)
6. Debugging + testing (8–9)
7. Safe AI usage (10) — apply it throughout

**Practice goal for the week:** be able to build and run a small validated CRUD API in Python backed by PostgreSQL, with a migration, a couple of tests, and a README.
