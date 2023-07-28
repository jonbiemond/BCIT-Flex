"""Tests for the offering model."""
import pytest

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
