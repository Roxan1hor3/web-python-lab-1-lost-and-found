from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from src.lost_and_found.adapters.services.lost_and_found_service import (
    LostAndFoundService,
)
from src.lost_and_found.api.dependencies.auth import is_authenticated_checker
from src.lost_and_found.api.dependencies.services import get_lost_and_found_service
from src.lost_and_found.extensions.db import get_session

auth_routers = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

templates = Jinja2Templates(directory="src/lost_and_found/templates")


@auth_routers.get("/login")
async def login(
    request: Request,
):
    return templates.TemplateResponse(
        request=request, name="loginpage.j2", context={"page_title": "Логин"}
    )


@auth_routers.post("/login")
async def login(
    request: Request,
    password: Annotated[str, Form()],
    username: Annotated[str, Form()],
    lost_and_found_service: LostAndFoundService = Depends(get_lost_and_found_service),
    session: AsyncSession = Depends(get_session),
):
    user = await lost_and_found_service.login_user(
        password=password, username=username, session=session
    )
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "Користувач не знайдений"},
        )
    response = templates.TemplateResponse(
        request=request,
        name="homepage.j2",
        context={
            "page_title": "Головна сторінка",
            "is_authenticated": True,
            "user": user,
        },
    )
    response.set_cookie("session_uuid", user.session_uuid.hex)
    return response


@auth_routers.get("/register")
async def register(
    request: Request,
):
    return templates.TemplateResponse(
        request=request, name="registerpage.j2", context={"page_title": "Реєстрація"}
    )


@auth_routers.post("/register")
async def register(
    request: Request,
    password: Annotated[str, Form()],
    username: Annotated[str, Form()],
    lost_and_found_service: LostAndFoundService = Depends(get_lost_and_found_service),
    session: AsyncSession = Depends(get_session),
):
    await lost_and_found_service.register_user(
        password=password, username=username, session=session
    )
    return templates.TemplateResponse(
        request=request, name="loginpage.j2", context={"page_title": "Логин"}
    )


@auth_routers.get("/logout", dependencies=[Depends(is_authenticated_checker)])
async def logout(
    request: Request,
    lost_and_found_service: LostAndFoundService = Depends(get_lost_and_found_service),
    session: AsyncSession = Depends(get_session),
):
    user = getattr(request.state, "user", None)

    if user:
        await lost_and_found_service.users_repo.update_session_uuid(
            _id=user.id, session_uuid=None, session=session
        )
    return templates.TemplateResponse(
        request=request,
        name="homepage.j2",
        context={
            "page_title": "Головна сторінка",
            "is_authenticated": False,
        },
    )
