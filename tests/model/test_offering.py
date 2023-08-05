"""Tests for the offering model."""
import pytest
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

from bcitflex.model import Offering
from tests import dbtest


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


class TestOffering:
    """Test properties of the Offering class."""

    def test_init(self, new_offering: Offering) -> None:
        """Test the constructor."""
        assert new_offering.crn == "67890"
        assert new_offering.instructor == "John Doe"
        assert new_offering.price == 123.45
        assert new_offering.duration == "1 week"
        assert (
            new_offering.meeting_time
            == "Day   Time    Location\nWed    16:00 - 19:00 DTC"
        )
        assert new_offering.status == "Open"
        assert new_offering.course_id == 1
        assert new_offering.available is True

    def test_str(self, new_offering: Offering) -> None:
        """Test the string representation."""
        assert (
            str(new_offering) == "CRN: 67890\n"
            " Instructor: John Doe\n"
            " Price: 123.45\n"
            " Duration: 1 week\n"
            " Status: Open\n"
        )


@dbtest
class TestOfferingDB:
    """Test the Offering class with a database session."""

    def test_add_offering(self, new_offering: Offering, session: Session) -> None:
        """Test adding an offering to the db."""
        session.add(new_offering)
        session.commit()
        assert session.get(Offering, "67890") == new_offering
        assert session.get(Offering, "67890").course.course_id == 1

    def test_update_offering(self, session: Session) -> None:
        """Test updating an offering in the db."""
        offering = session.get(Offering, "12345")
        offering.instructor = "Jane Doe"
        session.commit()
        assert session.get(Offering, "12345").instructor == "Jane Doe"

    def test_invalid_crn(self, offering: Offering, session: Session) -> None:
        """Test that adding an offering with an invalid value raises an exception."""
        offering.crn = "abcdef"
        with pytest.raises(DataError):
            try:
                session.add(offering)
                session.commit()
            except DataError as e:
                session.rollback()
                raise e
