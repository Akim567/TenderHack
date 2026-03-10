from sqlalchemy.orm import Session

from app.core.config import Settings


class ParserService:
    """Service contract for parsing workflows."""

    def __init__(self, db_session: Session, settings: Settings) -> None:
        self.db_session = db_session
        self.settings = settings

    async def create_parse_job(self, source: str) -> str:
        """Create parsing job (not implemented yet)."""
        _ = source
        raise NotImplementedError("Parsing workflow is not implemented yet.")
