"""Subject model declaration."""
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from . import Course


class Subject(Base):
    __tablename__ = "subject"
    __table_args__ = {"comment": "Subjects."}

    subject_id: Mapped[str] = mapped_column(
        String(4),
        primary_key=True,
        doc="Subject ID",
        comment="Subject code, e.g. COMP.",
    )
    name: Mapped[str | None] = mapped_column(
        String(100),
        doc="Subject Name",
        comment="Subject name.",
    )

    courses: Mapped[list["Course"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Subject(subject={self.subject_id})"
