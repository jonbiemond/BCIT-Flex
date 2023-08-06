"""Tests for the meeting model."""
import datetime

from bcitflex.model import Meeting


class TestMeeting:
    """Test the properties of the Meeting Class"""

    def test_init(self, new_meeting: Meeting) -> None:
        """Test the constructor."""
        assert new_meeting.meeting_id == 1
        assert new_meeting.start_date == datetime.date(2023, 9, 13)
        assert new_meeting.end_date == datetime.date(2023, 11, 29)
        assert new_meeting.days == ["Wed"]
        assert new_meeting.start_time == datetime.time(18)
        assert new_meeting.end_time == datetime.time(21)
        assert new_meeting.campus == "Online"
        assert new_meeting.room is None
