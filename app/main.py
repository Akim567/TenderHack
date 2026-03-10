from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import setup_logging
from app.core.middleware import register_middlewares


def create_app() -> FastAPI:
    """Build and configure FastAPI application instance."""
    settings = get_settings()

    setup_logging(level=settings.log_level, app_env=settings.app_env)

    application = FastAPI(
        title=settings.app_name,
        description="Backend template for a distributed monolith architecture.",
        version="0.1.0",
        debug=settings.debug,
    )

    register_middlewares(application, settings)
    register_exception_handlers(application)

    @application.get("/health", tags=["system"], summary="Application healthcheck")
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    application.include_router(api_router, prefix="/api/v1")
    return application


app = create_app()
