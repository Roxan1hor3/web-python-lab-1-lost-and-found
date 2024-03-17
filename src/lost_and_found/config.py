from functools import lru_cache
from typing import Sequence

from pydantic import PostgresDsn
from pydantic.v1 import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    API_PORT: int = 8000
    API_HOST: str = "127.0.0.1"
    API_DEBUG: bool = False

    ADMIN_API_KEY: str

    DB_URL: PostgresDsn
    POSTGRES_ECHO_MODE: bool = True

    LOGGER_LEVEL: str = "DEBUG"
    LOGGER_TYPE: str = "PLAIN"

    SQLA_ECHO: bool = False

    CORS_ALLOW_ORIGINS: Sequence[str] = ()
    CORS_ALLOW_METHODS: Sequence[str] = ("GET",)
    CORS_ALLOW_HEADERS: Sequence[str] = ()
    CORS_ALLOW_CREDENTIALS: bool = False

    USE_DOCS: bool = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
