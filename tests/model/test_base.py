"""Tests for the model Base class"""
import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from bcitflex.model import Course, Meeting, Offering, User
from bcitflex.model.base import db_to_attr, updated_pks
from tests import dbtest


class TestHelpers:
    """Test helper functions."""

    def test_db_to_attr(self):
        """Test the db_to_attr function."""
        cls_mapper = inspect(Course)
        assert db_to_attr(cls_mapper, "course_id") == "course_id"

    @pytest.mark.parametrize(
        "pk_val",
        [
            {"crn": 12345},
            {"crn": None},
        ],
    )
    def test_get_pks_single(self, pk_val):
        """Test the updated_pks function with a single pk."""
        obj = Offering(crn=12345)
        assert updated_pks(obj, pk_val) == {"crn": 12345}

    @pytest.mark.parametrize(
        "pk_val, expected",
        [
            ({"meeting_id": 15}, {"meeting_id": 15, "crn": 12345}),
            ({"crn": 54321}, {"meeting_id": 1, "crn": 54321}),
            ({"meeting_id": 15, "crn": 54321}, {"meeting_id": 15, "crn": 54321}),
            ({"meeting_id": None, "crn": 54321}, {"meeting_id": None, "crn": 54321}),
        ],
    )
    def test_get_pks_multiple(self, pk_val, expected):
        """Test the updated_pks function with multiple pks."""
        obj = Meeting(meeting_id=1, crn=12345)
        assert updated_pks(obj, pk_val) == expected

    @pytest.mark.parametrize(
        "pk_val, expected",
        [
            ({"course_id": None}, {"course_id": None}),
            ({"course_id": 15}, {"course_id": 15}),
        ],
    )
    def test_update_pks_default(self, pk_val, expected):
        """Test the update_pks function when there are default values."""
        obj = Course(subject_id="COMP", code="1001", name="Test Course")
        assert updated_pks(obj, pk_val) == expected


@dbtest
class TestGet:
    """Test the get functions."""

    def test_get_by_unique(self, session: Session):
        """Test the get_by_unique method."""
        product_type = User.get_by_unique(session, "test-user")
        assert product_type.username == "test-user"

    def test_get_by_unique_none(self, session: Session):
        """Test the get_by_unique method returns None when no results are found."""
        product_type = User.get_by_unique(session, "not_a_username")
        assert product_type is None

    def test_get_by_unique_no_unique_error(self, session: Session):
        """Test the get_by_unique method when no unique constraint is defined."""
        with pytest.raises(ValueError):
            Offering.get_by_unique(session, "unique")


@dbtest
class TestClone:
    """Test the clone method."""

    def test_clone_offering(self, session: Session, offering: Offering) -> None:
        """Test cloning an offering."""
        clone = offering.clone(pk_id="23498", instructor="Jane Doe", price=543.21)
        session.add(clone)
        session.commit()
        assert clone.crn != offering.crn
        assert clone.course_id == offering.course_id
        assert len(clone.meetings) == len(offering.meetings)

    def test_clone_without_relationships(
        self, session: Session, course: Course
    ) -> None:
        """Test cloning a course without relationships."""
        clone = course.clone(pk_id=2, include_relationships=False)
        session.add(clone)
        session.commit()
        assert clone.course_id != course.course_id
        assert clone.subject_id == course.subject_id

    def test_clone_missing_pk_id(self, session: Session, offering: Offering) -> None:
        """Test clone without passing a new pk_id."""
        clone = offering.clone(instructor="Jane Doe", price=543.21)
        assert clone.crn == offering.crn
        assert clone.course_id == offering.course_id
        assert len(clone.meetings) == len(offering.meetings)
