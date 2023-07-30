"""Tests for the course model."""
import pytest
from sqlalchemy.orm import Session

from bcitflex.model import Course, Offering


@pytest.fixture
def course(offering) -> Course:
    """Return a test course."""
    return Course(
        course_id=1,
        subject_id="COMP",
        code="1234",
        name="Test Course",
        prerequisites="COMP 1000",
        credits=3.0,
        url="https://www.bcit.ca",
        offerings=[offering],
    )


class TestCourse:
    """Test the Course class."""

    def test_init(self, course: Course, offering: Offering) -> None:
        """Test the constructor."""
        assert course.course_id == 1
        assert course.subject_id == "COMP"
        assert course.code == "1234"
        assert course.name == "Test Course"
        assert course.prerequisites == "COMP 1000"
        assert course.credits == 3.0
        assert course.url == "https://www.bcit.ca"
        assert course.offerings == [offering]


class TestCourseDB:
    """Test the Course class with a database session."""

    def test_add_course(self, course: Course, session: Session) -> None:
        """Test adding a course to the db."""
        session.add(course)
        session.commit()
        assert session.get(Course, 1) == course

    def test_update_course(self, course: Course, session: Session) -> None:
        """Test updating a course in the db."""
        course = session.get(Course, 1)
        course.name = "New Name"
        session.commit()
        assert session.get(Course, 1).name == "New Name"
