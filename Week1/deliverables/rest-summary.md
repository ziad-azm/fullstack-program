# REST API Basics — Summary

REST (Representational State Transfer) is a style for building web APIs where the client and server communicate over HTTP using resources. A resource is any "thing" the API exposes (e.g. an item, a user), identified by a URL such as `/items` or `/items/5`.

## Core principles
- **Resources are nouns, not actions.** Use `/items`, not `/getItems`. The HTTP method decides the action.
- **Stateless.** Each request carries everything the server needs (e.g. auth token). The server doesn't remember previous requests.
- **Uniform interface.** The same HTTP methods behave consistently across all resources.

## HTTP methods (verbs)

| Method | Purpose | Example |
|--------|---------|---------|
| `GET` | Read data | `GET /items` → list items |
| `POST` | Create new data | `POST /items` → create an item |
| `PUT` | Replace an item fully | `PUT /items/5` |
| `PATCH` | Update part of an item | `PATCH /items/5` |
| `DELETE` | Remove an item | `DELETE /items/5` |

## Common status codes

| Code | Meaning | When |
|------|---------|------|
| `200 OK` | Success | GET/PUT/PATCH succeeded |
| `201 Created` | Resource created | POST succeeded |
| `204 No Content` | Success, no body | DELETE succeeded |
| `400 Bad Request` | Invalid input | Validation failed |
| `401 Unauthorized` | Not authenticated | Missing/invalid token |
| `403 Forbidden` | Authenticated but not allowed | No permission |
| `404 Not Found` | Resource doesn't exist | Wrong ID |
| `500 Internal Server Error` | Server crashed | Unhandled exception |

## JSON & auth
- **JSON** is the standard data format for both requests and responses, sent with the header `Content-Type: application/json`.
- **Auth basics:** most APIs authenticate with a token in the header: `Authorization: Bearer <token>`. The server validates the token on every request (because REST is stateless).
