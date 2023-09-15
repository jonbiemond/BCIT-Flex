"""Offering Term declaration."""
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String

from . import Base

if TYPE_CHECKING:
    from . import Offering


class Term(Base):
    __tablename__ = "term"
    __table_args__ = {"comment": "Offering terms."}

    term_id: Mapped[String] = mapped_column(
        String(6),
        primary_key=True,
        doc="Term ID, used in HTML DIV",
        comment="Term ID.",
        server_default=None,
    )
    year: Mapped[Integer] = mapped_column(
        Integer, doc="Term year", comment="Term year."
    )
    season: Mapped[String] = mapped_column(
        String(20), doc="Term season", comment="Term season."
    )

    offerings: Mapped["Offering"] = relationship(
        back_populates="term", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Term({self.term_id})"
