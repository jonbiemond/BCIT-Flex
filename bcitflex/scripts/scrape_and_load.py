"""Script to scrape course data and load it to the databse. """
import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

import requests
from requests import Response
from selectolax.parser import HTMLParser, Node
from sqlalchemy import create_engine, delete, select
from sqlalchemy.orm import Session

from bcitflex.model import Base, Course, Offering, Subject
from bcitflex.modules.meeting_table import MeetingTable

BASE_URL = "https://www.bcit.ca"
COURSE_LIST = "/wp-json/bcit/ptscc/v1/list-active-urls"


class CoursePage:
    """HTML representation of a course page."""

    def __init__(self, response: Response) -> None:
        self.url: str = response.url
        self.html: HTMLParser = HTMLParser(response.text)
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


def parse_offering_node(node: Node, course: Course) -> Offering:
    """Parse the offering node and return the offering."""

    # TODO: Add crn

    # get instructor
    instructor_node = node.css_first('div[class="sctn-instructor"] p')

    if instructor_node is None:
        instructor = "Not Available"
    else:
        instructor = instructor_node.text(False)

    # get price
    price = node.css_first('li[class="sctn-block-list-item cost"').text(False)
    price = float(price.removeprefix("$"))

    # get duration
    duration = node.css_first('li[class="sctn-block-list-item duration"]').text(False)

    # get meeting times
    no_meeting_node = node.css_first('div[class="sctn-no-meets"] p')

    meeting_times = MeetingTable()
    if no_meeting_node is None:
        for meeting_time in node.css('div[class="sctn-meets"]'):
            for row in meeting_time.css("tr")[1:]:
                row_elements = list(
                    filter(
                        None,
                        [element.strip() for element in row.text().split("\n")],
                    )
                )
                meeting_times.add_meeting(*row_elements)

    else:
        meeting_times.set_status(no_meeting_node.text(False))

    # get status
    status_node = node.css_first('p[class="sctn-status-lbl"]')

    if status_node is None:
        status = "Available"

    else:
        status = status_node.text(False)

    return Offering(
        crn=None,
        instructor=instructor,
        price=price,
        duration=duration,
        status=status,
        course=course,
    )


def parse_course_info(page: CoursePage) -> Course:
    """Parse the course info and return the course."""

    code_and_name = page.html.css_first('h1[class="h1 page-hero__title"]').text(
        strip=True
    )
    subject, code = code_and_name[-9:].split(" ")
    name = code_and_name[:-9]
    prerequisites = page.html.css_first('div[id="prereq"] ul li').text()
    credit_hours = float(page.html.css_first('div[id="credits"] p').text(False))

    return Course(
        subject_id=subject,
        code=code,
        name=name,
        prerequisites=prerequisites,
        credits=credit_hours,
        url=page.url,
    )


def parse_response(response: Response, term: str) -> Course:
    """Parse the response and return the course."""

    course_page = CoursePage(response)
    course = parse_course_info(course_page)
    course.offerings = []

    for offering in course_page.html.css(f'div[id="{term}"] div[class="sctn"]'):
        parse_offering_node(offering, course)

    return course


def prep_db(session: Session):
    """Remove rows from tables in the database."""
    session.execute(delete(Course))


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


def get_course_urls(session: Session) -> list[str]:
    """Get course urls for subjects in the database."""

    # get subject course urls
    subject_urls = scrape_course_urls(BASE_URL + COURSE_LIST)

    # read subjects from db
    subjects = session.scalars(select(Subject)).all()

    # loop over subjects and add to list
    urls = []

    for subject in subjects:
        if subject.subject_id in subject_urls.keys():
            urls.extend(subject_urls[subject.subject_id])

    return urls


def extract_models(urls: list[str]) -> list[Course]:
    """Extract data for BCIT courses and return as list of Course objects."""
    base_url = "https://www.bcit.ca"
    term = next_term(collect_response(f"{base_url}{urls[0]}"))
    course_responses = get_page_responses([f"{base_url}{url}" for url in urls])
    courses = [parse_response(response, term) for response in course_responses]
    return courses


def load_models(session, models: list[Base]) -> None:
    """Commit models to database."""

    for model in models:
        session.add(model)

    session.commit()


def bcit_to_sql(db_url: str):
    """Parse BCIT Flex course pages and load them into a SQL database."""

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
        urls = get_course_urls(session)

        # get courses
        courses = extract_models(urls)

        # load
        load_models(session, courses)

        # log
        print(f"Successfully updated {len(courses)} courses.")

    except Exception as exc:
        trans.rollback()
        connection.close()
        raise exc

    else:
        trans.commit()
        connection.close()


if __name__ == "__main__":
    bcit_to_sql("postgresql://python_app@localhost:5432/bcitflex")
