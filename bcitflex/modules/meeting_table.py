import datetime

from tabulate import tabulate

WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


class EmptyMeetingError(Exception):
    def __init__(self):
        super().__init__("Offering has no meetings.")


# TODO: convert to model
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
            except ValueError as err:
                raise ValueError(f"Invalid date format: {date_str}") from err

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

        days = []

        for meeting in self._rows:
            days_str = meeting[1]

            meeting_days = days_str.split(" - ")
            if len(meeting_days) > 1:
                start, stop = (WEEKDAYS.index(day) for day in meeting_days)
                meeting_days = WEEKDAYS[start : stop + 1]

            else:
                meeting_days = days_str.split(", ")

            for day in meeting_days:
                if day in WEEKDAYS and day not in days:
                    days.append(day)

        return days

    def __get_time(self, idx: int) -> datetime.time | None:
        if idx not in [0, -1]:
            raise ValueError("Index must be 0 or -1")

        if not self:
            raise EmptyMeetingError()

        time_str = self._rows[0][2].split(" - ")[idx]

        if time_str == "N/A":
            return None

        time = datetime.datetime.strptime(time_str, "%H:%M").time()

        return time

    def start_time(self) -> datetime.time:
        return self.__get_time(0)

    def end_time(self) -> datetime.time:
        return self.__get_time(-1)

    def location(self) -> str:
        if not self:
            raise EmptyMeetingError()

        location_detail = self._rows[0][3]
        campus = location_detail.split(" ")[0]

        return campus
