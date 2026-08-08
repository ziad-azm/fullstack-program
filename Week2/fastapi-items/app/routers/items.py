from typing import List

from fastapi import APIRouter, HTTPException, Response, status

from ..database import get_connection
from ..schemas import ItemIn, ItemOut, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


def _row_to_item(row) -> ItemOut:
    item_id, name, price, in_stock, created_at = row
    return ItemOut(
        id=item_id,
        name=name,
        price=float(price),
        in_stock=in_stock,
        created_at=created_at,
    )


def _fetch_item_row(item_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, price, in_stock, created_at FROM items WHERE id = %s",
                (item_id,),
            )
            return cur.fetchone()


@router.post("", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemIn):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO items (name, price, in_stock)
                VALUES (%s, %s, %s)
                RETURNING id, name, price, in_stock, created_at
                """,
                (item.name, item.price, item.in_stock),
            )
            row = cur.fetchone()
    return _row_to_item(row)


@router.get("", response_model=List[ItemOut])
def list_items():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, price, in_stock, created_at FROM items ORDER BY id")
            rows = cur.fetchall()
    return [_row_to_item(row) for row in rows]


@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    row = _fetch_item_row(item_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return _row_to_item(row)


@router.patch("/{item_id}", response_model=ItemOut)
def update_item(item_id: int, item: ItemUpdate):
    updates = item.model_dump(exclude_unset=True)

    if not updates:
        row = _fetch_item_row(item_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
        return _row_to_item(row)

    set_clause = ", ".join(f"{field} = %s" for field in updates)
    values = list(updates.values())
    values.append(item_id)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                UPDATE items SET {set_clause}
                WHERE id = %s
                RETURNING id, name, price, in_stock, created_at
                """,
                values,
            )
            row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return _row_to_item(row)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM items WHERE id = %s RETURNING id", (item_id,))
            row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
