from fastapi import FastAPI, Request
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.lost_and_found.api.dependencies import services
from src.lost_and_found.api.v1.admin.views.admin import UserAdmin, FeedbackMessageAdmin, CommentAdmin, PostAdmin
from src.lost_and_found.api.v1.routers import v1_router
from src.lost_and_found.config import get_settings
from src.lost_and_found.extensions.db import engine

settings = get_settings()


def create_app() -> FastAPI:
    """Application factory."""
    docs_args = {}
    if settings.USE_DOCS:
        docs_args = {
            "docs_url": "/api/docs/",
            "openapi_url": "/api/openapi.json",
        }

    app = FastAPI(
        title="LostAndFound service API",
        strict_slashes=True,
        **docs_args,
    )
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(FeedbackMessageAdmin)
    admin.add_view(CommentAdmin)
    admin.add_view(PostAdmin)
    app.mount(
        "/static",
        StaticFiles(directory="src/lost_and_found/templates/static"),
        name="static",
    )
    app.mount(
        "/photos",
        StaticFiles(directory="photos"),
        name="photos",
    )
    setup_middleware(app)

    app.include_router(v1_router, prefix="/api")

    # attach_exception_handlers(app)

    register_events(app=app)

    return app


def setup_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    )

    @app.middleware("http")
    async def get_accept_language(request: Request, call_next):
        response = await call_next(request)
        return response


def register_events(app: FastAPI):
    @app.on_event("startup")
    def init_service_manager():
        services.init_service_manager(settings=settings)
