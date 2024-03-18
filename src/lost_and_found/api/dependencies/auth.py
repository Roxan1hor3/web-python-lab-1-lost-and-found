from uuid import UUID

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.lost_and_found.adapters.services.lost_and_found_service import (
    LostAndFoundService,
)
from src.lost_and_found.api.dependencies.services import get_lost_and_found_service
from src.lost_and_found.extensions.db import get_session


async def is_authenticated_checker(
    request: Request,
    lost_and_found_service: LostAndFoundService = Depends(get_lost_and_found_service),
    session: AsyncSession = Depends(get_session),
) -> Request:
    session_uuid = request.cookies.get("session_uuid", None)
    if session_uuid is None:
        request.state.user = None
        return request
    user = await lost_and_found_service.get_user_by_session_uuid(
        session_uuid=UUID(session_uuid), session=session
    )
    request.state.user = user
    return request
