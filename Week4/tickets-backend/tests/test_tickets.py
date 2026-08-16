"""End-to-end CRUD tests for the Tickets API.

These run against the real database in DATABASE_URL (see .env), so start
PostgreSQL first. Every test cleans up the rows it creates.

    pytest
"""

import pytest
from fastapi.testclient import TestClient

from app.database import get_connection, init_db
from app.main import app


@pytest.fixture(scope="module")
def client():
    init_db()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def make_ticket(client):
    """Creates tickets and deletes them again when the test finishes."""
    created_ids = []

    def _make(**overrides):
        payload = {"title": "Printer is jammed", "description": "2nd floor"}
        payload.update(overrides)
        response = client.post("/tickets", json=payload)
        assert response.status_code == 201
        created_ids.append(response.json()["id"])
        return response.json()

    yield _make

    with get_connection() as conn:
        with conn.cursor() as cur:
            for ticket_id in created_ids:
                cur.execute("DELETE FROM tickets WHERE id = %s", (ticket_id,))


# ---------- create ----------


def test_create_returns_201_with_defaults(make_ticket):
    ticket = make_ticket()

    assert ticket["id"] > 0
    assert ticket["title"] == "Printer is jammed"
    assert ticket["status"] == "open"
    assert ticket["priority"] == "medium"
    assert ticket["created_at"]


def test_create_accepts_explicit_status_and_priority(make_ticket):
    ticket = make_ticket(status="in_progress", priority="high")

    assert ticket["status"] == "in_progress"
    assert ticket["priority"] == "high"


def test_create_without_title_returns_400(client):
    response = client.post("/tickets", json={"description": "no title"})

    assert response.status_code == 400
    assert response.json()["detail"] == [{"field": "title", "message": "title is required"}]


def test_create_with_blank_title_returns_400(client):
    response = client.post("/tickets", json={"title": "   "})

    assert response.status_code == 400
    assert response.json()["detail"] == [{"field": "title", "message": "title must not be empty"}]


def test_create_with_too_long_title_returns_400(client):
    response = client.post("/tickets", json={"title": "x" * 151})

    assert response.status_code == 400
    assert response.json()["detail"] == [
        {"field": "title", "message": "title must be at most 150 characters"}
    ]


def test_create_with_invalid_status_returns_400(client):
    response = client.post("/tickets", json={"title": "Bad status", "status": "urgent"})

    assert response.status_code == 400
    assert response.json()["detail"][0]["field"] == "status"


def test_create_with_malformed_json_returns_400(client):
    response = client.post(
        "/tickets",
        content="{not json}",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == [
        {"field": "body", "message": "request body must be valid JSON"}
    ]


# ---------- list ----------


def test_list_returns_created_ticket(client, make_ticket):
    ticket = make_ticket()

    response = client.get("/tickets")

    assert response.status_code == 200
    assert ticket["id"] in [t["id"] for t in response.json()]


def test_list_filters_by_status(client, make_ticket):
    open_ticket = make_ticket(title="Still open")
    closed_ticket = make_ticket(title="Already closed", status="closed")

    response = client.get("/tickets", params={"status": "closed"})

    assert response.status_code == 200
    returned_ids = [t["id"] for t in response.json()]
    assert closed_ticket["id"] in returned_ids
    assert open_ticket["id"] not in returned_ids
    assert all(t["status"] == "closed" for t in response.json())


def test_list_with_invalid_status_filter_returns_400(client):
    response = client.get("/tickets", params={"status": "nope"})

    assert response.status_code == 400
    assert response.json()["detail"][0]["field"] == "status"


# ---------- get one ----------


def test_get_one_returns_the_ticket(client, make_ticket):
    ticket = make_ticket()

    response = client.get(f"/tickets/{ticket['id']}")

    assert response.status_code == 200
    assert response.json() == ticket


def test_get_missing_ticket_returns_404(client):
    response = client.get("/tickets/99999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket 99999999 not found"}


# ---------- patch ----------


def test_patch_updates_status(client, make_ticket):
    ticket = make_ticket()

    response = client.patch(f"/tickets/{ticket['id']}", json={"status": "closed"})

    assert response.status_code == 200
    assert response.json()["status"] == "closed"
    assert response.json()["title"] == ticket["title"]


def test_patch_missing_ticket_returns_404(client):
    response = client.patch("/tickets/99999999", json={"status": "closed"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket 99999999 not found"}


def test_patch_with_explicit_null_title_returns_400(client, make_ticket):
    ticket = make_ticket()

    response = client.patch(f"/tickets/{ticket['id']}", json={"title": None})

    assert response.status_code == 400
    assert response.json()["detail"] == [{"field": "title", "message": "title must not be null"}]


def test_patch_with_empty_body_returns_the_ticket_unchanged(client, make_ticket):
    ticket = make_ticket()

    response = client.patch(f"/tickets/{ticket['id']}", json={})

    assert response.status_code == 200
    assert response.json() == ticket


def test_patch_with_invalid_status_returns_400(client, make_ticket):
    ticket = make_ticket()

    response = client.patch(f"/tickets/{ticket['id']}", json={"status": "done"})

    assert response.status_code == 400
    assert response.json()["detail"][0]["field"] == "status"


# ---------- delete ----------


def test_delete_returns_204_then_404(client, make_ticket):
    ticket = make_ticket()

    assert client.delete(f"/tickets/{ticket['id']}").status_code == 204
    assert client.get(f"/tickets/{ticket['id']}").status_code == 404


def test_delete_missing_ticket_returns_404(client):
    response = client.delete("/tickets/99999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket 99999999 not found"}
