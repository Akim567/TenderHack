from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.db import get_db_session
from app.schemas.auth import UserResponse
from app.services.auth_service import AuthService
from app.services.parser_service import ParserService

bearer_scheme = HTTPBearer(auto_error=False)


def get_settings_dependency() -> Settings:
    """Provide application settings from cached configuration."""
    return get_settings()


def get_parser_service(
    db_session: Session = Depends(get_db_session),
    settings: Settings = Depends(get_settings_dependency),
) -> ParserService:
    """Provide parser service with all required dependencies."""
    return ParserService(db_session=db_session, settings=settings)


def get_auth_service(
    db_session: Session = Depends(get_db_session),
    settings: Settings = Depends(get_settings_dependency),
) -> AuthService:
    """Provide auth service with all required dependencies."""
    return AuthService(db_session=db_session, settings=settings)


def get_bearer_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    """Extract bearer token from Authorization header."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


async def get_current_user(
    token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """Resolve current authenticated user."""
    try:
        return await auth_service.get_current_user(token)
    except NotImplementedError as exc:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=str(exc),
        ) from exc
