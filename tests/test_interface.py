"""Tests for interface functions."""
from sqlalchemy.orm import Session

from bcitflex.interface import valid_subject
from tests import dbtest


@dbtest
def test_valid_subject(session: Session) -> None:
    """Test valid_subject returns subject validity."""
    assert valid_subject(session, "COMP") is True
    assert valid_subject(session, "ABCD") is False
