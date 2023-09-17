from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase
from sqlalchemy import FromClause, Join, Table
from sqlalchemy.event import listens_for
from sqlalchemy.orm import DeclarativeBase, ORMExecuteState, Session
from sqlalchemy.orm.util import _ORMJoin
from sqlalchemy.sql import (
    Executable,
    Select,
)


class SQLAlchemy(SQLAlchemyBase):
    """Flask extension that integrates DeclarativeBase with Flask-SQLAlchemy."""

    def __init__(self, model: DeclarativeBase, app=None, session_options=None):
        self.Model = model
        super(SQLAlchemy, self).__init__(
            app=app, session_options=session_options, metadata=model.metadata
        )

    def _make_declarative_base(self, *args, **kwargs):
        """Creates or extends the declarative base."""
        return self.Model


# Soft delete hook functions
def rewrite_statement(stmt: Executable) -> Select:
    """Rewrite a single SQL-like Statement."""

    if isinstance(stmt, Select):
        for from_clause in stmt.get_final_froms():
            stmt = rewrite_from_clause(stmt, from_clause)

        return stmt

    raise NotImplementedError(f'Unsupported statement type "{(type(stmt))}"!')


def rewrite_from_clause(stmt: Select, from_clause: FromClause):
    """Rewrite a single from clause."""

    if isinstance(from_clause, Table):
        deleted_field = from_clause.columns.get("deleted_at")
        stmt = stmt.where(deleted_field.is_(None))

    elif isinstance(from_clause, _ORMJoin):
        # not expecting recursive joins
        if any(
            type(j) in (_ORMJoin, Join) for j in (from_clause.left, from_clause.right)
        ):
            raise NotImplementedError(
                f"Recursive joins are not supported! Join: {from_clause}"
            )
        # rewrite the left and right sides of the join
        stmt = rewrite_from_clause(stmt, from_clause.left)
        stmt = rewrite_from_clause(stmt, from_clause.right)

    else:
        raise NotImplementedError(f'Unsupported froms type "{(type(from_clause))}"!')

    return stmt


@listens_for(Session, identifier="do_orm_execute")
def soft_delete_execute(state: ORMExecuteState):
    if not state.is_select:
        return

    # If soft delete is disabled, don't rewrite the statement
    if state.statement.get_execution_options().get("include_deleted"):
        return

    # Rewrite the statement
    state.statement = rewrite_statement(state.statement)
