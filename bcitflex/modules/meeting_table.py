from tabulate import tabulate


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
