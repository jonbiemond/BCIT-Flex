import datetime
import uuid
from typing import Type

import pytest
from alembic import config
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from bcitflex import create_app
from bcitflex.db import DBSession, check_current_head
from bcitflex.model import Course, Meeting, Offering, Subject, Term, User
from bcitflex.model.prerequisite import PrerequisiteAnd, PrerequisiteOr
from bcitflex.model.program import Program
from bcitflex.model.user import UserPreference
from tests.db_test_utils import (
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
    create_db,
    db_connection,
    dbtest,
    drop_tables,
    populate_db,
    setup_db,
)

DB_NAME = "_test_bcitflex"
DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_NAME}"


def pytest_configure(config):
    if config.getoption("-m") == "not dbtest":
        dbtest.kwargs["condition"] = True


# Database fixtures
@pytest.fixture(scope="class")
def database():
    """Create a database if it doesn't exist and drop any tables when done."""
    create_db(DB_NAME)
    connection = db_connection(DB_NAME)
    yield connection

    drop_tables(connection)
    connection.close()


@pytest.fixture(scope="class")
def db_session(request, database) -> Session:
    """Create a database and return a session to that database."""

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


# Model fixtures
@pytest.fixture
def subject(db_session) -> Type[Subject]:
    """Get a test subject."""
    subject = db_session.get(Subject, 1)
    if subject is None:
        raise ValueError("Subject not found in database.")
    return subject


@pytest.fixture
def course(db_session) -> Type[Course]:
    """Get a test course."""
    course = db_session.get(Course, 1)
    if course is None:
        raise ValueError("Course not found in database.")
    return course


@pytest.fixture
def offering(db_session) -> Type[Offering]:
    """Get a test offering."""
    offering = db_session.get(Offering, 1)
    if offering is None:
        raise ValueError("Offering not found in database.")
    return offering


@pytest.fixture
def new_subject() -> Subject:
    """Return a new subject object."""
    return Subject(code="MATH", name="Mathematics", is_active=True)


@pytest.fixture
def new_course() -> Course:
    """Return a new course object."""
    return Course(
        subject_id=1,
        code="5678",
        name="Test Course",
        prerequisites_raw="COMP 1000",
        credits=3.0,
        url="https://www.bcit.ca",
    )


@pytest.fixture
def new_program() -> Program:
    """Return a new program object."""
    return Program(
        name="Test Program",
        credential="Test Credential",
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
        offering_id=1,
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


@pytest.fixture
def new_user() -> User:
    """Return a new user object."""
    # return user with a unique username
    return User(username=str(uuid.uuid4())[:8], password="test")


@pytest.fixture
def new_user_preference() -> UserPreference:
    """Return a new user preference object."""
    return UserPreference(user_id=1, programs=[1, 2, 3])


@pytest.fixture
def new_prereq_and() -> PrerequisiteAnd:
    """Return a new prerequisite object."""
    return PrerequisiteAnd(
        course_id=1,
    )


@pytest.fixture
def new_prereq_or() -> PrerequisiteOr:
    """Return a new prerequisite object."""
    return PrerequisiteOr(
        prereq_and_id=1,
        course_id=3,
        criteria="Test Criteria",
    )


# App fixtures
@pytest.fixture
def app(request, database) -> Flask:
    """Create and configure a new app instance for each test."""

    # connect to the database with sqlalchemy
    engine = create_engine(DB_URL)

    # run the migrations
    alembic_cfg = config.Config("tests/alembic.ini")
    if not check_current_head(alembic_cfg, engine):
        config.command.upgrade(alembic_cfg, "head")

    # create app
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": DB_URL})

    with app.app_context():
        if not DBSession().query(Course).count() != 0:
            # setup db
            setup_db(DBSession())

            # populate db
            marker = request.node.get_closest_marker("empty_db")
            if marker is None:
                populate_db(DBSession())

    yield app


@pytest.fixture
def mock_app() -> Flask:
    """A mock app for testing disconnected from the database."""
    return create_app({"TESTING": True})


@pytest.fixture
def client(app: Flask):
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()


@pytest.fixture
def mock_runner(mock_app: Flask) -> FlaskCliRunner:
    return mock_app.test_cli_runner()


class AuthActions(object):
    """Perform authentication actions on the client."""

    def __init__(self, client: FlaskClient):
        """Initialize the AuthActions object."""
        self._client = client

    def login(self, username="test-user", password="test-password"):
        """Login with the given username and password."""
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        """Logout."""
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
