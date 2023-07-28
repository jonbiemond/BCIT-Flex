import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


@pytest.fixture(scope="module")
def session():
    engine = create_engine("postgresql://localhost:5432/bcitflex")
    connection = engine.connect()

    # begin a non-ORM transaction
    trans = connection.begin()

    # bind an individual Session to the connection with "create_savepoint"
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    # start a SAVEPOINT transaction
    yield session

    # rollback - everything above is rolled back including calls to commit()
    trans.rollback()
    connection.close()
