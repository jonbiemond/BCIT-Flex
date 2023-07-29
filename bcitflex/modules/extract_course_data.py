"""Logic to parse course data."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

import requests
from requests import Response
from selectolax.parser import HTMLParser, Node

from bcitflex.model import Offering
from bcitflex.modules.course import Course
from bcitflex.modules.meeting_table import MeetingTable


def next_term(url: str) -> str:
    """Get the next term from the given URL."""

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Next term response status code: {response.status_code}")

    else:
        html_parser = HTMLParser(response.text)

        for term in range(30, 0, -10):
            if (
                html_parser.css_first(f'div[id="{date.today().year}{term}"]')
                is not None
            ):
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


def get_course_responses(urls: list[str]) -> list[Response]:
    """Get the responses from the given course URLs."""

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(collect_response, url) for url in urls]
        responses = [future.result() for future in as_completed(futures)]

    return responses


def parse_offering_node(node: Node) -> Offering:
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
    )


def parse_response(response: Response, term: str) -> Course:
    """Parse the response and return the course."""

    html_parser = HTMLParser(response.text)

    code_and_name = html_parser.css_first('h1[class="h1 page-hero__title"]').text(
        strip=True
    )
    subject, code = code_and_name[-9:].split(" ")
    name = code_and_name[:-9]
    prerequisites = html_parser.css_first('div[id="prereq"] ul li').text()
    _credits = html_parser.css_first('div[id="credits"] p').text(False)

    offerings = []
    for offering in html_parser.css(f'div[id="{term}"] div[class="sctn"]'):
        offerings.append(parse_offering_node(offering))

    return Course(subject, code, name, prerequisites, _credits, response.url, offerings)


def available_courses(urls: list[str]) -> list[Course]:
    base_url = "https://www.bcit.ca"

    term = next_term(f"{base_url}{urls[0]}")

    course_responses = get_course_responses([f"{base_url}{url}" for url in urls])

    courses = [parse_response(response, term) for response in course_responses]

    return courses
