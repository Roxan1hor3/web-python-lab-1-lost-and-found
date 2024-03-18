from src.lost_and_found.adapters.filters.base import SortOption
from src.lost_and_found.adapters.filters.comments_filter import (
    CommentsFilterModel,
    CommentsFilter,
)
from src.lost_and_found.adapters.models.comment import CommentRetrieveModel
from src.lost_and_found.adapters.orm import Comment
from src.lost_and_found.adapters.repos.base import BaseSQLAlchemyRepo


class CommentRepo(BaseSQLAlchemyRepo):
    orm_model = Comment
    filter = CommentsFilter()

    async def get_comments_by_post_id(self, post_id, session):
        results = await self._get_list(
            limit=100,
            offset=0,
            filter_data=CommentsFilterModel(join_author=True, post_id=post_id),
            session=session,
            order_by="date",
            sort_option=SortOption.ASC,
        )
        return [
            CommentRetrieveModel(
                post_id=result[0].post_id,
                id=result[0].id,
                author_id=result[0].author_id,
                text=result[0].text,
                date=result[0].date,
                author=result[1],
            )
            for result in results
        ]

    async def create(self, comment, session):
        await self._create(obj=comment, session=session)
