"""Tests for the course model."""
import pytest
from sqlalchemy.orm import Session

from bcitflex.model import Course, Offering
from tests import dbtest


@pytest.fixture
def new_course(new_offering: Offering, new_course: Course) -> Course:
    """Return a new course object."""
    new_offering.course_id = 2
    new_course.offerings = [new_offering]
    return new_course


class TestCourse:
    """Test the Course class."""

    def test_init(self, new_course: Course, new_offering: Offering):
        """Test the constructor."""
        assert new_course.course_id is None
        assert new_course.subject_id == "COMP"
        assert new_course.code == "1234"
        assert new_course.name == "Test Course"
        assert new_course.prerequisites == "COMP 1000"
        assert new_course.credits == 3.0
        assert new_course.url == "https://www.bcit.ca"
        assert new_course.offerings == [new_offering]

    def test_str(self, new_course: Course):
        """Test the string representation"""
        assert (
            str(new_course) == "Course: COMP 1234\n"
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


@dbtest
class TestCourseDB:
    """Test the Course class with a database session."""

    def test_get_course(self, session: Session):
        """Test getting a course from the db."""
        course = session.get(Course, 1)
        assert course.subject.subject_id == "COMP"

    def test_add_course(self, new_course: Course, session: Session):
        """Test adding a course to the db."""
        session.add(new_course)
        session.commit()
        assert session.get(Course, 2) == new_course

    def test_update_course(self, session: Session):
        """Test updating a course in the db."""
        course = session.get(Course, 1)
        course.name = "New Name"
        session.commit()
        assert session.get(Course, 1).name == "New Name"

    def test_delete_course_cascade(self, session: Session):
        course = session.get(Course, 1)
        session.delete(course)
        session.commit()
        assert session.get(Offering, "12345") is None
