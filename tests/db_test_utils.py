"""Utils for configuring and cleaning up test databases.

Source: pgcli https://github.com/dbcli/pgcli
"""
import datetime
from os import getenv

import psycopg2
import pytest
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from bcitflex.model import (
    Course,
    Meeting,
    Offering,
    Subject,
    Term,
    User,
    UserPreference,
)
from bcitflex.model.prerequisite import PrerequisiteAnd, PrerequisiteOr
from bcitflex.model.program import Program

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
    """Create an empty database with the given name if it does not exist."""
    with db_connection().cursor() as cur:
        cur.execute(f"SELECT datname FROM pg_database WHERE datname = '{dbname}';")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {dbname};")
        else:
            with db_connection(dbname).cursor() as db_cur:
                db_cur.execute(
                    """
                    DROP SCHEMA public CASCADE;
                    CREATE SCHEMA public;"""
                )


def drop_tables(conn):
    """Drop all tables in the public schema."""
    with conn.cursor() as cur:
        cur.execute(
            """
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public;"""
        )


def setup_db(session: Session):
    """Set up the database for testing, runs for every session."""
    term = Term(term_id="202330", year=2023, season="Fall")
    session.add(term)
    session.commit()


def populate_db(session: Session):
    """Populate the database with test data."""
    comp = Subject(subject_id="COMP", name="Computer Systems", is_active=True)
    blaw = Subject(subject_id="BLAW", name="Business Law", is_active=False)
    ahvc = Subject(
        subject_id="AHVC", name="Asian History and Visual Culture", is_active=None
    )
    course1 = Course(
        subject_id="COMP",
        code="1234",
        name="Test Course",
        prerequisites_raw="COMP 1000",
        credits=3.0,
        url="https://www.bcit.ca",
    )
    course2 = Course(
        subject_id="COMP",
        code="1000",
        name="Test Course",
        prerequisites_raw="None",
        credits=3.0,
        url="https://www.bcit.ca",
    )
    course3 = Course(
        subject_id="COMP",
        code="3000",
        name="Test Course",
        prerequisites_raw="None",
        credits=3.0,
        url="https://www.bcit.ca",
    )
    program = Program(
        name="Computer Systems Technology (CST)",
        credential="Statement of Completion",
        url="https://www.bcit.ca",
        courses=[course1],
    )
    offering = Offering(
        crn="12345",
        instructor="John Doe",
        price=123.45,
        duration="1 week",
        status="Open",
        course_id=1,
        term_id="202330",
    )
    meeting = Meeting(
        offering_id=1,
        start_date=datetime.date(2023, 9, 13),
        end_date=datetime.date(2023, 11, 29),
        days=["Wed"],
        start_time=datetime.time(18),
        end_time=datetime.time(21),
        campus="Online",
    )
    user = User(
        username="test-user",
        password=generate_password_hash("test-password"),
    )
    user_preference = UserPreference(
        user_id=1,
        programs=[1, 2, 3],
    )
    user.preference = user_preference
    prereq_and = PrerequisiteAnd(course_id=1)
    prereq_or = PrerequisiteOr(
        prereq_and_id=1,
        course_id=2,
        criteria="60%",
    )
    session.add(comp)
    session.add(blaw)
    session.add(ahvc)
    session.add(course1)
    session.add(course2)
    session.add(course3)
    session.add(program)
    session.add(offering)
    session.add(meeting)
    session.add(user)
    session.add(prereq_and)
    session.add(prereq_or)
    session.commit()
