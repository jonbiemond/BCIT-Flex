from modules.offering import Offering


class Course:
    def __init__(self,
                 subject: str,
                 code: str,
                 name: str,
                 prerequisites: str,
                 _credits: str,
                 url: str,
                 offerings: list[Offering]):
        self._subject = subject
        self._code = code
        self._name = name
        self._prerequisites = prerequisites
        self.__credits = _credits
        self._url = url
        self._offerings = offerings
        self._offerings_count = len(offerings)

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

    def to_string(self) -> str:
        info = (
            f"Code: {self.subject()} {self.code()}\n"
            f"Name: {self.name()}\n"
            f"Prerequisites: {self.prerequisites()}\n"
            f"Credits: {self.credits()}\n"
            f"URL: {self.url()}\n"
            f"Offerings: {self._offerings_count}\n"
        )
        for offering in self.offerings():
            info += offering.to_string() + "\n"
        info += "\n"
        return info
