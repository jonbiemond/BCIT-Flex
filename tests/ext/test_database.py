from sqlalchemy import select
from sqlalchemy.orm import Session

from bcitflex.ext.database import rewrite_statement
from bcitflex.model import User
from tests import dbtest


class TestSoftDelete:
    """Test the SoftDelete extension."""

    def test_select_scalars(self):
        """Test selecting objects rewrites the statement."""
        stmt = select(User)
        stmt = rewrite_statement(stmt)

        # if we don't have a where clause, we can't be filtering for soft-deleted
        assert stmt.whereclause is not None

        # assert we are excluding soft-deleted objects
        assert stmt.whereclause.compare(User.deleted_at.is_(None))


@dbtest
class TestSoftDeleteDB:
    """Test the SoftDelete extension with the database."""

    def test_hook(self, session: Session):
        """Test event listener intercepts statement."""

        user_ct = len(session.scalars(select(User)).all())

        # add deleted user to database
        deleted_user = User(username="test", password="test")
        deleted_user.deleted_at = "2021-01-01"
        session.add(deleted_user)
        session.commit()

        # assert we are excluding soft-deleted objects
        assert len(session.scalars(select(User)).all()) == user_ct

    def test_include_option(self, session: Session):
        """Test that the include_deleted option includes deleted objects."""
        # Note: this test depends on the prior test (test_hook) for efficiency
        user_ct = len(session.scalars(select(User)).all())
        assert (
            len(
                session.scalars(
                    select(User).execution_options(include_deleted=True)
                ).all()
            )
            == user_ct + 1
        )
