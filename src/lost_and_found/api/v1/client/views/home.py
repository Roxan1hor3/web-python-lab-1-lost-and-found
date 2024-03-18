from fastapi import APIRouter, Request, Depends
from starlette.templating import Jinja2Templates

from src.lost_and_found.api.dependencies.auth import is_authenticated_checker

home_routers = APIRouter(
    prefix="/home",
    tags=["home"],
    dependencies=[Depends(is_authenticated_checker)],
)

templates = Jinja2Templates(directory="src/lost_and_found/templates")


@home_routers.get("/")
async def home(
    request: Request,
):
    user = getattr(request.state, "user", None)
    print(user)
    return templates.TemplateResponse(
        request=request,
        name="homepage.j2",
        context={
            "page_title": "Головна сторінка",
            "is_authenticated": True
            if user is not None and user.session_uuid is not None
            else False,
            "user": user,
        },
    )
