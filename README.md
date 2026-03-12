# FinTrack API

Personal finance tracker built with FastAPI + PostgreSQL.

## Requirements
- Python 3.11+
- Docker Desktop
- Poetry

## Start

```bash
# 1. Configure Poetry to create .venv inside the project (run once)
poetry config virtualenvs.in-project true

# 2. Install dependencies
poetry install

# 2. Start PostgreSQL
docker-compose up -d

# 3. Start the API
poetry run uvicorn app.main:app --reload
```

API runs at http://localhost:8000
Docs at http://localhost:8000/docs
Health check at http://localhost:8000/health

## Stop

```bash
docker-compose down
```

## Database Access

```bash
# Connect to the database
docker exec -it fintrack_db psql -U fintrack -d fintrack_dev

# Query users
docker exec fintrack_db psql -U fintrack -d fintrack_dev -c "SELECT id, email, full_name, is_active, created_at FROM users;"
```
