"""Course model declaration."""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Sequence, UniqueConstraint
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy.types import REAL, Integer, String, Text

from . import Base
from .base import TimestampsMixin
from .subject import Subject

if TYPE_CHECKING:
    from . import Offering


course_id_seq = Sequence("course_course_id_seq")


class Course(TimestampsMixin, Base):
    __tablename__ = "course"
    __table_args__ = (
        UniqueConstraint("subject_id", "code"),
        {"comment": "Courses."},
    )

    course_id: Mapped[Integer] = mapped_column(
        Integer,
        primary_key=True,
        doc="Course ID",
        comment="Serial course ID.",
        server_default=course_id_seq.next_value(),
    )
    subject_id: Mapped[String] = mapped_column(
        ForeignKey("subject.subject_id", ondelete="CASCADE")
    )
    code: Mapped[String] = mapped_column(
        String(4),
        doc="Course Code",
        comment="Course code.",
    )
    name: Mapped[String] = mapped_column(
        String(100),
        doc="Course Name",
        comment="Course name.",
    )
    prerequisites: Mapped[Text] = mapped_column(
        Text,
        doc="Prerequisites",
        comment="Prerequisites as strings.",
    )
    credits: Mapped[REAL] = mapped_column(
        REAL(2),
        doc="Credits",
        comment="Credit hours.",
    )
    url: Mapped[String] = mapped_column(
        String(2083),
        doc="URL",
        comment="BCIT Course URL.",
    )

    subject: Mapped["Subject"] = relationship(back_populates="courses")

    offerings: Mapped[list["Offering"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
        # Let the database handle cascades for unloaded children
        passive_deletes=True,
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

    def to_string(self) -> str:
        """Return string representation of the course and it's offerings."""
        strings = [self.__str__()]
        strings += [offering.to_string() for offering in self.offerings]
        return "\n\n".join(strings)

    @property
    def last_updated(self) -> str:
        """Return a formatted string of the last_updated timestamp."""
        return self.updated_at.isoformat()

    def set_id(self, session: Session) -> None:
        """Get the course_id from the database if it exists."""
        course = self.get_by_unique(session, (self.subject_id, self.code))
        self.course_id = course.course_id if course else None
