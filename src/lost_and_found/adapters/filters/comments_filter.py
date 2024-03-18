from src.lost_and_found.adapters.filters.base import BaseFilter, Query, BaseFilterModel
from src.lost_and_found.adapters.orm import Comment


class CommentsFilter(BaseFilter):
    field_lookup_map: dict[str, Query] = {
        "join_author": Query(
            expr_modifier=lambda expr, value: expr.join(Comment.author)
        ),
        "post_id": Query(filter_by=lambda value: Comment.post_id == value),
    }


class CommentsFilterModel(BaseFilterModel):
    join_author: bool
    post_id: int
