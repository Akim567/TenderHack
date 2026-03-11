from sqlalchemy.orm import Session

from app.core.config import Settings
from app.schemas.auth import TokenResponse, UserResponse


class AuthService:
    """Service contract for authentication workflows."""

    def __init__(self, db_session: Session, settings: Settings) -> None:
        self.db_session = db_session
        self.settings = settings

    async def login(self, username: str, password: str) -> TokenResponse:
        """Authenticate user and issue access token."""
        _ = username, password
        raise NotImplementedError("JWT authentication is not implemented yet.")

    async def get_current_user(self, token: str) -> UserResponse:
        """Resolve current user from bearer token."""
        _ = token
        raise NotImplementedError("JWT authentication is not implemented yet.")
