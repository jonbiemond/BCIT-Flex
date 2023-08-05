"""Utils for configuring and cleaning up test databases.

Source: pgcli https://github.com/dbcli/pgcli
"""
from os import getenv

import psycopg2
import pytest
from sqlalchemy import engine
from sqlalchemy.orm import Session

from alembic import config, script
from alembic.runtime import migration
from bcitflex.model import Base, Course, Offering, Subject

POSTGRES_USER = getenv("PGUSER", "postgres")
POSTGRES_HOST = getenv("PGHOST", "localhost")
POSTGRES_PORT = getenv("PGPORT", 5432)
POSTGRES_PASSWORD = getenv("PGPASSWORD", "postgres")


def db_connection(dbname=None):
    """Get a psycopg2 connection to the database."""
    conn = psycopg2.connect(
        user=POSTGRES_USER,
        host=POSTGRES_HOST,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
        dbname=dbname,
    )
    conn.autocommit = True
    return conn


try:
    conn = db_connection()
    CAN_CONNECT_TO_DB = True
except Exception:
    CAN_CONNECT_TO_DB = False


dbtest = pytest.mark.skipif(
    not CAN_CONNECT_TO_DB,
    reason="Need a postgres instance at localhost accessible by user 'postgres'",
)


def create_db(dbname):
    """Create a database with the given name if it does not exist."""
    with db_connection().cursor() as cur:
        cur.execute(f"SELECT datname FROM pg_database WHERE datname = '{dbname}';")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {dbname};")


def drop_tables(conn):
    """Drop all tables in the public schema."""
    with conn.cursor() as cur:
        cur.execute(
            """
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public;"""
        )


def check_current_head(alembic_cfg: config.Config, connectable: engine.Engine) -> bool:
    """Check if the database is up-to-date with the latest migrations."""
    directory = script.ScriptDirectory.from_config(alembic_cfg)
    with connectable.begin() as connection:
        context = migration.MigrationContext.configure(connection)
        return set(context.get_current_heads()) == set(directory.get_heads())


def clone_model(model: Base, **kwargs) -> Base:
    """Clone an arbitrary sqlalchemy model object without its primary key values."""
    table = model.__table__
    non_pk_columns = [
        k for k in table.columns.keys() if k not in table.primary_key.columns.keys()
    ]
    data = {c: getattr(model, c) for c in non_pk_columns}
    data.update(kwargs)

    clone = model.__class__(**data)
    return clone


def populate_db(session: Session):
    """Populate the database with test data."""
    subject = Subject(subject_id="COMP", name="Computer Systems")
    course = Course(
        course_id=1,
        subject_id="COMP",
        code="1234",
        name="Test Course",
        prerequisites="COMP 1000",
        credits=3.0,
        url="https://www.bcit.ca",
    )
    offering = Offering(
        crn="12345",
        instructor="John Doe",
        price=123.45,
        duration="1 week",
        meeting_time="Day   Time    Location\nWed    16:00 - 19:00 DTC",
        status="Open",
        course_id=1,
    )
    session.add(subject)
    session.add(course)
    session.add(offering)
    session.commit()
