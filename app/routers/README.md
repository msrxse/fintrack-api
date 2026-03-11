# Routers

Each file in this folder is a FastAPI `APIRouter` handling one resource. All routers are registered in `main.py`.

---

## JOIN Reference

### Relationship types

| Type         | Description               | JOINs needed           | Example             |
| ------------ | ------------------------- | ---------------------- | ------------------- |
| One-to-one   | 1 row matches 1 row       | 1                      | user → profile      |
| One-to-many  | 1 row matches many rows   | 1                      | user → accounts     |
| Many-to-many | many rows match many rows | 2 (via junction table) | transactions → tags |

### JOIN types

| JOIN type  | SQLAlchemy     | When to use            |
| ---------- | -------------- | ---------------------- |
| INNER JOIN | `.join()`      | Both sides must exist  |
| LEFT JOIN  | `.outerjoin()` | Right side is optional |

### Notes

1. > One table → no JOIN. Two tables → one JOIN. Three tables → two JOINs.

SQLAlchemy infers the `FROM` clause from the models you reference — no need to write it explicitly.

2. `.join()` is INNER JOIN by default. To do a LEFT JOIN:

```python
.outerjoin(Category, Transaction.category_id == Category.id)
```

### One table — no JOIN

```python
db.query(Transaction.amount).all()
```

```sql
SELECT amount FROM transactions
```

### Two tables — one JOIN

```python
db.query(Category.name, Transaction.amount)
  .join(Transaction, Transaction.category_id == Category.id)
  .all()
```

```sql
SELECT categories.name, transactions.amount
FROM categories
JOIN transactions ON transactions.category_id = categories.id
```
