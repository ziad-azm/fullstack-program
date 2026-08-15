from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, Response, status

from ..database import get_connection
from ..schemas import TicketIn, TicketOut, TicketStatus, TicketUpdate

router = APIRouter(prefix="/tickets", tags=["tickets"])

COLUMNS = "id, title, description, status, priority, created_at"


def _row_to_ticket(row) -> TicketOut:
    ticket_id, title, description, ticket_status, priority, created_at = row
    return TicketOut(
        id=ticket_id,
        title=title,
        description=description,
        status=ticket_status,
        priority=priority,
        created_at=created_at,
    )


def _fetch_ticket_row(ticket_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT {COLUMNS} FROM tickets WHERE id = %s", (ticket_id,))
            return cur.fetchone()


def _not_found(ticket_id: int) -> HTTPException:
    return HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")


@router.post("", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketIn):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO tickets (title, description, status, priority)
                VALUES (%s, %s, %s, %s)
                RETURNING {COLUMNS}
                """,
                (ticket.title, ticket.description, ticket.status.value, ticket.priority.value),
            )
            row = cur.fetchone()
    return _row_to_ticket(row)


@router.get("", response_model=List[TicketOut])
def list_tickets(ticket_status: Optional[TicketStatus] = Query(None, alias="status")):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if ticket_status is None:
                cur.execute(f"SELECT {COLUMNS} FROM tickets ORDER BY id")
            else:
                cur.execute(
                    f"SELECT {COLUMNS} FROM tickets WHERE status = %s ORDER BY id",
                    (ticket_status.value,),
                )
            rows = cur.fetchall()
    return [_row_to_ticket(row) for row in rows]


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int):
    row = _fetch_ticket_row(ticket_id)
    if row is None:
        raise _not_found(ticket_id)
    return _row_to_ticket(row)


@router.patch("/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, ticket: TicketUpdate):
    # mode="json" turns the status/priority enums into the plain strings the DB stores.
    updates = ticket.model_dump(exclude_unset=True, mode="json")

    if not updates:
        row = _fetch_ticket_row(ticket_id)
        if row is None:
            raise _not_found(ticket_id)
        return _row_to_ticket(row)

    set_clause = ", ".join(f"{field} = %s" for field in updates)
    values = list(updates.values())
    values.append(ticket_id)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                UPDATE tickets SET {set_clause}
                WHERE id = %s
                RETURNING {COLUMNS}
                """,
                values,
            )
            row = cur.fetchone()

    if row is None:
        raise _not_found(ticket_id)
    return _row_to_ticket(row)


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tickets WHERE id = %s RETURNING id", (ticket_id,))
            row = cur.fetchone()

    if row is None:
        raise _not_found(ticket_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
