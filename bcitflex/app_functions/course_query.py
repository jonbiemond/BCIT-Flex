"""Filter courses."""
from typing import Type

from sqlalchemy import (
    BindParameter,
    Column,
    ColumnExpressionArgument,
    FromClause,
    Join,
    Null,
    Select,
    Table,
    select,
)

from bcitflex.model import Base


def from_tables(from_: FromClause) -> list[Table]:
    """Return a list of tables in a from clause."""
    tables = []
    if isinstance(from_, Table):
        tables.append(from_)
    elif isinstance(from_, Join):
        tables.extend(from_tables(from_.left))
        tables.extend(from_tables(from_.right))
    return tables


def select_tables(stmt: Select) -> list[Table]:
    """Return a list of tables in a select statement."""
    tables = []
    for from_ in stmt.get_final_froms():
        tables.extend(from_tables(from_))
    return tables


class ModelFilter:
    """Successively create a SQLAlchemy select statement with desired filters.

    :param model: SQLAlchemy model to select
    :param stmt: SQLAlchemy select statement
    """

    model: Type[Base]
    stmt: Select

    def __init__(self, model: Type[Base]):
        """Initialize the select statement.

        :param model: SQLAlchemy model to select
        """
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
        tables = select_tables(self.stmt)

        for model in links:
            if model.__table__ not in tables:
                self.stmt = self.stmt.join(model)

        if not condition.is_clause_element:
            raise ValueError("Condition must be valid clause.")

        if not isinstance(condition.left, Column):
            raise ValueError("Expected column on the left side of the expression.")

        if not isinstance(condition.right, BindParameter | Null):
            raise ValueError("Expected parameter on the right side of the expression.")

        if isinstance(condition.right, Null) or condition.right.value == "":
            return

        if condition.left.table not in tables:
            self.stmt = self.stmt.join(condition.left.entity_namespace)

        self.stmt = self.stmt.where(condition)
