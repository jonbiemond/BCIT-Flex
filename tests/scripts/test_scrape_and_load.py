"""Test extracting course data from the BCIT website."""
from pickle import load

import pytest
import requests
from selectolax.parser import Node
from sqlalchemy import select
from sqlalchemy.orm import Session

from bcitflex.model import Course, Offering, Subject, Term
from bcitflex.scripts.scrape_and_load import (
    CoursePage,
    bcit_to_sql,
    extract_models,
    get_course_urls,
    load_models,
    offering_nodes,
    parse_course_info,
    parse_offering_node,
    parse_term_node,
    prep_db,
    scrape_course_urls,
    term_nodes,
)
from tests import dbtest
from tests.conftest import DB_URL


@pytest.fixture
def course_page() -> CoursePage:
    """Return a test course response."""
    return CoursePage(load(open("tests/test_data/course_response.pkl", "rb")))


@pytest.fixture
def term_node(course_page: CoursePage) -> Node:
    """Return a term node."""
    return course_page.html.css_first('div[id="offerings"] div[class="sctn"]')


@pytest.fixture
def offering_node(term_node: Node) -> Node:
    """Return a test offering node."""
    return term_node.css_first('div[class="sctn"]')


@pytest.fixture
def new_course(
    new_course: Course, new_subject: Subject, new_offering: Offering, new_term: Term
) -> Course:
    """Return a new course object."""
    new_offering.course_id = 2
    new_offering.term = new_term
    new_course.subject_id = "MATH"
    new_course.subject = new_subject
    new_course.offerings = [new_offering]
    return new_course


def test_term_nodes(course_page: CoursePage) -> None:
    """Test the term nodes function returns a valid term node."""
    term_node = next(term_nodes(course_page))
    assert term_node.parent.id == "202330"


def test_offering_nodes(term_node: Node) -> None:
    """Test the offering nodes function returns a valid offering_node"""
    node = next(offering_nodes(term_node))
    crn = node.css_first('li[class="sctn-block-list-item crn"] span').text(False)
    assert crn == "38186"


def test_parse_offering_node(
    offering_node: Node, new_course: Course, new_term: Term
) -> None:
    """Test the parse offering node function."""
    offering = parse_offering_node(offering_node, new_course, new_term)
    assert offering.price > 0
    assert offering.crn == "38186"


def test_parse_course_info(course_page: CoursePage) -> None:
    """Test the parse course function."""
    course = parse_course_info(course_page)
    assert course.credits > 0


def test_parse_term_node(term_node: Node) -> None:
    term = parse_term_node(term_node)
    assert term.term_id == "202330"


@dbtest
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


@dbtest
def test_get_course_urls(mocker, course_page: CoursePage, session: Session) -> None:
    """Test getting list of course urls."""

    # patch scrape_course_urls to return one url
    mocker.patch(
        "bcitflex.scripts.scrape_and_load.scrape_course_urls",
        return_value={"COMP": [course_page.url]},
    )

    urls = get_course_urls(session)
    assert len(urls) == 1
    assert urls[0] == course_page.url


def test_extract(monkeypatch, course_page: CoursePage) -> None:
    """Test extracting courses."""

    # mock request.get() to return response from test
    def mock_request(*args, **kwargs):
        return load(open("tests/test_data/course_response.pkl", "rb"))

    monkeypatch.setattr(requests, "get", mock_request)

    course = next(extract_models([course_page.url]))

    assert course.subject_id == "COMP"


@dbtest
def test_load_models(empty_session: Session, new_course: Course) -> None:
    """Test loading models to the db."""
    courses = (course for course in [new_course])
    assert empty_session.get(Course, 2) is None
    load_models(empty_session, courses)
    assert empty_session.get(Course, 2).course_id == 2


@dbtest
def test_bcit_to_sql(
    mocker, course_page: CoursePage, new_course: Course, empty_session: Session
) -> None:
    """Test adding data to the db."""

    # mock get_course_urls
    mocker.patch(
        "bcitflex.scripts.scrape_and_load.get_course_urls",
        return_value=[course_page.url],
    )

    # mock extract
    mocker.patch(
        "bcitflex.scripts.scrape_and_load.extract_models", return_value=[new_course]
    )

    bcit_to_sql(DB_URL)
    courses = empty_session.scalars(
        select(Course).where(Course.subject_id == "MATH")
    ).all()
    offerings = empty_session.scalars(select(Offering)).all()

    assert len(courses) == 1
    assert courses[0].subject_id == "MATH"
    assert offerings[0].price > 0


@dbtest
def test_bcit_to_sql_rollback(mocker, session: Session) -> None:
    # mock exception
    mocker.patch(
        "bcitflex.scripts.scrape_and_load.get_course_urls",
        side_effect=ArithmeticError,
    )

    with pytest.raises(ArithmeticError):
        bcit_to_sql(DB_URL)

    assert len(session.scalars(select(Offering)).all()) == 1
    assert len(session.scalars(select(Course)).all()) == 1
