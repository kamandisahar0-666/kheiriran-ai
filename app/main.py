from fastapi import FastAPI


app = FastAPI(
    title="Kheir Iran AI API",
    description="Backend API for Kheir Iran AI Assistant",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "message": "Kheir Iran AI API"
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "kheiriran-ai"
    }