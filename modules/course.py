from modules.offering import Offering


class Course:
    def __init__(self, code: str, name: str, prerequisites: str, _credits: str, url: str, offerings: list[Offering]):
        self._code = code
        self._name = name
        self._prerequisites = prerequisites
        self.__credits = _credits
        self._url = url
        self._offerings = offerings

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
