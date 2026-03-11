from fastapi import APIRouter

from app.api.v1.endpoints import auth, parsing, system

api_router = APIRouter()
api_router.include_router(system.router, tags=["system"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(parsing.router, tags=["parsing"])
