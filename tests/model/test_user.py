"""Tests for the User model."""
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from bcitflex.model import User
from tests import dbtest


class TestUser:
    """Test the User class."""

    def test_init(self, new_user: User):
        """Test the constructor."""
        assert new_user.id is None
        assert new_user.password == "test"

    def test_repr(self, new_user: User):
        """Test the repr method."""
        assert repr(new_user).startswith("<User(id=None,")


@dbtest
class TestUserDb:
    """Test the User class with a database session."""

    def test_save(self, new_user: User, session: Session):
        """Test the save method."""
        session.add(new_user)
        session.commit()
        assert new_user.id == 2

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
