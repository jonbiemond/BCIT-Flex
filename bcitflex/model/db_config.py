"""Database connection objects"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .base import Base

# Create engine and session
_engine = create_engine("postgresql://python_app@localhost:5432/bcitflex")
session = Session(_engine)

Base.metadata.create_all(_engine)
