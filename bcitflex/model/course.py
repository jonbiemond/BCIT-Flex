"""Course model declaration."""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Float

from . import Base
from .subject import Subject

if TYPE_CHECKING:
    from . import Offering


class Course(Base):
    __tablename__ = "course"
    __table_args__ = {"comment": "Courses."}

    course_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, doc="Course ID", comment="Serial course ID."
    )
    subject_id: Mapped[str] = mapped_column(ForeignKey("subject.subject_id"))
    code: Mapped[str] = mapped_column(
        String(4),
        doc="Course Code",
        comment="Course code.",
    )
    name: Mapped[str] = mapped_column(
        String(100),
        doc="Course Name",
        comment="Course name.",
    )
    prerequisites: Mapped[str] = mapped_column(
        String(100),
        doc="Prerequisites",
        comment="Prerequisites as strings.",
    )
    credits: Mapped[float] = mapped_column(
        Float(2),
        doc="Credits",
        comment="Credit hours.",
    )
    url: Mapped[str] = mapped_column(
        String(100),
        doc="URL",
        comment="URL.",
    )

    subject: Mapped["Subject"] = relationship(back_populates="courses")

    offerings: Mapped[list["Offering"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Course(course={self.fullcode}, name={self.name})"

    def __str__(self):
        course_str = (
            f"Course: {self.fullcode}\n"
            f"Name: {self.name}\n"
            f"Prerequisites: {self.prerequisites}\n"
            f"Credits: {self.credits}\n"
            f"URL: {self.url}\n"
        )
        return course_str

    @property
    def fullcode(self) -> str:
        """Concat of subject_id and course_code."""
        return f"{self.subject_id} {self.code}"

    def offering_count(self, available_only=False) -> int:
        """Return count of course offerings."""
        if available_only:
            return sum([offering.available for offering in self.offerings])
        return len(self.offerings)

    @property
    def is_available(self) -> bool:
        """Return True if at least one offering is available."""
        return self.offering_count(available_only=True) > 0
