from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from src.lost_and_found.adapters.services.lost_and_found_service import (
    LostAndFoundService,
)
from src.lost_and_found.api.dependencies.auth import is_authenticated_checker
from src.lost_and_found.api.dependencies.services import get_lost_and_found_service
from src.lost_and_found.extensions.db import get_session

comments_routers = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(is_authenticated_checker)],
)

templates = Jinja2Templates(directory="src/lost_and_found/templates")


@comments_routers.get("/{post_id}")
async def add_comment(
    request: Request,
    post_id: int,
):
    user = getattr(request.state, "user", None)
    return templates.TemplateResponse(
        request=request,
        name="addcomment.j2",
        context={
            "post_id": post_id,
            "is_authenticated": True
            if user is not None and user.session_uuid is not None
            else False,
            "page_title": "Коментарі",
            "user": user,
        },
    )


@comments_routers.post("/{post_id}")
async def add_comment(
    request: Request,
    post_id: int,
    comment_text: Annotated[str, Form()],
    lost_and_found_service: LostAndFoundService = Depends(get_lost_and_found_service),
    session: AsyncSession = Depends(get_session),
):
    user = getattr(request.state, "user", None)
    comment = await lost_and_found_service.create_comment(
        comment_text=comment_text, post_id=post_id, author_id=user.id, session=session
    )
    post = await lost_and_found_service.get_post(session=session, _id=post_id)
    post.comments.append(comment)
    return templates.TemplateResponse(
        request=request,
        name="showpost.j2",
        context={
            "post": post,
            "is_authenticated": True
            if user is not None and user.session_uuid is not None
            else False,
            "page_title": "Знахідки",
            "user": user,
        },
    )
