"""Offering Meeting declaration."""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Sequence
from sqlalchemy.types import Date, Integer, String, Time

from . import Base

if TYPE_CHECKING:
    from . import Offering

meeting_id_seq = Sequence("meeting_id_sq")


class Meeting(Base):
    __tablename__ = "meeting"
    __table_args__ = {"comment": "Offering meeting times."}

    meeting_id: Mapped[Integer] = mapped_column(
        Integer,
        primary_key=True,
        server_default=meeting_id_seq.next_value(),
        doc="Meeting ID",
        comment="Serial meeting ID.",
    )
    crn: Mapped[String] = mapped_column(ForeignKey("offering.crn", ondelete="CASCADE"))
    start_date: Mapped[Date] = mapped_column(
        Date, doc="Start date", comment="Start date."
    )
    end_date: Mapped[Date] = mapped_column(Date, doc="End date", comment="End date.")
    days: Mapped[ARRAY | None] = mapped_column(
        ARRAY(String),
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
    room: Mapped[String | None] = mapped_column(
        String(10), doc="Meeting room", comment="Meeting room."
    )

    offering: Mapped["Offering"] = relationship(back_populates="meetings")

    def __repr__(self):
        return f"Meeting(id={self.meeting_id})"
