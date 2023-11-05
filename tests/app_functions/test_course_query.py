"""Tests for the CourseFilter class and course query function."""
import pytest
from sqlalchemy import Select, select

from bcitflex.app_functions.course_query import ModelFilter
from bcitflex.model import Course, Meeting, Offering


def one_line(stmt: Select) -> str:
    """Transform statement to one line string."""
    return str(stmt).replace("\n", "")


@pytest.fixture(scope="function")
def course_filter():
    """Return a ModelFilter instance."""
    return ModelFilter(Course)


@pytest.fixture(scope="function")
def base_stmt(course_filter):
    """Return the base ModelFilter statement."""
    return one_line(select(Course).distinct())


class TestModelFilter:
    """Test the ModelFilter class."""

    def test_init(self, course_filter: ModelFilter, base_stmt: str):
        """Test select statement initialization."""
        assert one_line(course_filter.stmt) == base_stmt

    def test_add_condition(self, course_filter: ModelFilter, base_stmt: str):
        """Test that the condition method adds a where clause."""
        base_stmt += " WHERE course.code = :code_1"
        course_filter.where(Course.code == "1234")
        assert one_line(course_filter.stmt) == base_stmt

    def test_add_condition_none(self, course_filter: ModelFilter, base_stmt: str):
        """Test that condition does not add a clause if the value is None."""
        course_filter.where(Course.code.is_(None))
        assert one_line(course_filter.stmt) == base_stmt

    def test_add_condition_blank(self, course_filter: ModelFilter, base_stmt: str):
        """Test that add_condition does not add a condition if the value is blank."""
        course_filter.where(Course.code == "")
        assert one_line(course_filter.stmt) == base_stmt

    def test_add_multi_condition(self, course_filter: ModelFilter, base_stmt: str):
        """Test adding multiple conditions."""
        base_stmt += " WHERE course.code = :code_1"
        base_stmt += " AND course.subject_id = :subject_id_1"
        course_filter.where(Course.code == "1234")
        course_filter.where(Course.subject_id == "COMP")
        assert one_line(course_filter.stmt) == base_stmt

    def test_add_rel_condition(self, course_filter: ModelFilter, base_stmt: str):
        """Test adding condition for related table."""
        base_stmt += " JOIN offering ON course.course_id = offering.course_id"
        base_stmt += " WHERE offering.status = :status_1"
        course_filter.where(Offering.status == "Full")
        assert one_line(course_filter.stmt) == base_stmt

    def test_add_distant_rel_condition(
        self, course_filter: ModelFilter, base_stmt: str
    ):
        """Test adding a condition for an indirectly related table."""
        base_stmt += " JOIN offering ON course.course_id = offering.course_id"
        base_stmt += " JOIN meeting ON offering.offering_id = meeting.offering_id"
        base_stmt += " WHERE meeting.campus = :campus_1"
        course_filter.where(Meeting.campus == "Burnaby", [Offering])
        assert one_line(course_filter.stmt) == base_stmt

    def test_add_condition_collection(self, course_filter: ModelFilter, base_stmt: str):
        """Test adding a condition with an IN operator."""
        base_stmt += " JOIN offering ON course.course_id = offering.course_id"
        base_stmt += " WHERE offering.status IN (__[POSTCOMPILE_status_1])"
        course_filter.where(Offering.status.in_(["Full", "Cancelled"]))
        assert one_line(course_filter.stmt) == base_stmt

    def test_filter_partial_match(self, course_filter: ModelFilter, base_stmt: str):
        """Test the filter method with a relationship."""
        base_stmt += " WHERE lower(course.name) LIKE lower(:name_1)"
        course_filter.where(Course.name.ilike("%cours%"))
        assert one_line(course_filter.stmt) == base_stmt
