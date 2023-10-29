"""User model declaration."""

from sqlalchemy import ForeignKey, Sequence
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String, Text

from . import Base, MappedAsDataclass
from .base import TimestampsMixin

user_id_seq = Sequence("user_id_seq")
user_preference_id_seq = Sequence("user_preference_id_seq")


class UserPreference(Base):
    __tablename__ = "user_preference"
    __table_args__ = {"comment": "User preferences."}

    id: Mapped[Integer] = mapped_column(
        Integer,
        primary_key=True,
        doc="User preference ID",
        comment="Serial user preference ID.",
        server_default=user_preference_id_seq.next_value(),
    )
    user_id: Mapped[Integer] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        doc="User ID",
        comment="User ID.",
    )
    programs: Mapped[ARRAY] = mapped_column(
        MutableList.as_mutable(ARRAY(Integer)),
        doc="User selected program ids",
        comment="User selected program ids.",
        server_default="{}",
    )

    def __repr__(self):
        return f"UserPreference(id={self.id})"


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

    preference: Mapped["UserPreference"] = relationship(
        "UserPreference", default_factory=UserPreference, cascade="all, delete-orphan"
    )


UserPreference.__mapper__.add_property(
    "user", relationship(User, back_populates="preference")
)
