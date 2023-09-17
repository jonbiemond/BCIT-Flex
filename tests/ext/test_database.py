from sqlalchemy import select
from sqlalchemy.orm import Session

from bcitflex.model import Course, Offering, User
from tests import dbtest


@dbtest
class TestSoftDeleteDB:
    """Test the SoftDelete extension with the database."""

    def test_select(self, session: Session):
        """Test that the event hook intercepts a select statement."""

        user_ct = len(session.scalars(select(User)).all())

        # add deleted user to database
        deleted_user = User(username="test", password="test")
        deleted_user.deleted_at = "2021-01-01"
        session.add(deleted_user)
        session.commit()

        # assert we are excluding soft-deleted objects
        assert len(session.scalars(select(User)).all()) == user_ct

    def test_load_children(self, session: Session, new_offering: Offering):
        """Test that the select hook also applies to loading children."""

        # add deleted offering to database
        deleted_offering = new_offering
        deleted_offering.deleted_at = "2021-01-01"
        course_id = deleted_offering.course_id
        session.add(deleted_offering)
        session.commit()

        # assert soft-deleted objects are not loaded
        assert deleted_offering not in session.get(Course, course_id).offerings

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
