"""Test extracting course data from the BCIT website."""
import datetime
import re
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
    collect_response,
    extract_models,
    get_course_urls,
    load_courses,
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
def session(db_session) -> Session:
    """Return a new session for each function."""
    return db_session


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
def existing_course(
    new_course: Course, new_subject: Subject, new_offering: Offering, new_term: Term
) -> Course:
    """Return a course object that matches an existing row in the course table."""
    new_course.code = "1234"
    new_course.subject_id = "COMP"
    new_course.offerings = [new_offering]
    return new_course


class TestGetNodes:
    def test_term_nodes(self, course_page: CoursePage):
        """Test the term nodes function returns a valid term node."""
        term_node = next(term_nodes(course_page))
        # Example id: 202330
        assert re.match(r"^\d{6}$", term_node.parent.id)

    def test_offering_nodes(self, term_node: Node):
        """Test the offering nodes function returns a valid offering_node."""
        node = next(offering_nodes(term_node))
        crn = node.css_first('li[class="sctn-block-list-item crn"] span').text(False)
        # Example crn: 38185
        assert re.match(r"^\d{5}$", crn)

    def test_meeting_nodes(self, offering_node: Node):
        """Test the meeting nodes function returns a valid meeting node."""
        node = next(meeting_nodes(offering_node))
        assert len(node.text()) > 0


class TestParseNodes:
    def test_parse_term_node(self, term_node: Node):
        term = parse_term_node(term_node)
        assert re.match(r"^\d{6}$", term.term_id)

    def test_parse_course_info(self, course_page: CoursePage):
        """Test the parse course function."""
        course = parse_course_info(course_page)
        assert course.deleted_at is None
        assert course.credits > 0

    def test_parse_offering_node(
        self, offering_node: Node, existing_course: Course, new_term: Term
    ):
        """Test the parse offering node function."""
        offering = parse_offering_node(offering_node, existing_course, new_term)
        assert offering.deleted_at is None
        assert offering.price > 0
        assert re.match(r"^\d{5}$", offering.crn)

    def test_parse_meeting_node(
        self, meeting_node: Node, new_offering: Offering, new_term: Term
    ):
        """Test the parse meeting node function."""
        meeting = parse_meeting_node(meeting_node, new_offering, new_term)
        assert meeting.deleted_at is None
        assert isinstance(meeting.start_date, datetime.date)
        assert isinstance(meeting.end_date, datetime.date)
        assert meeting.days is None or len(meeting.days) > 0
        assert meeting.start_time is None or isinstance(
            meeting.start_time, datetime.time
        )
        assert meeting.end_time is None or isinstance(meeting.end_time, datetime.time)
        assert isinstance(meeting.campus, str)
        assert meeting.room is None or isinstance(meeting.room, str)


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
        """Test if prep_db does not delete data in the database."""
        populate_db(session)

        offerings = session.scalars(select(Offering)).all()
        assert len(offerings) == 1

        prep_db(session)

        offerings = session.scalars(select(Offering)).all()
        assert len(offerings) == 1

        terms = session.scalars(select(Term)).all()
        assert len(terms) > 0

    def test_load_models(self, session: Session, existing_course: Course):
        """Test loading models to the db."""
        courses = (course for course in [existing_course])
        assert session.get(Course, 1) is not None
        load_courses(session, courses)
        assert session.get(Course, 4) is None

    def test_collect_response_failure(self, monkeypatch):
        mock_response = MagicMock()
        mock_response.status_code = 404
        monkeypatch.setattr("requests.get", MagicMock(return_value=mock_response))

        with pytest.raises(Exception) as exc_info:
            collect_response("https://example.com")
            assert "Collect response status code" in str(exc_info.value)
