import datetime
from typing import Type

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from alembic import config
from bcitflex.model import Course, Meeting, Offering, Subject, Term
from tests.db_test_utils import (
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
    check_current_head,
    create_db,
    db_connection,
    drop_tables,
    populate_db,
    setup_db,
)

DB_NAME = "_test_bcitflex"
DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_NAME}"


@pytest.fixture(scope="class")
def session(request) -> Session:
    """Create a database and return a session to that database."""

    # create the database
    create_db(DB_NAME)
    psycopg2_connection = db_connection(DB_NAME)

    # connect to the database with sqlalchemy
    engine = create_engine(DB_URL)

    # run the migrations
    alembic_cfg = config.Config("tests/alembic.ini")
    if not check_current_head(alembic_cfg, engine):
        config.command.upgrade(alembic_cfg, "head")

    # begin a non-ORM transaction
    connection = engine.connect()
    trans = connection.begin()

    # bind an individual Session to the connection with "create_savepoint"
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    # setup db
    setup_db(session)

    # populate db
    marker = request.node.get_closest_marker("empty_db")
    if marker is None:
        populate_db(session)

    # start a SAVEPOINT transaction
    yield session

    # rollback - everything above is rolled back including calls to commit()
    trans.rollback()
    connection.close()

    # clean the database
    drop_tables(psycopg2_connection)
    psycopg2_connection.close()


# Model fixtures
@pytest.fixture
def subject(session) -> Type[Subject]:
    """Get a test subject."""
    subject = session.get(Subject, "COMP")
    if subject is None:
        raise ValueError("Subject not found in database.")
    return subject


@pytest.fixture
def course(session) -> Type[Course]:
    """Get a test course."""
    course = session.get(Course, 1)
    if course is None:
        raise ValueError("Course not found in database.")
    return course


@pytest.fixture
def offering(session) -> Type[Offering]:
    """Get a test offering."""
    offering = session.get(Offering, "12345")
    if offering is None:
        raise ValueError("Offering not found in database.")
    return offering


@pytest.fixture
def new_subject() -> Subject:
    """Return a new subject object."""
    return Subject(subject_id="MATH", name="Mathematics")


@pytest.fixture
def new_course() -> Course:
    """Return a new course object."""
    return Course(
        course_id=2,
        subject_id="COMP",
        code="1234",
        name="Test Course",
        prerequisites="COMP 1000",
        credits=3.0,
        url="https://www.bcit.ca",
    )


@pytest.fixture
def new_offering() -> Offering:
    """Return a new offering object."""
    return Offering(
        crn="67890",
        instructor="John Doe",
        price=123.45,
        duration="1 week",
        status="Open",
        course_id=1,
        term_id="202330",
    )


@pytest.fixture
def new_meeting() -> Meeting:
    """Return a new meeting object."""
    return Meeting(
        crn="12345",
        start_date=datetime.date(2023, 9, 13),
        end_date=datetime.date(2023, 11, 29),
        days=["Wed"],
        start_time=datetime.time(18),
        end_time=datetime.time(21),
        campus="Online",
    )


@pytest.fixture
def new_term() -> Term:
    """Return a new term object."""
    return Term(term_id="202410", year=2024, season="Winter")
