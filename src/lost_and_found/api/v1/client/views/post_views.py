from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.notify.adapters.models.email_blacklist import EmailBlacklistRetrieveModel
from src.notify.extensions.db import get_session_depends
from starlette.templating import Jinja2Templates

from src.lost_and_found.adapters.services.lost_and_found_service import (
    LostAndFoundService,
)
from src.lost_and_found.api.dependencies.services import get_lost_and_found_service

post_routers = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

templates = Jinja2Templates(directory="templates")


@post_routers.get("/", response_model=ResponsePostListSchema)
async def add_email_to_blacklist(
    post_params: PostListQueryParams,
    lost_and_found_service: LostAndFoundService = Depends(get_lost_and_found_service),
    session: AsyncSession = Depends(get_session_depends),
) -> EmailBlacklistRetrieveModel:
    results, count = await lost_and_found_service.get_post_list(session=session)
    # return {"results": results, "count": count}
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )
