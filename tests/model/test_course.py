"""Tests for the course model."""
import pytest
from sqlalchemy.orm import Session

from bcitflex.model import Course


@pytest.fixture
def new_course(new_offering) -> Course:
    """Return a new course object."""
    return Course(
        course_id=2,
        subject_id="COMP",
        code="1234",
        name="Test Course",
        prerequisites="COMP 1000",
        credits=3.0,
        url="https://www.bcit.ca",
        offerings=[new_offering],
    )


class TestCourse:
    """Test the Course class."""

    def test_init(self, new_course: Course, new_offering) -> None:
        """Test the constructor."""
        assert new_course.course_id == 2
        assert new_course.subject_id == "COMP"
        assert new_course.code == "1234"
        assert new_course.name == "Test Course"
        assert new_course.prerequisites == "COMP 1000"
        assert new_course.credits == 3.0
        assert new_course.url == "https://www.bcit.ca"
        assert new_course.offerings == [new_offering]


class TestCourseDB:
    """Test the Course class with a database session."""

    def test_add_course(self, new_course: Course, session: Session) -> None:
        """Test adding a course to the db."""
        session.add(new_course)
        session.commit()
        assert session.get(Course, 2) == new_course

    def test_update_course(self, session: Session) -> None:
        """Test updating a course in the db."""
        course = session.get(Course, 1)
        course.name = "New Name"
        session.commit()
        assert session.get(Course, 1).name == "New Name"
