from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase


class SQLAlchemy(SQLAlchemyBase):
    """Flask extension that integrates alchy with Flask-SQLAlchemy."""

    def __init__(self, app=None, session_options=None, model=None):
        self.Model = model
        super(SQLAlchemy, self).__init__(app=app, session_options=session_options)

    def _make_declarative_base(self, _):
        """Creates or extends the declarative base."""
        return self.Model
