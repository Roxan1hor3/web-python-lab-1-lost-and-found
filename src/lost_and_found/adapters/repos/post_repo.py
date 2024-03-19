from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.lost_and_found.adapters.filters.base import SortOption
from src.lost_and_found.adapters.filters.post_filters import PostFilterModel, PostFilter
from src.lost_and_found.adapters.models.post import (
    PostRetrieveModel,
    PostWithCommentsRetrieveModel,
    PostCreateModel,
)
from src.lost_and_found.adapters.orm import Post, User
from src.lost_and_found.adapters.repos.base import BaseSQLAlchemyRepo


class PostRepo(BaseSQLAlchemyRepo):
    orm_model = Post
    filter = PostFilter()

    async def get_list(self, session: AsyncSession):
        results = await self._get_list(
            limit=100,
            offset=0,
            filter_data=PostFilterModel(join_author=True),
            session=session,
            order_by="date",
            sort_option=SortOption.ASC,
        )
        return [
            PostRetrieveModel(
                name=result[0].name,
                id=result[0].id,
                description=result[0].description,
                photo=result[0].photo,
                author_id=result[0].author_id,
                date=result[0].date,
                author=result[1],
            )
            for result in results
        ]

    async def retrieve_with_comments(self, id, session):
        stmt = (
            select(self.orm_model, User)
            .join(self.orm_model.author)
            .where(self.orm_model.id == id)
            .limit(1)
        )
        res = await session.execute(stmt)
        result = res.fetchall()[0]
        return PostWithCommentsRetrieveModel(
            name=result[0].name,
            id=result[0].id,
            description=result[0].description,
            photo=result[0].photo,
            author_id=result[0].author_id,
            date=result[0].date,
            author=result[1],
            comments=[],
        )

    async def create_post(self, session: AsyncSession, post: PostCreateModel):
        post_id = await self._create(obj=post, session=session)
        post = await self.retrieve_with_comments(session=session, id=post_id)
        return PostRetrieveModel.model_validate(post)
