from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from bcitflex.model import Course, Offering, User
from tests import dbtest


@dbtest
class TestSoftDeleteDB:
    """Test the SoftDelete extension with the database."""

    def test_select(self, db_session: Session):
        """Test that the event hook intercepts a select statement."""

        user_ct = len(db_session.scalars(select(User)).all())

        # add deleted user to database
        deleted_user = User(username="test", password="test")
        deleted_user.deleted_at = "2021-01-01"
        db_session.add(deleted_user)
        db_session.commit()

        # assert we are excluding soft-deleted objects
        assert len(db_session.scalars(select(User)).all()) == user_ct

    def test_load_children(self, db_session: Session, new_offering: Offering):
        """Test that the select hook also applies to loading children."""

        # add deleted offering to database
        deleted_offering = new_offering
        deleted_offering.deleted_at = "2021-01-01"
        course_id = deleted_offering.course_id
        db_session.add(deleted_offering)
        db_session.commit()

        # assert soft-deleted objects are not loaded
        assert deleted_offering not in db_session.get(Course, course_id).offerings

    def test_include_option(self, db_session: Session):
        """Test that the include_deleted option includes deleted objects."""
        # Note: this test depends on the prior test (test_hook) for efficiency
        user_ct = len(db_session.scalars(select(User)).all())
        all_users = db_session.scalars(
            select(User).execution_options(include_deleted=True)
        ).all()
        assert len(all_users) == user_ct + 1

    def test_include_option_get(self, db_session: Session):
        """Test that the include_deleted option includes deleted objects when used with get."""

        # add deleted user to database
        deleted_user = User(username="deleted", password="test")
        deleted_user.deleted_at = "2021-01-01"
        db_session.add(deleted_user)
        db_session.commit()
        user_id = deleted_user.id

        # remove deleted user from identity map
        db_session.expunge_all()

        assert db_session.get(User, user_id) is None
        assert (
            db_session.get(User, user_id, execution_options={"include_deleted": True})
            is not None
        )

    def test_unit_of_work_delete(self, db_session: Session):
        """Test that the event hook intercepts a delete statement."""

        user = db_session.get(User, 1)
        db_session.delete(user)
        db_session.commit()

        # assert the user is soft-deleted
        assert db_session.get(User, 1) is None

    def test_execute_delete(self, db_session: Session):
        """Test that the event hook intercepts a delete statement."""

        db_session.execute(delete(User).where(User.id == 1))

        # assert the user is soft-deleted
        assert (
            db_session.scalar(
                select(User.deleted_at)
                .where(User.id == 1)
                .execution_options(include_deleted=True)
            )
            is not None
        )

    def test_relationship_delete(self, db_session: Session):
        """Test that the event hook intercepts delete statements emitted by a relationship change."""

        course = db_session.get(Course, 1)
        crn = course.offerings[0].crn
        course.offerings.remove(course.offerings[0])
        db_session.commit()

        # assert the offering is soft-deleted
        assert (
            db_session.scalar(
                select(Offering.deleted_at)
                .where(Offering.crn == crn)
                .execution_options(include_deleted=True)
            )
            is not None
        )

    def test_merge_delete(self, db_session: Session, new_course: Course):
        """Test that the event hook intercepts delete statements emitted during a merge."""

        # assert the offering is not soft-deleted, because tests aren't independent
        offering = db_session.execute(
            select(Offering)
            .where(Offering.crn == "12345")
            .execution_options(include_deleted=True)
        ).scalar()
        offering.deleted_at = None
        db_session.commit()
        assert (
            db_session.scalar(
                select(Offering.deleted_at)
                .where(Offering.crn == "12345")
                .execution_options(include_deleted=True)
            )
            is None
        )

        new_course.subject_id = "COMP"
        new_course.code = "1234"
        new_course.course_id = 1
        new_course.offerings = []
        db_session.merge(new_course)
        db_session.commit()

        # assert the offering is soft-deleted
        assert (
            db_session.scalar(
                select(Offering.deleted_at)
                .where(Offering.crn == "12345")
                .execution_options(include_deleted=True)
            )
            is not None
        )

    def test_merge_deleted_object(self, db_session: Session, new_course: Course):
        """Test that a deleted object can be merged and is marked as not deleted."""

        # soft delete course
        course = db_session.get(Course, 1)
        db_session.delete(course)
        db_session.commit()

        # confirm course is soft-deleted
        assert db_session.get(Course, 1) is None

        # merge new course
        new_course.course_id = 1
        # add deleted course to the identity map
        _ = db_session.get(Course, 1, execution_options={"include_deleted": True})
        new_course.deleted_at = None
        db_session.merge(new_course)
        db_session.commit()

        # confirm course is not soft-deleted
        assert db_session.get(Course, 1).deleted_at is None

    def test_cascade_delete(self, db_session: Session, new_offering: Offering):
        """Test that the event hook intercepts delete statements cascaded to foreign keys."""

        # add new_offering to the database
        new_offering.crn = "54321"
        course = db_session.get(Course, 1)
        course.offerings.append(new_offering)
        db_session.commit()

        assert (crn := course.offerings[0].crn) is not None

        db_session.delete(course)
        db_session.commit()

        # assert the offering is soft-deleted
        assert (
            db_session.scalar(
                select(Offering.deleted_at)
                .where(Offering.crn == crn)
                .execution_options(include_deleted=True)
            )
            is not None
        )
