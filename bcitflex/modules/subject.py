import requests

from bcitflex.modules.extract_course_data import available_courses

from .course import Course

URL = "https://www.bcit.ca/wp-json/bcit/ptscc/v1/list-active-urls"


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
