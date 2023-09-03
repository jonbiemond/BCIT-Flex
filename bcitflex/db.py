"""App db config"""

from flask import Flask

from .ext.database import SQLAlchemy
from .model.base import Base
from .scripts import load_db_command

db = SQLAlchemy(model=Base)
DBSession = db.session


def init_app(app: Flask):
    """Initialize app."""
    db.init_app(app)
    app.cli.add_command(load_db_command)
