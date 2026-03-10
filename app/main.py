from fastapi import FastAPI

from app.api.v1.router import api_router


def create_app() -> FastAPI:
    """Build FastAPI application with versioned API routing."""
    application = FastAPI(
        title="TenderHack Backend",
        description="Backend template for a distributed monolith architecture.",
        version="0.1.0",
    )
    application.include_router(api_router, prefix="/api/v1")
    return application


app = create_app()
