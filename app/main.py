from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import check_db_connection
from app.routers import transactions, accounts, categories, budgets

app = FastAPI(
    title="FinTrack API",
    description="Personal finance tracker",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router)
app.include_router(accounts.router)
app.include_router(categories.router)
app.include_router(budgets.router)


@app.get("/health", tags=["System"])
def health_check():
    db_ok = check_db_connection()
    return {
        "status": "ok" if db_ok else "degraded",
        "api": True,
        "database": db_ok,
        "environment": settings.environment,
    }


@app.get("/", tags=["System"])
def root():
    return {"message": "FinTrack API", "docs": "/docs"}
