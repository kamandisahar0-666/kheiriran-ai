from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.search import router as search_router

from app.db.database import (
    test_database_connection
)


app = FastAPI(
    title="Kheir Iran AI API",

    description=(
        "Backend API for "
        "Kheir Iran AI Assistant"
    ),

    version="0.1.0"
)


# -------------------------
# Routers
# -------------------------

app.include_router(
    search_router
)

app.include_router(
    chat_router
)


# -------------------------
# Root
# -------------------------

@app.get("/")
async def root():

    return {
        "message":
            "Kheir Iran AI API is running"
    }


# -------------------------
# Health
# -------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "kheiriran-ai"
    }


# -------------------------
# Database Health
# -------------------------

@app.get("/health/database")
async def database_health():

    try:

        result = (
            test_database_connection()
        )

        return {
            "status": "ok",
            "database": "connected",
            "result": result
        }

    except Exception as exc:

        return {
            "status": "error",
            "database": "disconnected",
            "error": str(exc)
        }