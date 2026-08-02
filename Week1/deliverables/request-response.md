# Simple API Request / Response Example

Creating an item via `POST /items`.

## Request
```http
POST /items HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

{
  "name": "Notebook",
  "price": 25.5,
  "in_stock": true
}
```

## Success response (`201 Created`)
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 12,
  "name": "Notebook",
  "price": 25.5,
  "in_stock": true,
  "created_at": "2026-07-31T10:15:00Z"
}
```

## Validation error response (`400 Bad Request`)
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "detail": [
    {
      "field": "price",
      "message": "price must be greater than 0"
    }
  ]
}
```

## Read example — `GET /items`
```http
GET /items HTTP/1.1
Host: api.example.com
```
```json
[
  { "id": 12, "name": "Notebook", "price": 25.5, "in_stock": true },
  { "id": 13, "name": "Pen",      "price": 3.0,  "in_stock": false }
]
```
