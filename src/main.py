"""Main module."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.endpoints import boards
from src.core.config import settings

app = FastAPI()

app.include_router(boards.router, prefix="/api/boards", tags=["boards"])

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Trello Services API",
        "version": settings.VERSION,
        "docs": "/docs",
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}



@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Value error handler."""
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": str(exc),
        }
    )
