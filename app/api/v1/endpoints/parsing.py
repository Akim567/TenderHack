from fastapi import APIRouter, HTTPException, status

from app.schemas.parsing import ParseJobRequest, ParseJobResponse

router = APIRouter(prefix="/parsing")


@router.post(
    "/jobs",
    response_model=ParseJobResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create parsing job",
)
async def create_parse_job(payload: ParseJobRequest) -> ParseJobResponse:
    """Business endpoint contract. Implementation will be added later."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Parsing workflow is not implemented yet.",
    )
