"""Test extracting course data from the BCIT website."""
import datetime
from pickle import load
from unittest.mock import MagicMock

import pytest
import requests
from selectolax.parser import Node
from sqlalchemy import select
from sqlalchemy.orm import Session

from bcitflex.model import Course, Offering, Subject, Term
from bcitflex.scripts.scrape_and_load import (
    CoursePage,
    extract_models,
    get_course_urls,
    load_models,
    meeting_nodes,
    offering_nodes,
    parse_course_info,
    parse_meeting_node,
    parse_offering_node,
    parse_term_node,
    prep_db,
    scrape_course_urls,
    term_nodes,
)
from tests import dbtest
from tests.db_test_utils import populate_db


@pytest.fixture(scope="function")
def session(session) -> Session:
    """Return a new session for each function."""
    return session


@pytest.fixture
def course_page() -> CoursePage:
    """Return a test course response."""
    return CoursePage(load(open("tests/test_data/course_response.pkl", "rb")))


@pytest.fixture
def term_node(course_page: CoursePage) -> Node:
    """Return a term node."""
    return next(term_nodes(course_page))


@pytest.fixture
def offering_node(term_node: Node) -> Node:
    """Return a test offering node."""
    return next(offering_nodes(term_node))


@pytest.fixture
def meeting_node(offering_node: Node) -> Node:
    """Return a meeting time row."""
    return next(meeting_nodes(offering_node))


@pytest.fixture
def new_course(
    new_course: Course, new_subject: Subject, new_offering: Offering, new_term: Term
) -> Course:
    """Return a new course object."""
    new_offering.course_id = 2
    new_course.subject_id = "MATH"
    new_course.subject = new_subject
    new_course.offerings = [new_offering]
    return new_course


class TestGetNodes:
    def test_term_nodes(self, course_page: CoursePage):
        """Test the term nodes function returns a valid term node."""
        term_node = next(term_nodes(course_page))
        assert term_node.parent.id == "202330"

    def test_offering_nodes(self, term_node: Node):
        """Test the offering nodes function returns a valid offering_node."""
        node = next(offering_nodes(term_node))
        crn = node.css_first('li[class="sctn-block-list-item crn"] span').text(False)
        assert crn == "38186"

    def test_meeting_nodes(self, offering_node: Node):
        """Test the meeting nodes function returns a valid meeting node."""
        node = next(meeting_nodes(offering_node))
        assert len(node.text()) > 0


class TestParseNodes:
    def test_parse_term_node(self, term_node: Node):
        term = parse_term_node(term_node)
        assert term.term_id == "202330"

    def test_parse_course_info(self, course_page: CoursePage):
        """Test the parse course function."""
        course = parse_course_info(course_page)
        assert course.credits > 0

    def test_parse_offering_node(
        self, offering_node: Node, new_course: Course, new_term: Term
    ):
        """Test the parse offering node function."""
        offering = parse_offering_node(offering_node, new_course, new_term)
        assert offering.price > 0
        assert offering.crn == "38186"

    def test_parse_meeting_node(
        self, meeting_node: Node, new_offering: Offering, new_term: Term
    ):
        """Test the parse meeting node function."""
        meeting = parse_meeting_node(meeting_node, new_offering, new_term)
        assert meeting.start_date == datetime.date(2024, 9, 13)
        assert meeting.end_date == datetime.date(2024, 11, 29)
        assert meeting.days == {"Wed"}
        assert meeting.start_time == datetime.time(18)
        assert meeting.end_time == datetime.time(21)
        assert meeting.campus == "Online"
        assert meeting.room is None


class TestExtractModels:
    def test_scrape_course_urls(self, monkeypatch):
        """Test urls are scraped from mock response."""

        # mock request.get() to return response from test
        mock_request = MagicMock(
            return_value=load(open("tests/test_data/course_list_response.pkl", "rb"))
        )

        monkeypatch.setattr(requests, "get", mock_request)

        result = scrape_course_urls("https://www.bcit.ca")

        assert len(result["COMP"]) > 1

    @dbtest
    @pytest.mark.parametrize(
        "all_subjects, expected",
        [
            (True, ["comp_url", "ahvc_url"]),
            (False, ["comp_url"]),
        ],
    )
    def test_get_course_urls(
        self, mocker, course_page: CoursePage, session: Session, all_subjects, expected
    ):
        """Test getting list of course urls."""

        # patch scrape_course_urls to return one url
        mocker.patch(
            "bcitflex.scripts.scrape_and_load.scrape_course_urls",
            return_value={
                "COMP": ["comp_url"],
                "BLAW": ["blaw_url"],
                "AHVC": ["ahvc_url"],
            },
        )

        urls = get_course_urls(session, all_subjects)
        assert urls == expected

    def test_extract(self, monkeypatch, course_page: CoursePage):
        """Test extracting courses."""

        # mock request.get() to return response from test
        mock_request = MagicMock(
            return_value=load(open("tests/test_data/course_response.pkl", "rb"))
        )
        monkeypatch.setattr(requests, "get", mock_request)

        course = next(extract_models([course_page.url]))

        assert course.subject_id == "COMP"


@dbtest
class TestLoadData:
    pytestmark = pytest.mark.empty_db

    def test_prep_db(self, session: Session):
        """Test if prep_db deletes data in the database."""
        populate_db(session)

        offerings = session.scalars(select(Offering)).all()
        assert len(offerings) == 1

        prep_db(session)

        offerings = session.scalars(select(Offering)).all()
        assert len(offerings) == 0

        terms = session.scalars(select(Term)).all()
        assert len(terms) == 6

    def test_load_models(self, session: Session, new_course: Course):
        """Test loading models to the db."""
        courses = (course for course in [new_course])
        assert session.get(Course, 1) is None
        load_models(session, courses)
        assert session.get(Course, 2).course_id == 2
