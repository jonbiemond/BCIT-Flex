"""Batch model declaration."""
from sqlalchemy import TIMESTAMP, Integer, Sequence
from sqlalchemy.orm import Mapped, mapped_column

from bcitflex.model import Base

batch_process_id_seq = Sequence("batch_process_id_seq")


class BatchProcess(Base):
    """Batch Process model.

    Course response processing record.
    """

    __tablename__ = "batch_process"
    __table_args__ = {"comment": "Batch process records."}

    id: Mapped[Integer] = mapped_column(
        Integer,
        primary_key=True,
        doc="Batch Process ID",
        comment="Serial batch process ID.",
        server_default=batch_process_id_seq.next_value(),
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, server_default="now()", nullable=False
    )
