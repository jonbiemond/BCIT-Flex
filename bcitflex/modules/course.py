from bcitflex.model.offering import Offering


class Course:
    def __init__(
        self,
        subject: str,
        code: str,
        name: str,
        prerequisites: str,
        _credits: str,
        url: str,
        offerings: list[Offering],
    ):
        self._subject = subject
        self._code = code
        self._name = name
        self._prerequisites = prerequisites
        self.__credits = _credits
        self._url = url
        self._offerings = offerings
        self._offering_count = len(offerings)
        self.status = self.__status()

    def subject(self) -> str:
        return self._subject

    def code(self) -> str:
        return self._code

    def name(self) -> str:
        return self._name

    def prerequisites(self) -> str:
        return self._prerequisites

    def credits(self) -> str:
        return self.__credits

    def url(self) -> str:
        return self._url

    def offerings(self) -> list[Offering]:
        return self._offerings

    def offering_count(self, available_only=False) -> int:
        if available_only:
            return len(
                [offering for offering in self.offerings() if offering.available()]
            )
        return self._offering_count

    def __status(self) -> str:
        if self.offering_count(available_only=True) > 0:
            return "Available"

        return "Unavailable"

    def to_string(self, available_only=False) -> str:
        offering_count = 0
        offering_info = ""

        for offering in self.offerings():
            if available_only:
                if not offering.available():
                    continue
            offering_count += 1
            offering_info += offering.to_string() + "\n"

        course_info = (
            f"Course: {self.subject()} {self.code()}\n"
            f"Name: {self.name()}\n"
            f"Prerequisites: {self.prerequisites()}\n"
            f"Credits: {self.credits()}\n"
            f"URL: {self.url()}\n"
            f"Offerings: {offering_count}\n"
        )
        info = course_info + offering_info + "\n"
        return info
