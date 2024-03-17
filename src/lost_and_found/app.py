from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from src.lost_and_found.api.dependencies import services
from src.lost_and_found.config import get_settings

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
        title="Synthetic LostAndFound service API",
        strict_slashes=True,
        **docs_args,
    )
    setup_middleware(app)

    # app.include_router(v1_router, prefix="/api")

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
