"""Tests for the model Base class"""
import pytest
from sqlalchemy.orm import Session

from bcitflex.model import Course, Offering
from tests import dbtest


@dbtest
class TestBase:
    def test_clone_error(self, session: Session, course: Course) -> None:
        """Test cloning a course raises an error."""
        with pytest.raises(ValueError):
            course.clone(code="4321")

    def test_clone_offering(self, session: Session, offering: Offering) -> None:
        """Test cloning an offering."""
        clone = offering.clone(pk_id="23498", instructor="Jane Doe", price=543.21)
        session.add(clone)
        session.commit()
        assert clone.crn != offering.crn
        assert clone.course_id == offering.course_id

    def test_clone_without_relationships(
        self, session: Session, course: Course
    ) -> None:
        """Test cloning a course without relationships."""
        clone = course.clone(pk_id="4321", include_relationships=False)
        session.add(clone)
        session.commit()
        assert clone.course_id != course.course_id
        assert clone.subject_id == course.subject_id
