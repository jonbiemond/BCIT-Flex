"""Course model declaration."""
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Float

from . import Base

if TYPE_CHECKING:
    from . import Offering


class Course(Base):
    __tablename__ = "course"
    __table_args__ = {"comment": "Courses."}

    course_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, doc="Course ID", comment="Serial course ID."
    )
    subject_id: Mapped[str] = mapped_column(
        doc="Subject",
        comment="Subject code, e.g. COMP.",
    )
    code: Mapped[str] = mapped_column(
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
        return f"{self.subject_id} {self.code}"
