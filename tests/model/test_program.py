"""Tests for the program model."""

from sqlalchemy.orm import Session

from bcitflex.model.program import Program
from tests import dbtest


@dbtest
class TestProgramDB:
    """Test the Program class with a database session."""

    def test_get_programs(self, db_session: Session):
        """Test the get_programs method."""
        program = db_session.get(Program, 1)
        assert program.name == "Computer Systems Technology (CST)"
