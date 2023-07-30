"""Course Offering and Meeting declarations."""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import NUMERIC, Integer

from . import Base

if TYPE_CHECKING:
    from . import Course


class Offering(Base):
    __tablename__ = "offering"
    __table_args__ = {"comment": "Course offerings."}

    crn: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        doc="Course Reference Number",
        comment="Course Reference Number, unique to offering.",
    )
    instructor: Mapped[str] = mapped_column(
        String(30), doc="Instructor", comment="Instructor."
    )
    price: Mapped[float] = mapped_column(NUMERIC, doc="Price", comment="Price.")
    duration: Mapped[str] = mapped_column(
        String(30), doc="Duration Weeks", comment="Duration in weeks."
    )
    status: Mapped[str] = mapped_column(
        String(30), doc="Status", comment="Status of course offering."
    )
    course_id: Mapped[int] = mapped_column(ForeignKey("course.course_id"))

    course: Mapped["Course"] = relationship(back_populates="offerings")

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
