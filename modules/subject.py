from concurrent.futures import ThreadPoolExecutor
from datetime import date

import requests
from selectolax.parser import HTMLParser

from modules.course import Course
from modules.offering import Offering

URL = "https://www.bcit.ca/wp-json/bcit/ptscc/v1/list-active-urls"


def next_term(url: str) -> str:
    response = requests.get(url)

    if response.status_code != 200:
        print(f"next term response status code {response.status_code}")

    else:
        html_parser = HTMLParser(response.text)

        for term in range(30, 0, -10):
            if html_parser.css_first(f'div[id="{date.today().year}{term}"]') is not None:
                return f"{date.today().year}{term}"


def parse_url(url: str, term: str, names_and_ids: dict[str, str]) -> Course | None:
    response = requests.get(url)

    if response.status_code != 200:
        print(f"parse url response status code {response.status_code}")

    else:
        html_parser = HTMLParser(response.text)

        code_and_name = html_parser.css_first('h1[class="h1 page-hero__title"]').text(strip=True)
        prerequisites = html_parser.css_first('div[id="prereq"] ul li').text()
        _credits = html_parser.css_first('div[id="credits"] p').text(False)

        offerings = []
        for offering in html_parser.css(f'div[id="{term}"] div[class="sctn"]'):
            instructor_node = offering.css_first('div[class="sctn-instructor"] p')

            if instructor_node is None:
                instructor = "Not Available"
            else:
                instructor = instructor_node.text(False)

            price = offering.css_first('li[class="sctn-block-list-item cost"').text(False)
            duration = offering.css_first('li[class="sctn-block-list-item duration"]').text(False)

            no_meeting_node = offering.css_first('div[class="sctn-no-meets"] p')

            meeting_times = []
            if no_meeting_node is None:
                for meeting_time in offering.css('div[class="sctn-meets"]'):
                    for row in meeting_time.css('tr'):
                        meeting_times.append(row.text(separator=" ", strip=True).strip())

            else:
                meeting_times.append(no_meeting_node.text())

            ids = names_and_ids.get(instructor.lower())

            rate_my_professor_urls = ""
            if ids:
                for _id in ids.split(" "):
                    rate_my_professor_urls += f"https://www.ratemyprofessors.com/professor?tid={_id} "

            else:
                rate_my_professor_urls = "Not Available"

            status_node = offering.css_first(f'p[class="sctn-status-lbl"]')

            if status_node is None or status_node.text(False) == "Sneak Preview":
                offerings.append(Offering(instructor, price, duration, meeting_times, rate_my_professor_urls.strip()))

        if offerings:
            return Course(code_and_name[-9:], code_and_name[:-9], prerequisites, _credits, url, offerings)

        return None


def available_courses(urls: list[str]) -> list[Course | None]:
    base_url = "https://www.bcit.ca"

    term = next_term(f"{base_url}{urls[0]}")

    names_and_ids = {}
    for line in open("bcit_rate_my_professors.txt"):
        name_and_id = line.rstrip("\n").split("|")
        names_and_ids.update({name_and_id[0]: name_and_id[1]})

    courses = []
    with ThreadPoolExecutor() as executor:
        for i in range(len(urls)):
            courses.append(executor.submit(parse_url, f"{base_url}{urls[i]}", term, names_and_ids).result())

    return courses


class Subject:
    def __init__(self, name: str):
        self._response = requests.get(URL)
        if self._response.status_code != 200:
            raise Exception(f"Active urls response status code {self._response.status_code}")
        self._name = name
        self._courses = self.get_courses()

    def name(self) -> str:
        return self._name

    def courses(self) -> list[Course]:
        return self._courses

    def get_courses(self) -> list[Course]:
        return available_courses([url for url in self._response.json()["data"] if f"-{self.name()}-" in url[-11:]])

    def to_file(self):
        with open(rf"..\{self.name()}_courses.txt", "w") as file:
            for course in self.courses():
                if course:
                    file.write(f"Code {course.code()}\n"
                               f"Name {course.name()}\n"
                               f"Prerequisites {course.prerequisites()}\n"
                               f"Credits {course.credits()}\n"
                               f"URL {course.url()}\n"
                               f"Offerings\n")

                    for offering in course.offerings():
                        file.write(f" Instructor {offering.instructor()}\n"
                                   f" Price {offering.price()}\n"
                                   f" Duration {offering.duration()}\n"
                                   f" Meeting Times\n {offering.meeting_times()}\n"
                                   f" Rate My Professor URLs {offering.rate_my_professor_urls()}\n\n")

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
