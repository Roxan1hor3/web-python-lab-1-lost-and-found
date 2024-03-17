from enum import StrEnum
from typing import Callable

from pydantic import BaseModel
from sqlalchemy import Select, text


class BaseFilterModel(BaseModel):
    pass


class BaseSortModel(BaseModel):
    def generate_params(self) -> list[text]:
        order_by = []
        for name, value in self.dict(exclude_unset=True).items():
            order_by.append(text(f"{name} {value}"))

        return order_by


class SortOption(StrEnum):
    ASC = "ASC"
    DESC = "DESC"


class Query:
    expr_modifier: Callable[[Select, str | int | float | bool], Select] = None
    filter_by: Callable[[str | int | float | bool], Select] = None

    def __init__(
        self,
        expr_modifier: Callable[[Select, str | int | float | bool], Select] = None,
        filter_by: Callable[[str | int | float | bool], Select] = None,
    ):
        self.expr_modifier = expr_modifier
        self.filter_by = filter_by

    def __call__(self, expr, value) -> Select:
        if self.expr_modifier:
            expr = self.expr_modifier(expr, value)

        if self.filter_by:
            expr = expr.filter(self.filter_by(value))

        return expr


class BaseFilter:
    field_lookup_map: dict[str, Query]

    def filter_query(self, expr: Select, filter_data: BaseModel) -> Select:
        for field, value in filter_data.model_dump(exclude_defaults=True).items():
            query = self.field_lookup_map.get(field)

            if query:
                expr = query(expr, value)

        return expr
