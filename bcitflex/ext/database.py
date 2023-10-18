from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase
from sqlalchemy.event import listens_for
from sqlalchemy.orm import (
    DeclarativeBase,
    ORMExecuteState,
    Session,
    with_loader_criteria,
)

from bcitflex.model.base import SoftDeleteMixin


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
@listens_for(Session, identifier="do_orm_execute")
def soft_delete_execute(state: ORMExecuteState):
    """Activate an event hook to rewrite the queries."""

    if state.is_select and not state.execution_options.get("include_deleted"):
        state.statement = state.statement.options(
            with_loader_criteria(
                SoftDeleteMixin,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )
