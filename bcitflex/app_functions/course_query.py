"""Filter courses."""
from typing import Type

from sqlalchemy import Column, ColumnExpressionArgument, Null, Select, select
from sqlalchemy.orm import Mapper

from bcitflex.model import Base


class ModelFilter:
    """Successively create a SQLAlchemy select statement with desired filters.

    :param model: SQLAlchemy model to select
    :param stmt: SQLAlchemy select statement
    """

    mapper: Mapper[Base]
    model: Type[Base]
    stmt: Select

    def __init__(self, model: Type[Base]):
        self.conditions: list[callable] = []
        self.model = model
        self.stmt = select(model).distinct()

    def __repr__(self) -> str:
        return f"ModelFilter({self.model.__name__})"

    def where(
        self, condition: ColumnExpressionArgument, links: list[Type[Base]] | None = None
    ):
        """Add a condition to the select statement.

        :param condition: A SQLAlchemy ColumnExpression. Left side must be a column object.
        :param links: A list of models defining the relationship path between the target model and the condition model.
        """

        links = links or []

        for model in links:
            if model.__table__ not in self.stmt.get_final_froms():
                self.stmt = self.stmt.join(model)

        if not condition.is_clause_element:
            raise ValueError("Condition must be valid clause.")

        if not isinstance(condition.left, Column):
            raise ValueError("Expected column on the left side of the expression.")

        if isinstance(condition.right, Null) or condition.right.value == "":
            return

        if condition.left.table not in self.stmt.get_final_froms():
            self.stmt = self.stmt.join(condition.left.entity_namespace)

        self.stmt = self.stmt.where(condition)
