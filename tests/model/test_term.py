"""Tests for the term model."""
from sqlalchemy.orm import Session

from bcitflex.model import Term
from tests import dbtest


class TestTerm:
    """Test properties of the Term class."""

    def test_init(self, new_term: Term) -> None:
        """Test the constructor."""
        assert new_term.term_id == "202410"
        assert new_term.year == 2024
        assert new_term.season == "Winter"

    def test_repr(self, new_term: Term) -> None:
        """Test the repr method."""
        assert new_term.__repr__() == "Term(202410)"


@dbtest
class TestTermDB:
    """Test the Term class with a database session."""

    def test_get_term(self, session: Session) -> None:
        """Test getting a term."""
        term = session.get(Term, "202330")
        assert term.term_id == "202330"
