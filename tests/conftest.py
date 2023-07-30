import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from alembic import config
from tests.db_test_utils import (
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
    check_current_head,
    create_db,
    db_connection,
    drop_tables,
)

DB_NAME = "_test_bcitflex"


@pytest.fixture(scope="module")
def database():
    """Create a database if it doesn't exist and drop any tables when done."""
    create_db(DB_NAME)
    connection = db_connection(DB_NAME)
    yield connection

    drop_tables(connection)
    connection.close()


@pytest.fixture(scope="module")
def session(database):
    # connect to the database with sqlalchemy
    db_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_NAME}"
    engine = create_engine(db_url)

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
