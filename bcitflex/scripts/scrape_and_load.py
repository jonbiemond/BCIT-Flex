"""Script to scrape course data and load it to the database. """
import datetime
import re
from collections import defaultdict
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

import click
import requests
from flask import current_app
from requests import Response
from selectolax.parser import HTMLParser, Node
from sqlalchemy import create_engine, or_, select
from sqlalchemy.orm import Session

from bcitflex.model import Course, Meeting, Offering, Subject, Term

TERMS = {10: "Winter", 20: "Spring/Summer", 30: "Fall"}
WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

BASE_URL = "https://www.bcit.ca"
COURSE_LIST = "/wp-json/bcit/ptscc/v1/list-active-urls"


class CoursePage:
    """HTML representation of a course page."""

    def __init__(self, response: Response) -> None:
        self.url: str = response.url
        self.tree: HTMLParser = HTMLParser(response.text)
        self.term: str = next_term(response)


def next_term(response: Response) -> str:
    """Get the next term from a course response."""

    html_parser = HTMLParser(response.text)

    for term in range(30, 0, -10):
        if html_parser.css_first(f'div[id="{date.today().year}{term}"]') is not None:
            return f"{date.today().year}{term}"


def read_rmp_ids(filename) -> dict[str, str]:
    """Read the RMP IDs from the file."""

    rmp_ids = {}
    with open(filename, "r") as file:
        for line in file:
            subject, rmp_id = line.split(",")
            rmp_ids[subject] = rmp_id.strip()

    return rmp_ids


def collect_response(url: str) -> Response:
    """Collect the response from the given URL and return the text."""

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Collect response status code: {response.status_code}")

    else:
        return response


def get_page_responses(urls: list[str]) -> list[Response]:
    """Get the responses from the given course URLs."""

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(collect_response, url) for url in urls]
        responses = [future.result() for future in as_completed(futures)]

    return responses


def parse_offering_node(node: Node, course: Course, term: Term) -> Offering:
    """Parse the offering node and return the offering."""

    # get crn
    crn = node.css_first('li[class="sctn-block-list-item crn"] span').text(False)

    # get instructor
    instructor_node = node.css_first('div[class="sctn-instructor"] p')

    if instructor_node is None:
        instructor = "Not Available"
    else:
        instructor = instructor_node.text(False)

    # get price
    price = node.css_first('li[class="sctn-block-list-item cost"]').text(False)
    price = float(price.removeprefix("$"))

    # get duration
    duration = node.css_first('li[class="sctn-block-list-item duration"]').text(False)

    # get status
    status_node = node.css_first('p[class="sctn-status-lbl"]')

    if status_node is None:
        status = "Available"

    else:
        status = status_node.text(False)

    # offering object
    offering = Offering(
        crn=crn,
        instructor=instructor,
        price=price,
        duration=duration,
        status=status,
        course=course,
        term_id=term.term_id,
    )

    # parse meeting times
    if node.css_first('div[class="sctn-no-meets"] p') is None:
        for meeting_node in meeting_nodes(node):
            parse_meeting_node(meeting_node, offering, term)

    return offering


def parse_meeting_node(node: Node, offering: Offering, term: Term) -> Meeting:
    """Parse the meeting node and return the meeting."""

    # columns: Dates, Days, Times, Locations
    elements = list(
        filter(
            None,
            [element.strip() for element in node.text().split("\n")],
        )
    )

    # parse dates
    dates = []
    for date_str in elements[0].split(" - "):
        try:
            date = datetime.datetime.strptime(date_str, "%b %d").date()
        except ValueError as err:
            raise ValueError(f"Invalid date format: {date_str}") from err

        date = date.replace(year=term.year)
        dates.append(date)

    start_date = dates[0]
    end_date = dates[-1]

    # parse days
    def parse_days(days_str: str) -> set[str] | None:
        if days_str == "N/A":
            return None

        days = set()
        meeting_days = days_str.split(" - ")
        if len(meeting_days) > 1:
            # Days: Mon - Fri
            start, stop = (WEEKDAYS.index(day) for day in meeting_days)
            meeting_days = WEEKDAYS[start : stop + 1]

        else:
            # Days: Mon, Wed, Fri
            meeting_days = days_str.split(", ")

        for day in meeting_days:
            days.add(day)

        return days

    days = parse_days(elements[1])

    # parse time
    times = []
    time_str = elements[2]

    if time_str == "N/A":
        times = [None, None]

    else:
        for time in time_str.split(" - "):
            times.append(datetime.datetime.strptime(time, "%H:%M").time())

    start_time = times[0]
    end_time = times[-1]

    # parse location
    location = elements[3].split(" ", maxsplit=2)
    campus = location.pop(0)
    building = location.pop(0) if location else None
    room = location[0] if location else None

    # pass to Meeting and return
    return Meeting(
        start_date=start_date,
        end_date=end_date,
        days=days,
        start_time=start_time,
        end_time=end_time,
        campus=campus,
        building=building,
        room=room,
        offering=offering,
    )


def parse_course_info(page: CoursePage) -> Course:
    """Parse the course info and return the course."""

    code_and_name = page.tree.css_first('h1[class="h1 page-hero__title"]').text(
        strip=True
    )
    subject, code = code_and_name[-9:].split(" ")
    name = code_and_name[:-9]
    prerequisites = page.tree.css_first('div[id="prereq"] ul li').text()
    credit_hours = float(page.tree.css_first('div[id="credits"] p').text(False))

    return Course(
        subject_id=subject,
        code=code,
        name=name,
        prerequisites=prerequisites,
        credits=credit_hours,
        url=page.url,
    )


def parse_term_node(term_node: Node) -> Term:
    """Parse the term node and return node."""
    term_id = term_node.parent.id
    year = int(term_id[:4])
    season = TERMS[int(term_id[-2:])]
    return Term(term_id=term_id, year=year, season=season)


def term_nodes(course_page: CoursePage) -> Iterator[Node]:
    """Parse CoursePage and yield term nodes."""
    for node in course_page.tree.css('div[id="offerings"] div[class="sctn"]'):
        yield node


def offering_nodes(term_node: Node) -> Iterator[Node]:
    """Parse term Node and yield offering nodes."""
    return (node for node in term_node.css('div[class="sctn"]'))


def meeting_nodes(offering_node: Node) -> Iterator[Node]:
    """Parse offering node and yield meeting nodes."""
    for node in offering_node.css_first('div[class="sctn-meets"]').css("tr")[1:]:
        yield node


def parse_response(response: Response) -> Course:
    """Parse the response and return the course."""

    course_page = CoursePage(response)
    course = parse_course_info(course_page)
    course.offerings = []

    for term_node in term_nodes(course_page):
        term = parse_term_node(term_node)
        for offering_node in offering_nodes(term_node):
            parse_offering_node(offering_node, course, term)

    return course


def prep_db(session: Session):
    """Remove rows from tables in the database and preload term table."""

    current_year = datetime.datetime.now().year
    for year in range(current_year, current_year + 2):
        for season_id, season in TERMS.items():
            term_id = f"{year}{season_id}"
            session.merge(Term(term_id=term_id, year=year, season=season))

    session.commit()


def scrape_course_urls(bcit_active_urls_url: str) -> dict[str, list[str]]:
    """Return list of urls for each subject_id key."""

    course_url_list = collect_response(bcit_active_urls_url)
    subject_urls = defaultdict(list)

    for url in course_url_list.json()["data"]:
        pattern = re.compile(r"([a-z]{4})-\d{4}/$")
        match = pattern.search(url)
        if match:
            subject_id = match.group(1).upper()
            subject_urls[subject_id] += [url]

    return subject_urls


def get_course_urls(session: Session, all_subjects: bool = False) -> list[str]:
    """Get course urls for subjects in the database."""

    # get subject course urls
    subject_urls = scrape_course_urls(BASE_URL + COURSE_LIST)

    # read subjects from db
    stmt = select(Subject)
    clauses = [Subject.is_active]
    if all_subjects:
        clauses.append(Subject.is_active == None)

    subjects = session.scalars(stmt.where(or_(*clauses))).all()

    # loop over subjects and add to list
    urls = []

    for subject in subjects:
        if subject.subject_id in subject_urls.keys():
            urls.extend(subject_urls[subject.subject_id])

    return urls


def extract_models(urls: list[str]) -> Iterator[Course]:
    """Extract data for BCIT courses and return as a list of Course objects."""
    base_url = "https://www.bcit.ca"
    course_responses = get_page_responses([f"{base_url}{url}" for url in urls])
    return (parse_response(response) for response in course_responses)


def load_courses(session: Session, courses: Iterator[Course]) -> int:
    """Merge courses into database."""

    for course in courses:
        course.set_id(session)
        session.merge(course)

    object_ct = len(session.dirty)

    session.commit()

    return object_ct


def bcit_to_sql(db_url: str, all_subjects: bool = False):
    """Parse BCIT Flex course pages and load them into the SQL database."""
    # [2023-09-10 Jonathan B.]
    #   It probably makes sense to refactor this function into load_db_command
    #   and lose the `if __name__ == "__main__"` block.

    # check response status
    collect_response(BASE_URL)

    # begin a non-ORM transaction
    engine = create_engine(db_url)
    connection = engine.connect()
    trans = connection.begin()

    # bind an individual Session to the connection with "create_savepoint"
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    try:
        # delete existing rows in tables
        prep_db(session)

        # get urls
        urls = get_course_urls(session, all_subjects)

        # get courses
        courses = extract_models(urls)

        # load
        count = load_courses(session, courses)

        # log
        print(f"Successfully loaded {count} objects.")

    except Exception as exc:
        trans.rollback()
        connection.close()
        raise exc

    else:
        trans.commit()
        connection.close()


# Flask CLI command
@click.command("load-db")
@click.option("--all-subjects", "-a", is_flag=True, help="Load all subjects.")
def load_db_command(all_subjects: bool = False):
    """Get data and replace what's in the database."""
    db_url = current_app.config["SQLALCHEMY_DATABASE_URI"]
    bcit_to_sql(db_url, all_subjects)


if __name__ == "__main__":
    bcit_to_sql("postgresql://python_app@localhost:5432/bcitflex")
