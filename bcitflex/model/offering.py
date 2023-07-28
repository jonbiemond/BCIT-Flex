"""Course Offering and Meeting declarations."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import NUMERIC

from . import Base


class Offering(Base):
    __tablename__ = "offering"
    __table_args__ = {"comment": "Course offerings."}

    crn: Mapped[int] = mapped_column(
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

    def __str__(self) -> str:
        info = (
            f"CRN: {self.crn}\n"
            f" Instructor: {self.instructor}\n"
            f" Price: {self.price}\n"
            f" Duration: {self.duration}\n"
            f" Status: {self.status}\n"
        )
        return info
