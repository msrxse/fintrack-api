# Error Handling

## The problem

Without global handlers, errors from different sources return different shapes:

- `HTTPException` → `{"detail": "..."}`
- `RequestValidationError` → `{"detail": [{"loc": [...], "msg": "..."}]}`
- Unhandled exceptions → FastAPI's default 500 format

A frontend consuming the API has to handle 3 different formats.

## The solution

Two global exception handlers in `app/main.py` normalize every error into one consistent shape.

## Response shape

**HTTPException (4xx, 5xx)**
```json
{
  "error": "This user already has an account. Login instead.",
  "status_code": 409
}
```

**RequestValidationError (422)**
```json
{
  "error": "Validation error",
  "detail": [
    {
      "loc": ["body", "account_id"],
      "msg": "Input should be a valid integer",
      "type": "int_parsing"
    }
  ]
}
```

## How each handler works

`@app.exception_handler(SomeException)` intercepts a specific exception type before it reaches the client. The handler receives `request` (the incoming request) and `exc` (the caught exception), and must return a `JSONResponse`.

`JSONResponse` takes `status_code` and `content` (a dict). The dict becomes the response body — the `content=` wrapper is internal to FastAPI.

## What each handler covers

| Handler | Exception type | Triggered by |
|---|---|---|
| `fastapi_exception_handler` | `HTTPException` | Any `raise HTTPException(...)` in your code, auth failures, missing bearer token (403) |
| `pydantic_exception_handler` | `RequestValidationError` | Wrong field types, missing required fields in request body |

## How to trigger each one

**HTTPException** — raise it manually anywhere:
```python
raise HTTPException(status_code=404, detail="Transaction not found")
```

**RequestValidationError** — send a bad request body. Example: send `"account_id": "hello"` where an integer is expected. Pydantic rejects it before your route runs.

**Auth errors** — hit a protected route without a token, or with an invalid/expired token. `HTTPBearer` raises 403 for missing token; `get_current_user` raises 401 for invalid token. Both go through `fastapi_exception_handler`.

## Adding a new handler

Register it in `app/main.py` the same way:
```python
@app.exception_handler(SomeOtherException)
def some_other_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "status_code": 500},
    )
```

## 401 vs 403

- **401 Unauthorized** — identity unknown (bad token, expired token, user not found)
- **403 Forbidden** — identity known, but access denied (missing token triggers this via `HTTPBearer`)
