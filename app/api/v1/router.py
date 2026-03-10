from fastapi import APIRouter

from app.api.v1.endpoints import parsing, system

api_router = APIRouter()
api_router.include_router(system.router, tags=["system"])
api_router.include_router(parsing.router, tags=["parsing"])
