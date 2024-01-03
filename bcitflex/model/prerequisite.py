"""Prerequisite model declaration."""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Sequence, UniqueConstraint, func, select
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String

from . import Base

if TYPE_CHECKING:
    from . import Course

and_prereq_id_seq = Sequence("prereq_and_id_seq")
or_prereq_id_seq = Sequence("prereq_or_id_seq")


def nssequence(context: DefaultExecutionContext):
    course_id = context.get_current_parameters()["course_id"]
    stmt = select(func.max(PrerequisiteAnd.prereq_no)).where(
        PrerequisiteAnd.course_id == course_id
    )
    max_id = context.connection.scalar(stmt)
    return max_id + 1 if max_id else 1


class PrerequisiteAnd(Base):
    """All prerequisites that must be met for a course.

    :ivar id: AND Prerequisite ID
    :ivar course_id: Parent course ID
    :ivar prereq_no: Serial ID partitioned by course_id.
    :ivar course: Parent course, for which this is a prerequisite.
    :ivar courses: Child courses, one of which must be fulfilled.
    :ivar children: Child OR prerequisites."""

    __tablename__ = "prereq_and"
    __table_args__ = (
        UniqueConstraint("course_id", "prereq_no"),
        {"comment": "All prerequisites that must be met for a course."},
    )

    id: Mapped[Integer] = mapped_column(
        Integer,
        primary_key=True,
        doc="AND Prerequisite ID",
        comment="Serial prerequisite_and ID.",
        server_default=and_prereq_id_seq.next_value(),
    )
    course_id: Mapped[Integer] = mapped_column(
        ForeignKey("course.course_id", ondelete="CASCADE"),
        doc="Parent course ID",
        comment="Parent course ID for which this is a prerequisite.",
    )
    prereq_no: Mapped[Integer] = mapped_column(
        Integer,
        doc="Prerequisite number",
        comment="Serial prerequisite_and ID partitioned by course_id.",
        default=nssequence,
    )

    course: Mapped["Course"] = relationship(back_populates="prerequisites")
    children: Mapped[list["PrerequisiteOr"]] = relationship(
        back_populates="parent", cascade="all"
    )

    def __repr__(self) -> str:
        return f"<PrerequisiteAnd {self.id}>"


class PrerequisiteOr(Base):
    """One of possibly multiple prerequisites that must be met for a course.

    :ivar id: OR Prerequisite ID
    :ivar prereq_and_id: Parent AND prerequisite ID
    :ivar course_id: Child course ID
    :ivar criteria: Criteria for prerequisite
    :ivar course: Child course, one of which must be fulfilled.
    :ivar parent: Parent AND prerequisite, for which this is a child."""

    __tablename__ = "prereq_or"
    __table_args__ = (
        UniqueConstraint("prereq_and_id", "course_id"),
        {"comment": "At least one prerequisite per prereq_and_id must be met."},
    )

    id: Mapped[Integer] = mapped_column(
        Integer,
        primary_key=True,
        doc="OR Prerequisite ID",
        comment="Serial prerequisite_or ID.",
        server_default=or_prereq_id_seq.next_value(),
    )
    prereq_and_id: Mapped[Integer] = mapped_column(
        ForeignKey("prereq_and.id", ondelete="CASCADE")
    )
    course_id: Mapped[Integer] = mapped_column(ForeignKey("course.course_id"))
    criteria: Mapped[String | None] = mapped_column(
        String(100),
        doc="Criteria",
        comment="Criteria for prerequisite.",
    )

    course: Mapped["Course"] = relationship(back_populates="prerequisites_of")
    parent: Mapped["PrerequisiteAnd"] = relationship(back_populates="children")

    def __repr__(self) -> str:
        return f"<PrerequisiteOr {self.id}>"
