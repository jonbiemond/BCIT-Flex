"""Test the app factory."""

from bcitflex import create_app
from tests import dbtest
from tests.conftest import DB_URL


@dbtest
def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": DB_URL}).testing
    assert create_app({"TESTING": True}).testing
