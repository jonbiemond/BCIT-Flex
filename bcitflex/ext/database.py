from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase
from sqlalchemy.orm import DeclarativeBase


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
