FROM python:3.11-slim

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
