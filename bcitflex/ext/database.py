from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase
from sqlalchemy import Table
from sqlalchemy.event import listens_for
from sqlalchemy.orm import DeclarativeBase, ORMExecuteState, Session
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

    def _make_declarative_base(self, _):
        """Creates or extends the declarative base."""
        return self.Model


# Soft delete hook functions
def rewrite_statement(stmt: Executable) -> Select:
    """Rewrite a single SQL-like Statement."""

    if isinstance(stmt, Select):
        for from_clause in stmt.get_final_froms():
            if isinstance(from_clause, Table):
                deleted_field = from_clause.columns.get("deleted_at")
                stmt = stmt.where(deleted_field.is_(None))

            else:
                raise NotImplementedError(
                    f'Unsupported froms type "{(type(from_clause))}"!'
                )

        return stmt

    raise NotImplementedError(f'Unsupported statement type "{(type(stmt))}"!')


@listens_for(Session, identifier="do_orm_execute")
def soft_delete_execute(state: ORMExecuteState):
    if not state.is_select:
        return

    # If soft delete is disabled, don't rewrite the statement
    if state.statement.get_execution_options().get("include_deleted"):
        return

    # Rewrite the statement
    state.statement = rewrite_statement(state.statement)
