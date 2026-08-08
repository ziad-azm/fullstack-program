"""
Week 1 — API Basics Exercise (FastAPI)
======================================
A minimal REST API that demonstrates the Week 1 backend basics:

  - Routing          -> @app.get / @app.post decorators
  - Models / schemas -> Pydantic BaseModel classes
  - Validation       -> Field(...) constraints on the schema
  - API development   -> a small /items resource (list, get one, create)
  - Error handling    -> HTTPException (404) + clean 400 on validation

Storage is a simple in-memory list — no database needed, so it runs anywhere.
"""

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field

app = FastAPI(title="API Basics Exercise")

# In-memory "database"
items: list[dict] = []
next_id = 1


# ---------- Models / schemas (validation lives here) ----------
class ItemIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)   # required, non-empty
    price: float = Field(..., gt=0)                        # must be > 0
    in_stock: bool = True


class ItemOut(ItemIn):
    id: int
    created_at: str


# ---------- Error handling: clean 400 for validation errors ----------
@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    errors = [
        {"field": ".".join(str(p) for p in e["loc"] if p != "body"), "message": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse(status_code=400, content={"detail": errors})


# ---------- Routing + API development ----------
@app.get("/items", response_model=list[ItemOut])
def list_items():
    """Return all items."""
    return items


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    """Return one item, or 404 if it doesn't exist."""
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(item: ItemIn):
    """Create a new item. Validation runs automatically before this code."""
    global next_id
    new = {
        "id": next_id,
        "name": item.name,
        "price": item.price,
        "in_stock": item.in_stock,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    items.append(new)
    next_id += 1
    return new
