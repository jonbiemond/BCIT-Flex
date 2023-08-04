"""Tests for the subject model."""
import pytest
from sqlalchemy.orm import Session

from bcitflex.model import Course, Offering, Subject
from tests import dbtest


@pytest.fixture
def new_subject() -> Subject:
    """Return a new subject object."""
    return Subject(subject_id="MATH", name="Mathematics")


class TestSubject:
    """Test properties of the Subject class."""

    def test_init(self, new_subject) -> None:
        """Test the constructor."""
        assert new_subject.subject_id == "MATH"
        assert new_subject.name == "Mathematics"


@dbtest
class TestSubjectDB:
    """Test the Subject class with a database session."""

    def test_get_subject(self, session: Session) -> None:
        """Test getting a subject from the db."""
        subject = session.get(Subject, "COMP")
        assert len(subject.courses) == 1

    def test_add_subject(self, new_subject, session: Session) -> None:
        """Test adding a subject to the db."""
        session.add(new_subject)
        session.commit()
        assert session.get(Subject, "MATH") == new_subject

    def test_update_subject(self, session: Session) -> None:
        """Test updating a subject in the db."""
        subject = session.get(Subject, "COMP")
        subject.name = "Comp Sci"
        session.commit()
        assert session.get(Subject, "COMP").name == "Comp Sci"

    def test_delete_subject(self, session: Session) -> None:
        """Test deleting a subject from the db."""
        subject = session.get(Subject, "COMP")
        session.delete(subject)
        session.commit()
        assert session.get(Subject, "COMP") is None
        assert session.get(Course, 1) is None
        assert session.get(Offering, "12345") is None
