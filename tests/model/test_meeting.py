"""Tests for the meeting model."""
import datetime

from sqlalchemy.orm import Session

from bcitflex.model import Meeting, Offering
from tests import dbtest


class TestMeeting:
    """Test the properties of the Meeting Class"""

    def test_init(self, new_meeting: Meeting) -> None:
        """Test the constructor."""
        assert new_meeting.crn == "12345"
        assert new_meeting.start_date == datetime.date(2023, 9, 13)
        assert new_meeting.end_date == datetime.date(2023, 11, 29)
        assert new_meeting.days == ["Wed"]
        assert new_meeting.start_time == datetime.time(18)
        assert new_meeting.end_time == datetime.time(21)
        assert new_meeting.campus == "Online"
        assert new_meeting.building is None
        assert new_meeting.room is None

    def test_set_meeting_id(self, new_meeting: Meeting, new_offering: Offering) -> None:
        """Test adding an offering to a meeting sets the meeting_id."""
        new_meeting.offering = new_offering
        assert new_meeting.meeting_id == 1

    def test_set_new_meeting_id(self, new_offering: Offering) -> None:
        """Test adding an offering during instantiation sets the meeting_id."""
        new_meeting = Meeting(
            start_date=datetime.date(2023, 9, 13),
            end_date=datetime.date(2023, 11, 29),
            offering=new_offering,
        )
        assert new_meeting.meeting_id == 1


@dbtest
class TestMeetingDB:
    """Test the Offering class with a database session."""

    def test_get_meeting(self, session: Session) -> None:
        """Test getting a meeting from the db."""
        meeting = session.get(Meeting, (1, "12345"))
        assert meeting.meeting_id == 1

    def test_update_meeting(self, session: Session) -> None:
        """Test updating a meeting in the db."""
        meeting = session.get(Meeting, (1, "12345"))
        meeting.start_time = datetime.time(17, 30)
        session.commit()
        assert meeting.start_time == datetime.time(17, 30)

    def test_add_second_meeting(self, session: Session, new_meeting: Meeting) -> None:
        """Test adding a meeting to the db."""
        session.add(new_meeting)
        session.commit()
        assert new_meeting.crn == "12345"
        assert new_meeting.meeting_id == 2

    def test_add_first_meeting(
        self, session: Session, new_offering: Offering, new_meeting: Meeting
    ) -> None:
        """Test adding the first meeting of an offering."""
        # new_offering.meetings.append(new_meeting)
        new_meeting.offering = new_offering
        session.add(new_offering)
        session.commit()
        assert new_meeting.crn == "67890"
        assert new_meeting.meeting_id == 1

    def test_add_two_meetings(
        self, session: Session, new_offering: Offering, new_meeting: Meeting
    ) -> None:
        """Test adding two meetings to an offering."""
        primary_meeting = new_meeting
        secondary_meeting = Meeting(
            start_date=datetime.date(2023, 9, 13),
            end_date=datetime.date(2023, 11, 29),
            days=["Thu"],
            start_time=datetime.time(18),
            end_time=datetime.time(21),
            campus="Online",
            room=None,
        )
        new_offering.crn = "54321"
        primary_meeting.offering = new_offering
        secondary_meeting.offering = new_offering
        session.add(new_offering)
        session.commit()
        assert primary_meeting.crn == "54321"
        assert primary_meeting.meeting_id == 1
        assert secondary_meeting.crn == "54321"
        assert secondary_meeting.meeting_id == 2
