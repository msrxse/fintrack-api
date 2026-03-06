# Models

SQLAlchemy ORM models. Each file = one database table.

## Tables

### users
Stores user accounts. Foundation of the schema — everything else belongs to a user.
- `id` — primary key, auto-increment
- `email` — unique, indexed for fast login lookups
- `hashed_password` — bcrypt hash, never plain text
- `is_active` — deactivate users without deleting them
- `created_at` — set by the database automatically via `server_default`

### accounts
A user's bank accounts (checking, savings, credit, investment).
- `user_id` — foreign key to users (one user → many accounts)
- `type` — restricted to an Enum: checking, savings, credit, investment
- `balance` — `Numeric(12, 2)`, never Float (floats have rounding errors with money)
- `currency` — 3-char ISO code, defaults to EUR

### categories
Transaction categories (Food, Rent, Salary, etc). Can be system-level or user-created.
- `is_system` — True for built-in categories shared across all users
- `user_id` — nullable. NULL = system category, set = user-created category
- Both fields together make queries explicit and readable

### transactions
The core of the app. Every money movement lives here.
- `amount` — always positive. Direction is determined by `type`
- `type` — Enum: income or expense
- `date` — the actual transaction date, not `created_at`
- `is_deleted` — soft delete. Financial records are never hard-deleted
- `category_id` — nullable, a transaction can be uncategorized
- `merchant` — who was paid (Amazon, Netflix, Uber, etc)

### budgets
Spending limits per category per period.
- `limit_amount` — the cap the user sets
- `period` — Enum: weekly or monthly
- `UniqueConstraint` on (user_id, category_id, period) — one budget per category per period per user

## Key Concepts

**ORM** — Each class maps to a table. Instances of the class map to rows.

**ForeignKey** — Creates the link between tables at the database level. The column stores the `id` of the related row.

**relationship()** — Python-side navigation only, no DB column created. Lets you do `user.accounts` or `account.user`.

**One-to-many** — One user has many accounts. Enforced by `ForeignKey` on the "many" side.

**One-to-one** — Same as above but add `unique=True` on the FK and `uselist=False` on the relationship.

**Enum** — Restricts a column to a fixed set of values. Enforced at the DB level.

**Soft delete** — Set `is_deleted = True` instead of running DELETE. Preserves history.

**server_default=func.now()** — The database sets the timestamp, not Python. More reliable across timezones and concurrent requests.

**UniqueConstraint** — Enforces that a combination of columns must be unique across all rows.

## Why __init__.py imports all models

Alembic can only generate migrations for models it knows about. Models are registered with SQLAlchemy's `Base` when their file is imported. Importing everything in `__init__.py` ensures all models are registered when Alembic runs.
