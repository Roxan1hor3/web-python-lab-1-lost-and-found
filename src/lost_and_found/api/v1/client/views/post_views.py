from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.templating import Jinja2Templates

from src.lost_and_found.adapters.services.lost_and_found_service import (
    LostAndFoundService,
)
from src.lost_and_found.api.dependencies.auth import is_authenticated_checker
from src.lost_and_found.api.dependencies.services import get_lost_and_found_service
from src.lost_and_found.extensions.db import get_session

post_routers = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(is_authenticated_checker)],
)

templates = Jinja2Templates(directory="src/lost_and_found/templates")


@post_routers.get("/")
async def get_post_list(
    request: Request,
    lost_and_found_service: LostAndFoundService = Depends(get_lost_and_found_service),
    session: AsyncSession = Depends(get_session),
):
    user = getattr(request.state, "user", None)
    posts = await lost_and_found_service.get_post_list(session=session)
    return templates.TemplateResponse(
        request=request,
        name="postlist.j2",
        context={
            "posts": [post for post in posts],
            "is_authenticated": True
            if user is not None and user.session_uuid is not None
            else False,
            "page_title": "Знахідки",
            "user": user,
        },
    )


@post_routers.get("/{id}/")
async def get_post(
    request: Request,
    id: int,
    lost_and_found_service: LostAndFoundService = Depends(get_lost_and_found_service),
    session: AsyncSession = Depends(get_session),
):
    user = getattr(request.state, "user", None)
    post = await lost_and_found_service.get_post(session=session, _id=id)
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


@post_routers.post("/add_comment")
async def add_post(
    request: Request,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    photo: UploadFile = File(),
    lost_and_found_service: LostAndFoundService = Depends(get_lost_and_found_service),
    session: AsyncSession = Depends(get_session),
):
    user = getattr(request.state, "user", None)
    post = await lost_and_found_service.create_post(
        session=session, _id=user.id, name=name, description=description, image=photo
    )
    post = await lost_and_found_service.get_post(session=session, _id=post.id)
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


@post_routers.get("/add_comment")
async def add_post(
    request: Request,
):
    user = getattr(request.state, "user", None)
    return templates.TemplateResponse(
        request=request,
        name="addpost.j2",
        context={
            "is_authenticated": True
            if user is not None and user.session_uuid is not None
            else False,
            "page_title": "Додати пост",
            "user": user,
        },
    )
