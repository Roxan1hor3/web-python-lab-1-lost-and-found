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

contact_routers = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
    dependencies=[Depends(is_authenticated_checker)],
)

templates = Jinja2Templates(directory="src/lost_and_found/templates")


@contact_routers.get("/")
async def get_contacts(
    request: Request,
):
    user = getattr(request.state, "user", None)
    return templates.TemplateResponse(
        request=request,
        name="contacts.j2",
        context={
            "authors": [
                {"name": "Хусаінов Дмитро ІО-11"},
                {"name": "Шинкарчук Богдан ІО-11"},
                {"name": "Столярчук Микола ІО-11"},
            ],
            "page_title": "Про нас",
            "is_authenticated": True
            if user is not None and user.session_uuid is not None
            else False,
            "user": user,
        },
    )


@contact_routers.post("/")
async def add_ask(
    request: Request,
    email: Annotated[str, Form()],
    text: Annotated[str, Form()],
    lost_and_found_service: LostAndFoundService = Depends(get_lost_and_found_service),
    session: AsyncSession = Depends(get_session),
):
    user = getattr(request.state, "user", None)
    await lost_and_found_service.create_feedback_message(
        email=email, text=text, session=session
    )
    return templates.TemplateResponse(
        request=request,
        name="contacts.j2",
        context={
            "authors": [
                {"name": "Хусаінов Дмитро ІО-11"},
                {"name": "Шинкарчук Богдан ІО-11"},
                {"name": "Столярчук Микола ІО-11"},
            ],
            "page_title": "Про нас",
            "is_authenticated": True
            if user is not None and user.session_uuid is not None
            else False,
            "user": user,
        },
    )
