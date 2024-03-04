"""Tests for the course model."""
import datetime

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bcitflex.model import Course, Offering
from bcitflex.model.prerequisite import PrerequisiteAnd, PrerequisiteOr
from tests import dbtest


@pytest.fixture
def new_course(
    new_offering: Offering,
    new_course: Course,
    new_prereq_and: PrerequisiteAnd,
    new_prereq_or: PrerequisiteOr,
) -> Course:
    """Return a new course object."""
    new_offering.course_id = 2
    new_course.offerings = [new_offering]
    new_prereq_and.children = [new_prereq_or]
    new_course.prerequisites = [new_prereq_and]
    return new_course


class TestCourse:
    """Test the Course class."""

    def test_init(self, new_course: Course, new_offering: Offering):
        """Test the constructor."""
        assert new_course.course_id is None
        assert new_course.subject_id == 1
        assert new_course.code == "5678"
        assert new_course.name == "Test Course"
        assert new_course.prerequisites_raw == "COMP 1000"
        assert new_course.credits == 3.0
        assert new_course.url == "https://www.bcit.ca"
        assert new_course.offerings == [new_offering]

    def test_str(self, new_course: Course):
        """Test the string representation"""
        assert (
            str(new_course) == "Subject: None\n"
            "Code: 5678\n"
            "Name: Test Course\n"
            "Prerequisites: COMP 1000\n"
            "Credits: 3.0\n"
            "URL: https://www.bcit.ca\n"
        )

    def test_offering_count(self, new_course: Course, new_offering: Offering):
        """Test offering_count method."""
        full_offering = new_offering.clone(
            crn="54321", status="Full", include_relationships=False
        )
        new_course.offerings.append(full_offering)
        assert new_course.offering_count() == 2
        assert new_course.offering_count(available_only=True) == 1

    def test_is_available(self, new_course: Course):
        """Test is_available method."""
        assert new_course.is_available

    def test_to_string(self, new_course: Course):
        """Lazy test for to_string method."""
        assert len(new_course.to_string()) > 50

    def test_last_updated(self, new_course: Course):
        """Test last_updated property."""
        new_course.updated_at = datetime.datetime(
            2011, 6, 29, 16, 52, 48, tzinfo=datetime.timezone.utc
        )
        updated_at = new_course.updated_at
        assert (
            updated_at.tzinfo is not None
            and updated_at.tzinfo.utcoffset(updated_at) is not None
        )
        assert new_course.last_updated == "2011-06-29T16:52:48+00:00"


@dbtest
class TestCourseDB:
    """Test the Course class with a database session."""

    def test_get_course(self, db_session: Session):
        """Test getting a course from the db."""
        course = db_session.get(Course, 1)
        assert course.subject.code == "COMP"

    def test_add_course(self, new_course: Course, db_session: Session):
        """Test adding a course to the db."""
        max_id = db_session.scalar(text("SELECT MAX(course_id) FROM course"))
        db_session.add(new_course)
        db_session.commit()
        assert db_session.get(Course, max_id + 1) == new_course

    def test_update_course(self, db_session: Session):
        """Test updating a course in the db."""
        course = db_session.get(Course, 1)
        course.name = "New Name"
        db_session.commit()
        assert db_session.get(Course, 1).name == "New Name"

    def test_unique_constraint(self, db_session: Session):
        """Test unique constraint on subject_id and code."""
        new_course = db_session.get(Course, 1).clone(
            course_id=None, include_relationships=False
        )
        db_session.add(new_course)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_merge(self, db_session: Session):
        """Test merge doesn't create a new object when code and subject_id already exist."""
        course_ct = len(db_session.scalars(select(Course)).all())
        new_course = db_session.get(Course, 1).clone(
            pk_id=None, include_relationships=False
        )
        new_course.set_id(db_session)
        db_session.merge(new_course)
        db_session.commit()
        assert len(db_session.scalars(select(Course)).all()) == course_ct

    def test_delete_course_cascade(self, db_session: Session):
        course = db_session.get(Course, 1)
        db_session.delete(course)
        db_session.commit()
        assert db_session.get(Offering, "12345") is None
