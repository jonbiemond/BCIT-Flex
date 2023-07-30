"""Test extracting course data from the BCIT website."""
from pickle import load

import pytest
from selectolax.parser import Node

from bcitflex.modules.extract_course_data import (
    CoursePage,
    parse_course_info,
    parse_offering_node,
)


@pytest.fixture
def course_page() -> CoursePage:
    """Return a test course response."""
    return CoursePage(load(open("tests/test_data/course_response.pkl", "rb")))


@pytest.fixture
def offering_node(course_page) -> Node:
    """Return a test offering node."""
    return course_page.html.css_first(f'div[id="{course_page.term}"] div[class="sctn"]')


def test_parse_offering_node(offering_node: Node) -> None:
    """Test the parse offering node function."""
    offering = parse_offering_node(offering_node)
    assert offering.price > 0


def test_parse_course_info(course_page) -> None:
    """Test the parse course function."""
    course = parse_course_info(course_page)
    assert course.credits > 0
