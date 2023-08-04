"""Test extracting course data from the BCIT website."""
from pickle import load

import pytest
import requests
from selectolax.parser import Node
from sqlalchemy import select
from sqlalchemy.orm import Session

from bcitflex.model import Course, Offering, Subject
from bcitflex.modules.extract_course_data import (
    CoursePage,
    bcit_to_sql,
    extract_models,
    get_course_urls,
    load_models,
    parse_course_info,
    parse_offering_node,
    prep_db,
    scrape_course_urls,
)
from tests.conftest import DB_URL


@pytest.fixture
def course_page() -> CoursePage:
    """Return a test course response."""
    return CoursePage(load(open("tests/test_data/course_response.pkl", "rb")))


@pytest.fixture
def offering_node(course_page: CoursePage) -> Node:
    """Return a test offering node."""
    return course_page.html.css_first(f'div[id="{course_page.term}"] div[class="sctn"]')


@pytest.fixture
def new_subject() -> Subject:
    """Return a new subject object."""
    return Subject(subject_id="MATH", name="Mathematics")


@pytest.fixture
def new_offering() -> Offering:
    """Return a new offering object."""
    return Offering(
        crn=67890,
        instructor="John Doe",
        price=123.45,
        duration="1 week",
        status="Open",
        course_id=2,
    )


@pytest.fixture
def new_course(new_subject: Subject, new_offering: Offering) -> Course:
    """Return a new course object."""
    return Course(
        course_id=2,
        subject_id="MATH",
        code="1234",
        name="Test Course",
        prerequisites="MATH 1000",
        credits=3.0,
        url="https://www.bcit.ca",
        subject=new_subject,
        offerings=[new_offering],
    )


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


def test_get_course_urls(mocker, course_page: CoursePage, session: Session) -> None:
    """Test getting list of course urls."""

    # patch scrape_course_urls to return one url
    mocker.patch(
        "bcitflex.modules.extract_course_data.scrape_course_urls",
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

    course = extract_models([course_page.url])[0]

    assert course.subject_id == "COMP"


def test_load_models(empty_session: Session, new_course: Course) -> None:
    """Test loading models to the db."""
    # TODO: replace session with session for empty db
    assert empty_session.get(Course, 2) is None
    load_models(empty_session, [new_course])
    assert empty_session.get(Course, 2).course_id == 2


def test_bcit_to_sql(
    mocker, course_page: CoursePage, new_course: Course, empty_session: Session
) -> None:
    """Test adding data to the db."""

    # mock get_course_urls
    mocker.patch(
        "bcitflex.modules.extract_course_data.get_course_urls",
        return_value=[course_page.url],
    )

    # mock extract
    mocker.patch(
        "bcitflex.modules.extract_course_data.extract_models", return_value=[new_course]
    )

    bcit_to_sql(DB_URL)
    courses = empty_session.scalars(
        select(Course).where(Course.subject_id == "MATH")
    ).all()
    offerings = empty_session.scalars(select(Offering)).all()

    assert len(courses) == 1
    assert courses[0].subject_id == "MATH"
    assert offerings[0].price > 0


def test_bcit_to_sql_rollback(mocker, session: Session) -> None:
    # mock exception
    mocker.patch(
        "bcitflex.modules.extract_course_data.get_course_urls",
        side_effect=ArithmeticError,
    )

    with pytest.raises(ArithmeticError):
        bcit_to_sql(DB_URL)

    assert len(session.scalars(select(Offering)).all()) == 1
    assert len(session.scalars(select(Course)).all()) == 1
