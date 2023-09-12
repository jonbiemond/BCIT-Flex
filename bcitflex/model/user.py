"""User model declaration."""

from sqlalchemy import Sequence
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, String, Text

from . import Base, MappedAsDataclass
from .base import TimestampsMixin

user_id_seq = Sequence("user_id_seq")


class User(MappedAsDataclass, TimestampsMixin, Base):
    __tablename__ = "user"
    __table_args__ = {"comment": "Users."}

    id: Mapped[Integer] = mapped_column(
        Integer,
        primary_key=True,
        doc="User ID",
        comment="Serial user ID.",
        server_default=user_id_seq.next_value(),
        init=False,
        repr=True,
    )
    username: Mapped[String] = mapped_column(
        String(20), doc="Username", comment="Username.", unique=True, repr=True
    )
    password: Mapped[Text] = mapped_column(
        Text, doc="Password", comment="Hashed password.", repr=False
    )
