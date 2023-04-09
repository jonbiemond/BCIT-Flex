from tabulate import tabulate
import datetime


class EmptyMeetingError(Exception):
    def __init__(self):
        super().__init__("Offering has no meetings.")


class MeetingTable:
    def __init__(self):
        self._headers = ["Dates", "Days", "Times", "Locations"]
        self._rows = []
        self._status = "Available"

    def status(self) -> str:
        return self._status

    def __len__(self):
        return len(self._rows)

    def __bool__(self):
        return bool(self._rows)

    def add_meeting(self, dates: str, days: str, times: str, locations: str):
        self._rows.append([dates, days, times, locations])

    def set_status(self, status: str):
        self._status = status

    def to_string(self) -> str:
        table = tabulate(self._rows, headers=self._headers, tablefmt="grid")
        return table

    def __get_dates(self, idx: int) -> list[datetime.date]:
        if idx not in [0, -1]:
            raise ValueError("Index must be 0 or -1")

        if not self:
            raise EmptyMeetingError()

        dates = []

        for meeting in self._rows:
            dates_str = meeting[0]
            date_str = dates_str.split(" - ")[idx]
            year = datetime.datetime.now().year

            try:
                end_date = datetime.datetime.strptime(date_str, "%b %d").date()
            except ValueError:
                raise ValueError(f"Invalid date format: {date_str}")

            end_date = end_date.replace(year=year)
            dates.append(end_date)

        return dates

    def start_date(self) -> datetime.date:
        dates = self.__get_dates(0)
        return min(dates)

    def end_date(self) -> datetime.date:
        dates = self.__get_dates(-1)
        return max(dates)

    def days(self) -> list[str]:
        if not self:
            raise EmptyMeetingError()

        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        days = []

        for meeting in self._rows:
            days_str = meeting[1]

            meeting_days = days_str.split(' - ')
            if len(meeting_days) > 1:
                start, stop = (weekdays.index(day) for day in meeting_days)
                meeting_days = weekdays[start : stop + 1]

            else:
                meeting_days = days_str.split(', ')

            for day in meeting_days:
                if day in weekdays and day not in days:
                    days.append(day)

        return days


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
