from fastapi import APIRouter

from src.lost_and_found.api.v1.client.routers import client_router

v1_router = APIRouter(prefix="/v1", responses={404: {"description": "Not found"}})

v1_router.include_router(client_router)
