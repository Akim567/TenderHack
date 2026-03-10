from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Service healthcheck")
async def healthcheck() -> dict[str, str]:
    """Infrastructure-level probe endpoint.

    No business logic should live here.
    """
    return {"status": "ok"}
