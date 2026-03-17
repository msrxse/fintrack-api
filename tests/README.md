# Tests — Key Concepts

## SQLAlchemy Session: Three Operations

### `session.add(obj)`
Tells SQLAlchemy to track an object. No SQL is sent yet. The object exists only in Python memory.

### `session.flush()`
Sends the SQL to the database (e.g. `INSERT INTO users ...`) but keeps the transaction open. The row exists inside this transaction but **other connections cannot see it yet**. Useful when you need the DB-generated ID before committing:

```python
session.add(user)
session.flush()          # DB assigns user.id = 42
session.add(Account(user_id=user.id))  # now you can use it
session.commit()
```

### `session.commit()`
Closes and finalizes the transaction. The change is permanent. Other connections can now see it.

### `session.rollback()`
Throws away everything in the current transaction since the last commit. The DB is left as if the SQL never ran.

---

## One-Time Setup

Before running tests for the first time, create the test database inside the running Postgres container:

```bash
docker exec fintrack_db psql -U fintrack -d postgres -c "CREATE DATABASE fintrack_test;"
```

This only needs to be done once. The tables inside are created and dropped automatically by pytest.

## Running Tests

```bash
poetry run pytest tests/test_auth.py -v        # run one file
poetry run pytest -v                            # run all tests
poetry run pytest --cov=app -v                 # run with coverage report
```

---

## Trailing Slashes in Test Requests

Always use a trailing slash on POST/PUT/DELETE requests in tests:

```python
client.post("/budgets/", ...)   # correct
client.post("/budgets", ...)    # wrong — causes silent failure
```

Without the trailing slash, FastAPI issues a 307 redirect to the URL with the slash. `TestClient` does not follow redirects by default, so the request body is dropped and the route never executes. The call returns a 307 with no error, making the failure hard to spot.

GET requests are unaffected since they have no body.

---

## How Tests Use This

Each test runs inside a transaction that is **never committed**:

```
BEGIN TRANSACTION        ← before the test
  POST /transactions     ← test runs, app flushes and "commits" internally
  assert response == 201
ROLLBACK                 ← after the test — everything is discarded
```

The app code runs normally. But the outer transaction is rolled back, so nothing persists between tests. The database is clean for the next test without dropping or recreating tables.
