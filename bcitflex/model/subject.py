"""Subject model declaration."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean, String

from . import Base

if TYPE_CHECKING:
    from . import Course


subject_id_seq = Sequence("subject_id_seq")


class Subject(Base):
    """Subject model.

    :ivar id: Surrogate key.
    :ivar code: Subject code.
    :ivar name: Subject name.
    :ivar is_active: Included in web scraping.
    """

    __tablename__ = "subject"
    __table_args__ = {"comment": "Subjects."}

    id: Mapped[Integer] = mapped_column(
        Integer,
        primary_key=True,
        doc="Subject ID",
        comment="Serial subject ID.",
        server_default=subject_id_seq.next_value(),
    )
    code: Mapped[String] = mapped_column(
        String(4),
        unique=True,
        doc="Subject Code",
        comment="Subject code, e.g. COMP.",
    )
    name: Mapped[String | None] = mapped_column(
        String(100),
        doc="Subject Name",
        comment="Subject name.",
    )
    is_active: Mapped[Boolean | None] = mapped_column(
        Boolean,
        doc="Included in web scraping",
        comment="Whether the subject is included in web scraping.",
    )

    courses: Mapped[list["Course"]] = relationship(
        back_populates="subject", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"Subject({self.id})"

    def __str__(self):
        return f"{self.code}: {self.name}"

    def get_course(self, course_code: str) -> Course:
        """Get a course by the course code."""
        return next(
            (course for course in self.courses if course.code == course_code), None
        )
