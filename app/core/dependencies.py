from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.db import get_db_session
from app.services.parser_service import ParserService


def get_settings_dependency() -> Settings:
    """Provide application settings from cached configuration."""
    return get_settings()


def get_parser_service(
    db_session: Session = Depends(get_db_session),
    settings: Settings = Depends(get_settings_dependency),
) -> ParserService:
    """Provide parser service with all required dependencies."""
    return ParserService(db_session=db_session, settings=settings)
