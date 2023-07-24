"""BCIT course parsing logic."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

import requests
from selectolax.parser import HTMLParser

from bcitflex.modules.course import Course
from bcitflex.modules.offering import MeetingTable, Offering


def next_term(url: str) -> str:
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


def parse_url(url: str, term: str, rmp_ids: dict[str, str]) -> Course:
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Parse url response status code: {response.status_code}")

    else:
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
            instructor_node = offering.css_first('div[class="sctn-instructor"] p')

            if instructor_node is None:
                instructor = "Not Available"
            else:
                instructor = instructor_node.text(False)

            price = offering.css_first('li[class="sctn-block-list-item cost"').text(
                False
            )
            duration = offering.css_first(
                'li[class="sctn-block-list-item duration"]'
            ).text(False)

            no_meeting_node = offering.css_first('div[class="sctn-no-meets"] p')

            meeting_times = MeetingTable()
            if no_meeting_node is None:
                for meeting_time in offering.css('div[class="sctn-meets"]'):
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

            ids = rmp_ids.get(instructor.lower())

            rate_my_professor_urls = ""
            if ids:
                for _id in ids.split(" "):
                    rate_my_professor_urls += (
                        f"https://www.ratemyprofessors.com/professor?tid={_id} "
                    )

            else:
                rate_my_professor_urls = "Not Available"

            status_node = offering.css_first('p[class="sctn-status-lbl"]')

            if status_node is None:
                status = "Available"

            else:
                status = status_node.text(False)

            offerings.append(
                Offering(
                    instructor,
                    price,
                    duration,
                    meeting_times,
                    status,
                    rate_my_professor_urls.strip(),
                )
            )

        return Course(subject, code, name, prerequisites, _credits, url, offerings)


def available_courses(urls: list[str]) -> list[Course]:
    base_url = "https://www.bcit.ca"

    term = next_term(f"{base_url}{urls[0]}")

    rmp_ids = {}
    for line in open(r"../resources/bcit_rate_my_professors.txt"):
        name_and_id = line.rstrip("\n").split("|")
        rmp_ids.update({name_and_id[0]: name_and_id[1]})

    courses = []

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(parse_url, f"{base_url}{url}", term, rmp_ids)
            for url in urls
        ]
        for future in as_completed(futures):
            courses.append(future.result())

    return courses
