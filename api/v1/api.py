from fastapi import APIRouter

from api.v1.endpoints import health, user_management

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(user_management.router, tags=["user-management"])
