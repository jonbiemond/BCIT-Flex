from tabulate import tabulate


class MeetingTable:
    def __init__(self):
        self._headers = ["Dates", "Days", "Times", "Locations"]
        self._rows = []
        self._status = "Available"

    def add_meeting(self, dates: str, days: str, times: str, locations: str):
        self._rows.append([dates, days, times, locations])

    def set_status(self, status: str):
        self._status = status

    def to_string(self) -> str:
        table = tabulate(self._rows, headers=self._headers, tablefmt="grid")
        return table


class Offering:
    def __init__(
            self,
            instructor: str,
            price: str,
            duration: str,
            meeting_times: MeetingTable,
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
        return self._meeting_times.to_string()

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
            f" Meeting Times:\n{self.meeting_times()}\n" 
            f" Status: {self.status()}\n"
            f" Rate My Professor URLs: {self.rate_my_professor_urls()}\n"
        )
        return info
