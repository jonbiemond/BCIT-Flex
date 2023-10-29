"""Tests for the User model."""
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from bcitflex.model import Program, User, UserPreference
from tests import dbtest


class TestUser:
    """Test the User class."""

    def test_init(self, new_user: User):
        """Test the constructor."""
        assert new_user.id is None
        assert new_user.password == "test"

    def test_repr(self, new_user: User):
        """Test the repr method."""
        assert repr(new_user).startswith("User(id=None,")

    def test_user_is_subscriptable(self, new_user: User):
        """Test the subscript operator."""
        assert new_user["password"] == "test"

    def test_user_preference_is_not_none(self, new_user: User):
        """Test that the user preference property is not None."""
        assert new_user.preference is not None


class TestUserPreference:
    """Test the UserPreference class."""

    def test_init(self, new_user_preference: UserPreference):
        """Test the constructor."""
        assert new_user_preference.id is None
        assert new_user_preference.programs == [1, 2, 3]


@dbtest
class TestUserDB:
    """Test the User class with a database session."""

    def test_save(self, new_user: User, session: Session):
        """Test the save method."""
        session.add(new_user)
        session.commit()
        assert new_user.id is not None

    def test_integrity_error(self, session: Session):
        """Test that the database rejects duplicate usernames."""
        session.add(User(username="test", password="test"))
        session.commit()
        with pytest.raises(IntegrityError):
            with session.begin():
                session.add(User(username="test", password="test"))

    def test_hash_password(self, new_user: User, session: Session):
        """Test database accepts hashed password."""
        new_user.password = generate_password_hash("test")
        session.add(new_user)
        session.commit()
        assert new_user.password != "test"

    def test_user_preference(self, session: Session):
        """Test the user preference relationship."""
        user = session.execute(select(User)).scalar()
        assert user.preference is not None
        assert user.preference.user_id == user.id
        assert user.preference.programs == [1, 2, 3]

    def test_user_preference_programs(self, session: Session):
        """Test selecting programs by user preference."""
        user = session.execute(select(User)).scalar()
        programs = session.scalars(
            select(Program).where(Program.program_id.in_(user.preference.programs))
        ).all()
        assert len(programs) > 0

    def test_user_preference_is_not_none(self, session: Session):
        """Test that the user has a row in the user_preference table."""
        new_user = User(username="no_preference", password="test")
        session.add(new_user)
        session.commit()

        new_user = User.get_by_unique(session, "no_preference")
        assert new_user.preference is not None
