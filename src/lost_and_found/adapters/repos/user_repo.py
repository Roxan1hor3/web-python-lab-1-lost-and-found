from uuid import UUID

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.lost_and_found.adapters.models.user import UserCreateModel, UserRetrieveModel
from src.lost_and_found.adapters.orm import User
from src.lost_and_found.adapters.repos.base import BaseSQLAlchemyRepo


class UserRepo(BaseSQLAlchemyRepo):
    orm_model = User

    async def create_user(self, user: UserCreateModel, session: AsyncSession):
        await self._create(obj=user, session=session)

    async def get_user_by_username_and_password(
        self, username: str, password: str, session: AsyncSession
    ) -> UserRetrieveModel | None:
        stmt = select(self.orm_model).where(
            and_(
                self.orm_model.username == username, self.orm_model.password == password
            )
        )

        res = await session.execute(stmt)
        result = res.scalar()
        return UserRetrieveModel.model_validate(result) if result is not None else None

    async def update_session_uuid(
        self, _id: int, session_uuid: UUID, session: AsyncSession
    ):
        stmt = (
            update(self.orm_model)
            .where(self.orm_model.id == _id)
            .values(session_uuid=session_uuid)
        )

        await session.execute(stmt)
        await session.commit()

    async def get_user_by_session_uuid(self, session_uuid: UUID, session: AsyncSession):
        stmt = select(self.orm_model).where(self.orm_model.session_uuid == session_uuid)

        res = await session.execute(stmt)
        result = res.scalar()
        return UserRetrieveModel.model_validate(result) if result is not None else None
