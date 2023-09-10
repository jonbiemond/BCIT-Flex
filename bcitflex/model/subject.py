"""Subject model declaration."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean, String

from . import Base

if TYPE_CHECKING:
    from . import Course


class Subject(Base):
    __tablename__ = "subject"
    __table_args__ = {"comment": "Subjects."}

    subject_id: Mapped[String] = mapped_column(
        String(4),
        primary_key=True,
        doc="Subject ID",
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
        back_populates="subject", cascade="all, delete-orphan", passive_deletes=True
    )

    def __repr__(self):
        return f"Subject(subject={self.subject_id})"

    def get_course(self, course_code: str) -> Course:
        """Get a course by the course code."""
        return next(
            (course for course in self.courses if course.code == course_code), None
        )
