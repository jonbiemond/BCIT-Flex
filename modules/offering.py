class Offering:
    def __init__(self, instructor: str, price: str, duration: str,
                 meeting_times: list[str], rate_my_professor_urls: str):
        self._instructor = instructor
        self._price = price
        self._duration = duration
        self._meeting_times = meeting_times
        self._rate_my_professor_urls = rate_my_professor_urls

    def instructor(self) -> str:
        return self._instructor

    def price(self) -> str:
        return self._price

    def duration(self) -> str:
        return self._duration

    def meeting_times(self) -> str:
        return "\n ".join(self._meeting_times)

    def rate_my_professor_urls(self) -> str:
        return self._rate_my_professor_urls
