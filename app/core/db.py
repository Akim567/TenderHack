from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    """Declarative base for ORM models."""


@lru_cache(maxsize=1)
def get_engine():
    """Create and cache SQLAlchemy engine from current settings."""
    settings = get_settings()
    return create_engine(settings.database_url, future=True)


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
    """Create and cache session factory."""
    return sessionmaker(bind=get_engine(), class_=Session, autoflush=False, autocommit=False)


def get_db_session() -> Generator[Session, None, None]:
    """Provide transactional SQLAlchemy session."""
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()
