"""Test the app db connection."""
import pytest
from sqlalchemy import text

from bcitflex.db import DBSession
from tests import dbtest


@dbtest
def test_get_close_db(app):
    """Test connection to db is closed after context."""
    with app.app_context():
        db = DBSession()
        assert db is DBSession()

    with pytest.raises(RuntimeError) as e:
        db.execute(text("SELECT 1"))

    assert "Working outside of application context." in str(e.value)
