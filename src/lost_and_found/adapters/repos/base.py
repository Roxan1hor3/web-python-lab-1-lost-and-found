from typing import TypeVar, Sequence
from uuid import UUID

from sqlalchemy import select, update, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.lost_and_found.adapters.filters.base import (
    BaseFilter,
    SortOption,
    BaseSortModel,
    BaseFilterModel,
)
from src.lost_and_found.adapters.models.base import EntityModel
from src.lost_and_found.adapters.orm import User
from src.lost_and_found.adapters.orm.base import BaseOrmModel

ORMModel = TypeVar(name="ORMModel", bound=BaseOrmModel, covariant=True)
FilterModel = TypeVar(name="FilterModel", bound=BaseFilterModel, covariant=True)
SortModel = TypeVar(name="SortModel", bound=BaseSortModel, covariant=True)


class BaseRepo:
    pass


def sort_convertor(model: BaseSortModel, sort_by: str) -> type[SortModel]:
    if not sort_by:
        return model()
    items = {item.strip() for item in sort_by.split(",")}
    data = {}

    for field in items:
        if field.startswith("-"):
            sort_field, sort_direction = field[1:], SortOption.DESC
        else:
            sort_field, sort_direction = field, SortOption.ASC

        data[sort_field] = sort_direction

    return model(**data)


class BaseSQLAlchemyRepo(BaseRepo):
    orm_model: type[BaseOrmModel]
    filter: type[BaseFilter]

    async def _get_one(self, object_id: UUID, session: AsyncSession) -> ORMModel | None:
        stmt = select(self.orm_model).where(self.orm_model.id == object_id)

        res = await session.execute(stmt)
        return res.scalar()

    async def _create(self, obj: EntityModel, session: AsyncSession) -> UUID:
        stmt = (
            insert(self.orm_model)
            .values(**obj.model_dump())
            .returning(self.orm_model.id)
        )

        uuid = await session.execute(stmt)
        await session.commit()

        return uuid.first()[0]

    async def _upsert(
        self, obj: EntityModel, session: AsyncSession, index_elements: list[str]
    ) -> ORMModel:
        stmt = (
            insert(self.orm_model)
            .values(**obj.model_dump())
            .returning(self.orm_model.id)
            .on_conflict_do_update(index_elements=index_elements, set_=obj.model_dump())
        )

        _id = await session.execute(stmt)
        await session.commit()

        return _id.first()[0]

    async def _update(
        self, object_id: int, object_data: EntityModel, session: AsyncSession
    ) -> ORMModel:
        data = object_data.model_dump(exclude_unset=True, exclude_none=True)
        stmt = (
            update(self.orm_model).where(self.orm_model.id == object_id).values(**data)
        )

        await session.execute(stmt)
        await session.commit()

    async def _get_list(
        self,
        limit: int,
        offset: int,
        filter_data: FilterModel,
        order_by: str,
        sort_option: str,
        session: AsyncSession,
    ) -> Sequence[ORMModel]:
        objects = self.filter.filter_query(
            expr=select(self.orm_model, User), filter_data=filter_data
        )

        stmt = objects.order_by(text((f"{order_by} {sort_option}")))
        query_res = await session.execute(stmt.limit(limit).offset(offset))

        return query_res.fetchall()
