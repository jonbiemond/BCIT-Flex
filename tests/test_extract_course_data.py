"""Test extracting course data from the BCIT website."""
from pickle import load

import pytest
import requests
from selectolax.parser import Node
from sqlalchemy import select
from sqlalchemy.orm import Session

from bcitflex.model import Course, Offering
from bcitflex.modules.extract_course_data import (
    CoursePage,
    parse_course_info,
    parse_offering_node,
    prep_db,
    scrape_course_urls,
)


@pytest.fixture
def course_page() -> CoursePage:
    """Return a test course response."""
    return CoursePage(load(open("tests/test_data/course_response.pkl", "rb")))


@pytest.fixture
def offering_node(course_page: CoursePage) -> Node:
    """Return a test offering node."""
    return course_page.html.css_first(f'div[id="{course_page.term}"] div[class="sctn"]')


def test_parse_offering_node(offering_node: Node, course: Course) -> None:
    """Test the parse offering node function."""
    offering = parse_offering_node(offering_node, course)
    assert offering.price > 0


def test_parse_course_info(course_page: CoursePage) -> None:
    """Test the parse course function."""
    course = parse_course_info(course_page)
    assert course.credits > 0


def test_prep_db(session: Session) -> None:
    """Test if prep_db deletes data in the database."""
    prep_db(session)
    offerings = session.scalars(select(Offering)).all()
    assert len(offerings) == 0


def test_scrape_course_urls(monkeypatch) -> None:
    """Test urls are scraped from mock response."""

    # mock request.get() to return response from test
    def mock_request(*args, **kwargs):
        return load(open("tests/test_data/course_list_response.pkl", "rb"))

    monkeypatch.setattr(requests, "get", mock_request)

    result = scrape_course_urls("https://www.bcit.ca")

    assert len(result["COMP"]) > 1
