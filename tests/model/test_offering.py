"""Tests for the offering model."""
import pytest
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

from bcitflex.model import Offering


@pytest.fixture
def offering() -> Offering:
    """Return a test offering."""
    return Offering(
        crn=12345,
        instructor="John Doe",
        price=123.45,
        duration="1 week",
        status="Open",
    )


class TestOffering:
    """Test the Offering class."""

    def test_init(self, offering: Offering) -> None:
        """Test the constructor."""
        assert offering.crn == 12345
        assert offering.instructor == "John Doe"
        assert offering.price == 123.45
        assert offering.duration == "1 week"
        assert offering.status == "Open"

    def test_str(self, offering: Offering) -> None:
        """Test the string representation."""
        assert (
            str(offering) == "CRN: 12345\n"
            " Instructor: John Doe\n"
            " Price: 123.45\n"
            " Duration: 1 week\n"
            " Status: Open\n"
        )

    def test_add_offering(self, offering: Offering, session: Session) -> None:
        """Test adding an offering to the db."""
        session.add(offering)
        session.commit()
        assert session.get(Offering, 12345) == offering

    def test_update_offering(self, session) -> None:
        """Test updating an offering in the db."""
        offering = session.get(Offering, 12345)
        offering.instructor = "Jane Doe"
        session.commit()
        assert session.get(Offering, 12345).instructor == "Jane Doe"

    def test_invalid_crn(self, offering: Offering, session: Session) -> None:
        """Test that adding an offering with an invalid value raises an exception."""
        offering.crn = "abc"
        with pytest.raises(DataError):
            try:
                session.add(offering)
                session.commit()
            except DataError as e:
                session.rollback()
                raise e
