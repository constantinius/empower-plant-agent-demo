"""Main FastAPI application for the AI Agent."""

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from config import settings

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    environment=settings.sentry_environment,
    traces_sample_rate=settings.sentry_traces_sample_rate,
    profiles_sample_rate=settings.sentry_profiles_sample_rate,
)

# Create FastAPI app
app = FastAPI(
    title="Empower Plant Agent API",
    description="AI-powered plant care and empowerment assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["agent"])


@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "Welcome to the Empower Plant Agent API",
        "docs": "/docs",
        "health": "/api/v1/health",
        "version": "1.0.0",
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
