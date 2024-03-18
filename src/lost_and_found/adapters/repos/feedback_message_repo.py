from sqlalchemy.ext.asyncio import AsyncSession

from src.lost_and_found.adapters.models.feedback_message import (
    FeedbackMessageCreateModel,
)
from src.lost_and_found.adapters.orm import FeedbackMessage
from src.lost_and_found.adapters.repos.base import BaseSQLAlchemyRepo


class FeedbackMessageRepo(BaseSQLAlchemyRepo):
    orm_model = FeedbackMessage

    async def create(
        self, feedback_message: FeedbackMessageCreateModel, session: AsyncSession
    ):
        await self._create(obj=feedback_message, session=session)
