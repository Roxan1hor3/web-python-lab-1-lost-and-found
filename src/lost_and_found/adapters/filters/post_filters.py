from src.lost_and_found.adapters.filters.base import BaseFilterModel, BaseFilter, Query
from src.lost_and_found.adapters.orm import Post


class PostFilter(BaseFilter):
    field_lookup_map: dict[str, Query] = {
        "join_author": Query(expr_modifier=lambda expr, value: expr.join(Post.author))
    }


class PostFilterModel(BaseFilterModel):
    join_author: bool
