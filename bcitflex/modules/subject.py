from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

import requests
from selectolax.parser import HTMLParser

from .course import Course
from .offering import MeetingTable, Offering

URL = "https://www.bcit.ca/wp-json/bcit/ptscc/v1/list-active-urls"


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


class Subject:
    def __init__(self, name: str):
        self._response = requests.get(URL)
        if self._response.status_code != 200:
            raise Exception(
                f"Active urls response status code {self._response.status_code}"
            )
        self._name = name
        self._courses = self.__get_courses()

    def name(self) -> str:
        return self._name

    def courses(self, **filters) -> list[Course]:
        courses = self._courses
        for key, value in filters.items():
            if value is None:
                continue
            if isinstance(value, str):
                value = [value]
            courses = [course for course in courses if getattr(course, key) in value]
        return courses

    def courses_to_string(self, **filters) -> str:
        return "\n".join([course.to_string() for course in self.courses(**filters)])

    def __get_courses(self) -> list[Course]:
        urls = []
        for url in self._response.json()["data"]:
            if f"-{self.name()}-" in url[-11:]:
                urls.append(url)
        if len(urls) == 0:
            raise ValueError(f"Subject {self.name()} does not contain any courses.")
        return available_courses(urls)

    def to_file(self):
        filename = f"{self.name()}_courses.txt"
        with open(filename, "w") as file:
            for course in self.courses():
                if course:
                    file.write(course.to_string())

        return filename

    def has_course(self, code: str) -> bool:
        for course in self.courses():
            if course.code() == code:
                return True

        return False

    def get_course(self, code: str) -> Course:
        for course in self.courses():
            if course.code() == code:
                return course

        raise ValueError(f"Course {code} not found in {self.name()}")


if __name__ == "__main__":
    subject = Subject("COMP")
    print(subject.get_course("2854").to_string())
