# Schemas

Pydantic v2 schemas. Each file = one resource.

## Why schemas exist

SQLAlchemy models map to database tables. Schemas define what the API accepts and returns. They are never the same thing.

Reasons to keep them separate:

- Models contain fields you never expose (`hashed_password`, internal flags)
- Input and output shapes are different — creating a user needs email + password, returning a user needs id + email + created_at
- Pydantic validates and coerces data automatically — wrong types get rejected before they reach the database
- The client should not be able to set fields like `is_active` or `id` directly

## The pattern

Every resource follows the same structure:

- `UserCreate` — what the API accepts on POST (no id, no created_at)
- `UserUpdate` — what the API accepts on PUT (all fields optional)
- `UserOut` — what the API returns (no password, includes id and timestamps)

## from_attributes = True

SQLAlchemy objects are not plain dicts. By default Pydantic cannot read them.

Adding `model_config = ConfigDict(from_attributes=True)` to an output schema tells Pydantic to read attributes directly off the object — so `user.email` works the same as `{"email": "..."}`.

Only output schemas need this. Input schemas receive plain dicts from the request body.

## Decimals and dates

- `Decimal` fields from SQLAlchemy serialize correctly to JSON as numbers
- `date` and `datetime` fields serialize as ISO strings automatically
- No manual conversion needed

## Nested schemas

An output schema can embed another schema:

```python
class TransactionOut(BaseModel):
    id: int
    amount: Decimal
    category: CategoryOut  # nested
    model_config = ConfigDict(from_attributes=True)
```

This works as long as the relationship is loaded before the session closes.
