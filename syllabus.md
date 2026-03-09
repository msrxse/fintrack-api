# FinTrack API — Full Syllabus

**Stack:** Python 3.12, FastAPI, PostgreSQL (Docker), SQLAlchemy, Alembic, JWT Auth, Pydantic v2

## Teaching Style

Python syntax is taught **in context**, not upfront. Every time a new concept appears in the code (list comprehension, type hints, decorators, async/await, enums, etc.), it is explained right next to the example that uses it — like this:

```python
# --- CONCEPT: List Comprehension ---
# A concise way to build a list from another list.
# Syntax: [expression for item in iterable if condition]
# Instead of:
#   results = []
#   for t in transactions:
#       if t.amount < 0:
#           results.append(t)
# You write:
results = [t for t in transactions if t.amount < 0]
```

No separate syntax module — you learn exactly what you need, exactly when you need it.

---

## Module 1 — Dev Environment Setup

**Goal:** Get everything running locally, understand the tooling.

- [x] Done

Topics:

- Python virtual environments (`venv`)
- `requirements.txt` — pinning versions, why it matters
- Docker & `docker-compose.yml` for PostgreSQL
- `.env` files & never committing secrets
- Project folder structure and why we organize it this way
- Running FastAPI for the first time (`uvicorn`)

Outcome: FastAPI server running, PostgreSQL in Docker, you can hit `/health` in the browser.

---

## Module 2 — Database Design & SQLAlchemy Models

**Goal:** Design a real schema like a backend engineer would.

- [x] Done

Tables:

- `users` — id, email, hashed_password, created_at
- `accounts` — id, user_id, name, type (checking/savings/credit), currency, balance
- `categories` — id, name, type (income/expense), is_system
- `transactions` — id, account_id, category_id, amount, description, merchant, date, type
- `budgets` — id, user_id, category_id, limit_amount, period (monthly/weekly)

Topics:

- SQLAlchemy declarative models
- Column types, constraints, indexes
- Relationships (`ForeignKey`, `relationship()`, lazy loading vs eager)
- Enums in the database
- `created_at` / `updated_at` with server defaults

Outcome: All tables defined in Python, relationships understood.

---

## Module 3 — Alembic Migrations

**Goal:** Manage schema changes safely like production teams do.

- [x] Done

Topics:

- What migrations are and why `CREATE TABLE` scripts don't scale
- `alembic init`, `alembic.ini`, `env.py` setup
- Auto-generating migrations from models
- `upgrade` / `downgrade` — always write both
- Handling data migrations vs schema migrations
- Common pitfalls (renaming columns, adding NOT NULL)

Outcome: Tables created in PostgreSQL via migration. You can roll back and forward.

---

## Module 4 — Seed Data (Real Financial Data)

**Goal:** Populate the DB with realistic data to query against.

- [x] Done

Data included:

- 3 users with multiple accounts each
- 500+ transactions over 12 months
- Real merchant names (Amazon, Netflix, Uber, Whole Foods, etc.)
- Realistic amounts, frequencies, and categories
- Some edge cases: refunds (negative amounts), transfers between accounts, currency variations

Topics:

- Writing seed scripts with SQLAlchemy sessions
- Using `faker` library for realistic names/emails
- Idempotent seeds (safe to re-run)
- Bulk inserts for performance

Outcome: DB filled with real-looking data you can actually query and explore.

---

## Module 5 — Pydantic v2 Schemas

**Goal:** Understand the difference between your DB model and your API contract.

- [ ] Done

Topics:

- Why schemas and models are separate (never expose ORM objects directly)
- `BaseModel`, `model_validator`, `field_validator`
- Input schemas (what the API accepts) vs output schemas (what it returns)
- Nested schemas (transaction with account info)
- `model_config` with `from_attributes=True` (ORM mode)
- Handling decimals and dates properly in JSON

Outcome: Clean, validated request/response shapes for all resources.

---

## Module 6 — CRUD Routes

**Goal:** Build all the API endpoints with proper REST conventions.

- [ ] Done

Endpoints built:

- `GET /transactions` — list with filters (date range, category, account, type)
- `GET /transactions/{id}` — single transaction
- `POST /transactions` — create
- `PUT /transactions/{id}` — update
- `DELETE /transactions/{id}` — soft delete
- Same pattern for accounts, categories, budgets

Topics:

- FastAPI routers (`APIRouter`) for clean organization
- Path params vs query params vs request body
- Filtering, sorting, pagination (limit/offset)
- HTTP status codes — when to use 200 vs 201 vs 204 vs 404
- Dependency injection for DB sessions

Outcome: Full working REST API, testable in `/docs`.

---

## Module 7 — Analytics & Aggregations

**Goal:** The most interview-relevant module — complex SQL through SQLAlchemy.

- [ ] Done

Endpoints built:

- `GET /analytics/spending-by-category` — total spend per category for a period
- `GET /analytics/monthly-summary` — income vs expenses per month
- `GET /analytics/top-merchants` — top 10 merchants by spend
- `GET /analytics/budget-status` — actual vs budget per category
- `GET /analytics/cash-flow` — running balance over time
- `GET /analytics/trends` — month-over-month % change per category

Topics:

- SQLAlchemy `func.sum`, `func.count`, `group_by`, `having`
- Raw SQL with `text()` for complex queries
- Date truncation in PostgreSQL (`date_trunc`)
- Window functions (running totals)
- Query optimization — when to add indexes
- Returning shaped analytics responses

Outcome: You can explain and write complex DB queries — a core backend interview skill.

---

## Module 8 — Authentication & Authorization

**Goal:** Secure the API properly, understand JWT deeply.

- [ ] Done

Topics:

- Password hashing with `bcrypt` — why you never store plaintext
- JWT structure — header, payload, signature
- `POST /auth/register` and `POST /auth/login` returning access tokens
- Protected routes using FastAPI `Depends()`
- `get_current_user` dependency — decoding and validating tokens
- Role-based access (admin vs regular user)
- Refresh tokens (concept + implementation)
- Returning 401 vs 403 — the difference matters

Outcome: All routes protected. Users only see their own data.

---

## Module 9 — Dependencies, Middleware & Error Handling

**Goal:** Make the API production-quality, not just functional.

- [ ] Done
      Topics:

- FastAPI dependency injection pattern deeply — reusable, testable
- Global exception handlers (`@app.exception_handler`)
- Custom error responses with consistent shape
- CORS middleware (why it exists, how to configure)
- Request logging middleware (log every request with timing)
- Rate limiting concept
- Background tasks (`BackgroundTasks`) — e.g. send email on registration

Outcome: API behaves predictably under errors, ready for a frontend to consume.

---

## Module 10 — Testing with pytest

**Goal:** Write tests like a professional, not an afterthought.

- [ ] Done
      Topics:

- `pytest` setup and project structure for tests
- Test database — separate DB, wipe between tests
- `TestClient` from FastAPI
- Fixtures — reusable setup (test user, auth token, seeded data)
- Testing CRUD endpoints
- Testing auth (unauthorized, wrong token, expired token)
- Testing analytics endpoints with known data
- Coverage reporting

Outcome: Test suite that gives you confidence to refactor. Looks great in a portfolio.

---

## Module 11 — Deployment-Ready Configuration

**Goal:** Understand what makes code "production-ready."

- [ ] Done

Topics:

- `pydantic-settings` for typed environment config
- Multiple environments: `local`, `test`, `production`
- Dockerizing the FastAPI app itself (`Dockerfile`)
- `docker-compose.yml` with both app + DB
- Health check endpoint (`/health` with DB ping)
- Database connection pooling
- Graceful startup/shutdown events
- What you'd add next: CI/CD, secrets management, monitoring

Outcome: The full app runs with `docker-compose up`. Interview-ready explanation of the stack.

---

## Project Structure

```
fintrack-api/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic v2 schemas
│   ├── routers/         # FastAPI route handlers
│   ├── services/        # Business logic
│   └── dependencies.py  # Auth, DB session injection
├── alembic/             # DB migrations
├── scripts/             # Seed data scripts
├── tests/               # pytest
├── docker-compose.yml
├── .env
└── requirements.txt
```
