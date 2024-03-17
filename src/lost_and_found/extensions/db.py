from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.lost_and_found.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.DB_URL.unicode_string(), echo=settings.SQLA_ECHO)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
