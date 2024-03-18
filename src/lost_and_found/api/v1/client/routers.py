from fastapi import APIRouter

from src.lost_and_found.api.v1.client.views.auth import auth_routers
from src.lost_and_found.api.v1.client.views.comments import comments_routers
from src.lost_and_found.api.v1.client.views.contacts import contact_routers
from src.lost_and_found.api.v1.client.views.home import home_routers
from src.lost_and_found.api.v1.client.views.post_views import post_routers

client_router = APIRouter(
    prefix="/client",
)

client_router.include_router(home_routers)
client_router.include_router(post_routers)
client_router.include_router(contact_routers)
client_router.include_router(comments_routers)
client_router.include_router(auth_routers)
