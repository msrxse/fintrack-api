import logging
import time
from typing import Awaitable, Callable

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import check_db_connection
from app.routers import accounts, analytics, auth, budgets, categories, transactions

logging.basicConfig(level=logging.INFO)

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

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(accounts.router)
app.include_router(categories.router)
app.include_router(budgets.router)
app.include_router(analytics.router)

@app.exception_handler(HTTPException)
def fastapi_exception_handler(request, exc):
    return JSONResponse(
        status_code = exc.status_code,
        content = {"error": exc.detail, "status_code": exc.status_code},
    )

@app.exception_handler(RequestValidationError)
def pydantic_exception_handler(request, exc):
    return JSONResponse(
        status_code = 422,
        content = {"error": "Validation error", "detail": exc.errors()},
    )

@app.exception_handler(Exception)
def unhandled_exception_handler(request, exc):
    return JSONResponse(
        status_code = 500,
        content = {"error": "Internal server error", "status_code": 500},
    )


@app.middleware("http")
async def add_logger(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    start_time = time.time()
    response = await call_next(request)
    logging.info(f"Completed in {(time.time() - start_time) * 1000:.0f}ms")
    return response

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
