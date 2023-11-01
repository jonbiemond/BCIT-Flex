"""Tests for the CourseFilter class and course query function."""
import pytest

from bcitflex.app_functions.course_query import ModelFilter, coerce_to_column_type
from bcitflex.model import Course, Offering, Subject
from bcitflex.model.enum import Match


@pytest.fixture(scope="function")
def course_filter():
    """Return a ModelFilter instance."""
    return ModelFilter(Course)


@pytest.fixture
def courses():
    """Return a list of Course instances."""
    return [
        Course(code="1234", name="Test Course", subject=Subject(subject_id="COMP")),
        Course(
            code="5678",
            subject=Subject(subject_id="COMP"),
            name="Second Course",
            offerings=[Offering(term_id="202101")],
        ),
    ]


class TestHelperFunctions:
    """Test the helper functions of course_query.py."""

    @pytest.mark.parametrize(
        "model_column, value, expected",
        [
            (Course.code, 1234, "1234"),
            (Course.code, "1234", "1234"),
        ],
    )
    def test_coerce_to_column_type(self, model_column, value, expected):
        """Test the coerce_to_column_type function."""
        coerced_value = coerce_to_column_type(model_column, value)
        assert isinstance(coerced_value, str)
        assert coerced_value == expected


class TestModelFilter:
    """Test the ModelFilter class."""

    def test_add_condition(self, course_filter: ModelFilter):
        """Test that the add_condition method adds a condition."""
        course_filter.add_condition("code", "1234")
        assert len(course_filter.conditions) == 1

    def test_add_condition_none(self, course_filter: ModelFilter):
        """Test that add_condition does not add a condition if the value is None."""
        course_filter.add_condition("code", None)
        assert len(course_filter.conditions) == 0

    def test_add_condition_blank(self, course_filter: ModelFilter):
        """Test that add_condition does not add a condition if the value is blank."""
        course_filter.add_condition("code", "")
        assert len(course_filter.conditions) == 0

    def test_add_rel_condition(self, course_filter: ModelFilter):
        """Test the add_condition method with a relationship."""
        course_filter.add_condition("subject_id", "COMP", Subject)
        assert len(course_filter.conditions) == 1

    def test_filter(self, course_filter: ModelFilter, courses):
        """Test the filter method."""
        course_filter.add_condition("code", "1234")
        filtered_courses = course_filter.filter(courses)
        assert len(filtered_courses) == 1
        assert filtered_courses[0].code == "1234"

    def test_filter_rel(self, course_filter: ModelFilter, courses):
        """Test the filter method with a relationship."""
        course_filter.add_condition("subject_id", "COMP", Subject)
        filtered_courses = course_filter.filter(courses)
        assert len(filtered_courses) == 2
        assert filtered_courses[0].subject.subject_id == "COMP"

    def test_filter_rel_collection(self, course_filter: ModelFilter, courses):
        """Test the filter method with a relationship."""
        course_filter.add_condition("term_id", "202101", Offering)
        filtered_courses = course_filter.filter(courses)
        assert len(filtered_courses) == 1
        assert filtered_courses[0].offerings[0].term_id == "202101"

    def test_filter_name_course(self, course_filter: ModelFilter, courses):
        """Test the filter method with a relationship."""
        course_filter.add_condition("name", "Test Course")
        filtered_courses = course_filter.filter(courses)
        assert len(filtered_courses) == 1
        assert filtered_courses[0].name == "Test Course"

    def test_filter_exact_match(self, course_filter: ModelFilter, courses):
        """Test the filter method with a relationship."""
        course_filter.add_condition("name", "cours")
        filtered_courses = course_filter.filter(courses)
        assert len(filtered_courses) == 0

    def test_filter_partial_match(self, course_filter: ModelFilter, courses):
        """Test the filter method with a relationship."""
        course_filter.add_condition("name", "cours", None, Match.PARTIAL)
        filtered_courses = course_filter.filter(courses)
        assert len(filtered_courses) == 2
        assert list(map(lambda x: x.name, filtered_courses)) == [
            "Test Course",
            "Second Course",
        ]
