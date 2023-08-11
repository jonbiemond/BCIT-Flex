"""Offering Meeting declaration."""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, inspect, select
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Date, Integer, String, Time
from tabulate import tabulate

from . import Base

if TYPE_CHECKING:
    from . import Offering


def nssequence(context: DefaultExecutionContext):
    crn = context.get_current_parameters()["crn"]
    stmt = select(func.max(Meeting.meeting_id)).where(Meeting.crn == crn)
    max_id = context.connection.scalar(stmt)
    return max_id + 1 if max_id else 1


class Meeting(Base):
    __tablename__ = "meeting"
    __table_args__ = {"comment": "Offering meeting times."}

    meeting_id: Mapped[Integer] = mapped_column(
        Integer,
        primary_key=True,
        server_default=None,
        doc="Meeting ID",
        comment="Serial meeting ID partitioned within crn.",
        default=nssequence,
    )
    crn: Mapped[String] = mapped_column(
        ForeignKey("offering.crn", ondelete="CASCADE"), primary_key=True
    )
    start_date: Mapped[Date] = mapped_column(
        Date, doc="Start date", comment="Start date."
    )
    end_date: Mapped[Date] = mapped_column(Date, doc="End date", comment="End date.")
    days: Mapped[ARRAY | None] = mapped_column(
        ARRAY(String(3)),
        doc="Days of the week",
        comment="Days of the week offering meets on.",
    )
    start_time: Mapped[Time | None] = mapped_column(
        Time, doc="Start time", comment="Start time."
    )
    end_time: Mapped[Time | None] = mapped_column(
        Time, doc="End time", comment="End time."
    )
    campus: Mapped[String | None] = mapped_column(
        String(30), doc="Meeting campus", comment="Meeting campus."
    )
    building: Mapped[String | None] = mapped_column(
        String(10), doc="Meeting building", comment="Meeting building."
    )
    room: Mapped[String | None] = mapped_column(
        String(10), doc="Meeting room", comment="Meeting room."
    )

    offering: Mapped["Offering"] = relationship(back_populates="meetings")

    def __repr__(self):
        return f"Meeting(id={self.meeting_id}, crn={self.crn})"

    def __setattr__(self, key, value):
        """Set meeting_id if not set."""
        if key == "offering" and self.meeting_id is None:
            self.meeting_id = value.next_meeting_id()
        super().__setattr__(key, value)


def tabulate_meetings(meetings: list[Meeting]) -> str:
    """Return tabulated string of Meeting info."""
    headers = ["meeting_id"] + inspect(Meeting).columns.keys()[2:]
    rows = [[getattr(meeting, column) for column in headers] for meeting in meetings]
    return tabulate(rows, headers=headers, tablefmt="grid")
