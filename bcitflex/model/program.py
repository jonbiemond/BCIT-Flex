"""Program model declaration."""
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Sequence, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String

from . import Base
from .base import TimestampsMixin

if TYPE_CHECKING:
    from . import Course


program_id_seq = Sequence("program_program_id_seq")


program_course_association = Table(
    "program_course_association",
    Base.metadata,
    Column("program_id", Integer, ForeignKey("program.program_id", ondelete="CASCADE")),
    Column("course_id", Integer, ForeignKey("course.course_id", ondelete="CASCADE")),
)


class Program(TimestampsMixin, Base):
    __tablename__ = "program"

    program_id: Mapped[Integer] = mapped_column(
        Integer,
        primary_key=True,
        doc="Program ID",
        comment="Serial program ID.",
        server_default=program_id_seq.next_value(),
    )
    name: Mapped[String] = mapped_column(
        String(100), doc="Program Name", comment="Program Name."
    )
    credential: Mapped[String] = mapped_column(
        String(100), doc="Credential", comment="Program Credential."
    )
    url: Mapped[String] = mapped_column(
        String(2083), doc="URL", comment="BCIT Program URL."
    )

    courses: Mapped[list["Course"]] = relationship(
        secondary=program_course_association,
        back_populates="programs",
    )

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"Program(id={self.program_id}, name={self.name})"
