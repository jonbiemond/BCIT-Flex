"""Test extracting course data from the BCIT website."""
from pickle import load

import pytest
from requests import Response
from selectolax.parser import HTMLParser, Node

from bcitflex.modules.extract_course_data import next_term, parse_offering_node


@pytest.fixture
def course_response() -> Response:
    """Return a test course response."""
    return load(open("tests/test_data/course_response.pkl", "rb"))


@pytest.fixture
def offering_node(course_response) -> Node:
    """Return a test offering node."""

    term = next_term(course_response)

    html = HTMLParser(course_response.text)
    return html.css_first(f'div[id="{term}"] div[class="sctn"]')


def test_parse_offering_node(offering_node: Node) -> None:
    """Test the parse offering node function."""

    offering = parse_offering_node(offering_node)
    assert offering.price > 0
