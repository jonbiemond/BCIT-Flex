class Offering:
    def __init__(
            self,
            instructor: str,
            price: str,
            duration: str,
            meeting_times: list[str],
            status: str,
            rate_my_professor_urls: str
    ):
        self._instructor = instructor
        self._price = price
        self._duration = duration
        self._meeting_times = meeting_times
        self._status = status
        self._available = status not in ["Full", "In Progress"]
        self._rate_my_professor_urls = rate_my_professor_urls

    def instructor(self) -> str:
        return self._instructor

    def price(self) -> str:
        return self._price

    def duration(self) -> str:
        return self._duration

    def meeting_times(self) -> str:
        return "\n ".join(self._meeting_times)

    def status(self) -> str:
        return self._status

    def available(self) -> bool:
        return self._available

    def rate_my_professor_urls(self) -> str:
        return self._rate_my_professor_urls

    def to_string(self) -> str:
        info = (
            f" Instructor: {self.instructor()}\n"
            f" Price: {self.price()}\n" 
            f" Duration: {self.duration()}\n" 
            f" Meeting Times:\n {self.meeting_times()}\n" 
            f" Status: {self.status()}\n"
            f" Rate My Professor URLs: {self.rate_my_professor_urls()}\n"
        )
        return info
