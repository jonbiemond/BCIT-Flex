"""Tests for the CourseFilter class and course query function."""
import pytest
from sqlalchemy import Select, select

from bcitflex.app_functions.course_query import ModelFilter, select_tables
from bcitflex.model import Course, Meeting, Offering, Program


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


class TestHelpers:
    """Test helper functions in the course_query module."""

    @pytest.mark.parametrize(
        "stmt, expected",
        [
            (select(Course), [Course]),
            (select(Course).join(Offering), [Course, Offering]),
            (select(Course).join(Offering).join(Meeting), [Course, Offering, Meeting]),
        ],
    )
    def test_from_tables(self, stmt: Select, expected):
        """Test that from_tables returns the correct tables."""
        expected = [model.__table__ for model in expected]
        assert select_tables(stmt) == expected


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

    @pytest.mark.parametrize(
        "condition",
        [
            Course.code,
            Course.code == Course.code,
        ],
    )
    def test_invalid_condition(self, course_filter: ModelFilter, condition):
        """Test that an invalid condition raises a ValueError."""
        with pytest.raises(ValueError):
            course_filter.where(condition)

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

    def test_add_associated_relationship_condition(
        self, course_filter: ModelFilter, base_stmt: str
    ):
        """Test adding a condition for an indirectly related table."""
        base_stmt += " JOIN offering ON course.course_id = offering.course_id"
        base_stmt += " JOIN meeting ON offering.offering_id = meeting.offering_id"
        base_stmt += " WHERE meeting.campus = :campus_1"
        course_filter.where(Meeting.campus == "Burnaby", [Offering])
        assert one_line(course_filter.stmt) == base_stmt

    def test_multi_condition_and_associated_relationship_condition(
        self, course_filter: ModelFilter, base_stmt: str
    ):
        """Test adding a condition for an indirectly related table when it is already referenced in another condition."""
        base_stmt += " JOIN offering ON course.course_id = offering.course_id"
        base_stmt += " JOIN meeting ON offering.offering_id = meeting.offering_id"
        base_stmt += " WHERE offering.status = :status_1"
        base_stmt += " AND meeting.campus = :campus_1"
        course_filter.where(Offering.status == "Full")
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

    def test_association_table(self, course_filter: ModelFilter, base_stmt: str):
        """Test that the association table is used when filtering by a many-to-many relationship."""
        base_stmt += " JOIN program_course_association AS program_course_association_1 ON course.course_id = program_course_association_1.course_id"
        base_stmt += " JOIN program ON program.program_id = program_course_association_1.program_id"
        base_stmt += " WHERE program.program_id = :program_id_1"
        course_filter.where(Program.program_id == 1, [Course.programs])
        assert one_line(course_filter.stmt) == base_stmt
