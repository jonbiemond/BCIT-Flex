"""Database connection objects"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Create engine and session
engine = create_engine("postgresql://python_app@localhost:5432/bcitflex")
session = Session(engine)
