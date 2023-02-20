from concurrent.futures import ThreadPoolExecutor
from datetime import date

import requests
from selectolax.parser import HTMLParser

from modules.course import Course
from modules.offering import Offering


def valid_subject() -> str:
    subject = input("Enter a subject ").strip().lower()

    while subject not in open("subjects.txt").read().splitlines():
        subject = input(f"\"{subject}\" is not a valid subject, please try again ").strip().lower()

    return subject


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
            instructor = offering.css_first('div[class="sctn-instructor"] p').text(False)
            price = offering.css_first('li[class="sctn-block-list-item cost"').text(False)
            duration = offering.css_first('li[class="sctn-block-list-item duration"]').text(False)

            no_meeting_element = offering.css_first('div[class="sctn-no-meets"] p')

            meeting_times = []
            if no_meeting_element is None:
                for meeting_time in offering.css('div[class="sctn-meets"]'):
                    for row in meeting_time.css('tr'):
                        meeting_times.append(row.text(separator=" ", strip=True).strip())

            else:
                meeting_times.append(no_meeting_element.text())

            ids = names_and_ids.get(instructor.lower())

            rate_my_professor_urls = ""
            if ids:
                for _id in ids.split(" "):
                    rate_my_professor_urls += f"https://www.ratemyprofessors.com/professor?tid={_id} "

            else:
                rate_my_professor_urls = "Not Found"

            status_element = offering.css_first(f'p[class="sctn-status-lbl"]')

            if status_element is None or status_element.text(False) == "Sneak Preview":
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


def main():
    subject = valid_subject()

    response = requests.get("https://www.bcit.ca/wp-json/bcit/ptscc/v1/list-active-urls")

    if response.status_code != 200:
        print(f"active urls response status code {response.status_code}")

    else:
        with open(f"{subject}_courses.txt", "w") as file:
            for course in available_courses([url for url in response.json()["data"] if f"-{subject}-" in url]):
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


if __name__ == '__main__':
    main()
