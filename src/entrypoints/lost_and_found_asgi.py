import uvicorn

from src.lost_and_found.app import create_app
from src.lost_and_found.config import get_settings

settings = get_settings()

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app="src.entrypoints.lost_and_found_asgi:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_DEBUG,
    )
