"""Course Offering and Meeting declarations."""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import NUMERIC, Float, Integer, String

from . import Base

if TYPE_CHECKING:
    from . import Course, Meeting, Term


class Offering(Base):
    __tablename__ = "offering"
    __table_args__ = {"comment": "Course offerings."}

    crn: Mapped[String] = mapped_column(
        String(5),
        primary_key=True,
        doc="Course Reference Number",
        comment="Course Reference Number, unique to offering.",
    )
    instructor: Mapped[String] = mapped_column(
        String(30), doc="Instructor", comment="Instructor."
    )
    price: Mapped[Float] = mapped_column(NUMERIC, doc="Price", comment="Price.")
    duration: Mapped[String] = mapped_column(
        String(30), doc="Duration Weeks", comment="Duration in weeks."
    )
    status: Mapped[String] = mapped_column(
        String(30), doc="Status", comment="Status of course offering."
    )
    course_id: Mapped[Integer] = mapped_column(
        ForeignKey("course.course_id", ondelete="CASCADE")
    )
    term_id: Mapped[String] = mapped_column(ForeignKey("term.term_id"))

    course: Mapped["Course"] = relationship(back_populates="offerings")
    term: Mapped["Term"] = relationship(back_populates="offerings")

    meetings: Mapped[list["Meeting"]] = relationship(back_populates="offering")

    def __repr__(self):
        return f"Offering(course={self.course.fullcode if self.course else None}, crn={self.crn}, instructor={self.instructor},  status={self.status})"

    def __str__(self) -> str:
        info = (
            f"CRN: {self.crn}\n"
            f" Instructor: {self.instructor}\n"
            f" Price: {self.price}\n"
            f" Duration: {self.duration}\n"
            f" Status: {self.status}\n"
        )
        return info

    @property
    def available(self):
        return self.status not in ["Full", "In Progress"]

    def next_meeting_id(self) -> int:
        """Get the next meeting_id for the crn."""
        max_id = max(m.meeting_id for m in self.meetings) if self.meetings else 0
        if max_id is None:
            raise ValueError(
                "An existing meeting does not have a meeting_id. Try to flush the session first or assign the Offering to the meeting instead."
            )
        return max_id + 1
