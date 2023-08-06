from typing import Type

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from alembic import config
from bcitflex.model import Course, Offering, Subject
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
)

DB_NAME = "_test_bcitflex"
DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_NAME}"


@pytest.fixture(scope="module")
def database():
    """Create a database if it doesn't exist and drop any tables when done."""
    create_db(DB_NAME)
    connection = db_connection(DB_NAME)
    yield connection

    drop_tables(connection)
    connection.close()


@pytest.fixture(scope="module")
def session(database) -> Session:
    # connect to the database with sqlalchemy
    engine = create_engine(DB_URL)

    # run the migrations
    alembic_cfg = config.Config("tests/alembic.ini")
    if not check_current_head(alembic_cfg, engine):
        config.command.upgrade(alembic_cfg, "head")

    # populate the database with test data
    # session = Session(bind=engine)
    # populate_db(session)

    # begin a non-ORM transaction
    connection = engine.connect()
    trans = connection.begin()

    # bind an individual Session to the connection with "create_savepoint"
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    # populate db
    populate_db(session)

    # start a SAVEPOINT transaction
    yield session

    # rollback - everything above is rolled back including calls to commit()
    trans.rollback()
    connection.close()


# TODO: make session fixture dynamic and remove this one
@pytest.fixture(scope="function")
def empty_session(database) -> Session:
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

    # start a SAVEPOINT transaction
    yield session

    # rollback - everything above is rolled back including calls to commit()
    trans.rollback()
    connection.close()


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
        meeting_time="Day   Time    Location\nWed    16:00 - 19:00 DTC",
        status="Open",
        course_id=1,
    )
