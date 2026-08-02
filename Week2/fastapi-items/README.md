# Items API (FastAPI)

A small `/items` REST API built with FastAPI, Pydantic validation, and PostgreSQL.

## 1. Set up the database

Create the Postgres database (adjust host/user as needed):

```bash
createdb week2db
```

Copy the example env file and set your connection string:

```bash
cp .env.example .env
# then edit .env, e.g.:
# DATABASE_URL=postgresql://user:password@localhost:5432/week2db
```

The `items` table is created automatically on startup (`CREATE TABLE IF NOT EXISTS`) — no manual migration needed.

## 2. Install dependencies and run

```bash
python -m venv venv
source venv/Scripts/activate      # Windows Git Bash; PowerShell: venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

The API runs on **http://localhost:8000**. Interactive docs (Swagger UI) are at **http://localhost:8000/docs**.

## Endpoints

| Method   | Path          | Behaviour                                | Success code |
| -------- | ------------- | ----------------------------------------- | :-----------: |
| `POST`   | `/items`      | Create an item                            | `201` / `400` |
| `GET`    | `/items`      | List all items                            | `200`         |
| `GET`    | `/items/{id}` | Get one item                              | `200` / `404` |
| `PATCH`  | `/items/{id}` | Partially update an item                  | `200` / `404` / `400` |
| `DELETE` | `/items/{id}` | Delete an item                            | `204` / `404` |

## curl examples

**Create**

```bash
curl -i -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Notebook", "price": 25.5, "in_stock": true}'
# 201 Created
```

**List all**

```bash
curl -i http://localhost:8000/items
# 200 OK -> []  (or an array of items)
```

**Get one**

```bash
curl -i http://localhost:8000/items/1
# 200 OK
```

**Update (partial)**

```bash
curl -i -X PATCH http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 19.99}'
# 200 OK
```

**Delete**

```bash
curl -i -X DELETE http://localhost:8000/items/1
# 204 No Content
```

**Validation error** (price must be greater than 0)

```bash
curl -i -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Notebook", "price": -5}'
# 400 Bad Request
# {"detail": [{"field": "price", "message": "price must be greater than 0"}]}
```

**Not found**

```bash
curl -i http://localhost:8000/items/9999
# 404 Not Found
# {"detail": "Item 9999 not found"}
```
