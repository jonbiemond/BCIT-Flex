import pytest
import datetime

from modules.offering import Offering, MeetingTable, EmptyMeetingError


@pytest.fixture
def meeting_times():
    meeting_times = MeetingTable()
    meeting_times.add_meeting("Apr 04 - Jun 20", "Tue", "18:00 - 21:30", "Burnaby")
    meeting_times.add_meeting("May 09", "Tue", "18:00 - 21:30", "Burnaby SW01 Rm. 3190")
    meeting_times.add_meeting("Jun 20", "Tue", "18:00 - 21:30", "Burnaby SW01 Rm. 3170")
    return meeting_times


@pytest.fixture
def offering(meeting_times):
    return Offering(
        "John Smith",
        "$546.00",
        "12 weeks",
        meeting_times,
        "Available",
        "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=123456",
    )


@pytest.fixture
def empty_meeting():
    return MeetingTable()


# MeetingTable tests
def test_meeting_set_status():
    meeting_times = MeetingTable()
    meeting_times.set_status("No meeting times available")
    assert meeting_times.status() == "No meeting times available"


def test_meeting_get_start_date(meeting_times):
    year = datetime.datetime.now().year
    assert meeting_times.start_date() == datetime.date(year, 4, 4)

    meeting_times_2 = MeetingTable()
    meeting_times_2.add_meeting("Apr 04", "Tue", "18:00 - 21:30", "Burnaby")
    assert meeting_times_2.start_date() == datetime.date(year, 4, 4)


def test_meeting_get_end_date(meeting_times):
    year = datetime.datetime.now().year
    assert meeting_times.end_date() == datetime.date(year, 6, 20)

    meeting_times_2 = MeetingTable()
    meeting_times_2.add_meeting("Apr 04 - Jun 20", "Tue", "18:00 - 21:30", "Burnaby")
    meeting_times_2.add_meeting(
        "Jul 04", "Tue", "18:00 - 21:30", "Burnaby SW01 Rm. 3190"
    )
    assert meeting_times_2.end_date() == datetime.date(year, 7, 4)


def test_meeting_invalid_start_date():
    meeting_times = MeetingTable()
    meeting_times.add_meeting("N/A", "Tue", "18:00 - 21:30", "Burnaby")
    with pytest.raises(ValueError):
        meeting_times.start_date()


def test_empty_meeting_start_date(empty_meeting):
    with pytest.raises(EmptyMeetingError):
        empty_meeting.start_date()


def test_meeting_get_days(meeting_times):
    assert meeting_times.days() == ["Tue"]

    meeting_days_1 = MeetingTable()
    meeting_days_1.add_meeting(
        "Apr 04 - Jun 20", "Tue, Thu", "18:00 - 21:30", "Burnaby"
    )
    assert meeting_days_1.days() == ["Tue", "Thu"]

    meeting_days_2 = MeetingTable()
    meeting_days_2.add_meeting(
        "Apr 04 - Jun 20", "Tue - Fri", "18:00 - 21:30", "Burnaby"
    )
    assert meeting_days_2.days() == ["Tue", "Wed", "Thu", "Fri"]

    meeting_days_3 = MeetingTable()
    meeting_days_3.add_meeting("Apr 04 - Jun 20", "Mon", "18:00 - 21:30", "Burnaby")
    meeting_days_3.add_meeting("Apr 04 - Jun 20", "Tue", "18:00 - 21:30", "Burnaby")
    assert meeting_days_3.days() == ["Mon", "Tue"]

    meeting_days_4 = MeetingTable()
    meeting_days_4.add_meeting("Apr 04 - Jun 20", "N/A", "18:00 - 21:30", "Burnaby")
    assert meeting_days_4.days() == []


def test_meeting_get_start_time(meeting_times):
    assert meeting_times.start_time() == datetime.time(18, 0)

    meeting_times_1 = MeetingTable()
    meeting_times_1.add_meeting("N/A", "Tue", "N/A", "Burnaby")
    assert meeting_times_1.start_time() is None


def test_meeting_get_end_time(meeting_times):
    assert meeting_times.end_time() == datetime.time(21, 30)

    meeting_times_1 = MeetingTable()
    meeting_times_1.add_meeting("N/A", "Tue", "N/A", "Burnaby")
    assert meeting_times_1.end_time() is None


def test_meeting_get_location(meeting_times):
    assert meeting_times.location() == "Burnaby"

    meeting_times_1 = MeetingTable()
    meeting_times_1.add_meeting("N/A", "Tue", "N/A", "Online")
    assert meeting_times_1.location() == "Online"

    meeting_times_2 = MeetingTable()
    meeting_times_2.add_meeting("N/A", "Tue", "N/A", "N/A")
    assert meeting_times_2.location() == "N/A"


# Offering tests
def test_offering_available(offering):
    assert offering.available() is True


def test_offering_not_on_day(offering):
    assert offering.not_on_any_days(["Mon"]) is True
    assert offering.not_on_any_days(["Tue", "Wed"]) is False


def test_offering_not_on_day_invalid(offering):
    with pytest.raises(ValueError):
        offering.not_on_any_days(["Mon", "Tue", "Thur"])


def test_offering_is_part_time(offering):
    assert offering.is_part_time() is True
