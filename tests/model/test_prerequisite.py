"""Test for the prerequisite model."""
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bcitflex.model import Course
from bcitflex.model.prerequisite import PrerequisiteAnd, PrerequisiteOr
from tests import dbtest


@pytest.fixture
def new_prerequisite(
    new_prereq_and: PrerequisiteAnd, new_prereq_or: PrerequisiteOr
) -> PrerequisiteAnd:
    """Return a new prerequisite object."""
    new_prereq_and.children = [new_prereq_or]
    return new_prereq_and


class TestPrerequisite:
    """Test the Prerequisite class."""

    def test_init(
        self, new_prerequisite: PrerequisiteAnd, new_prereq_or: PrerequisiteOr
    ):
        """Test the constructor."""
        assert new_prerequisite.course_id == 1
        assert new_prerequisite.course is None
        assert new_prerequisite.children == [new_prereq_or]

    def test_repr(self, new_prerequisite: PrerequisiteAnd):
        """Test the repr method."""
        new_prerequisite.id = 2
        assert repr(new_prerequisite) == "<PrerequisiteAnd 2>"


@dbtest
class TestPrerequisiteDB:
    """Test the Prerequisite class with a database session."""

    def test_get_prerequisite(self, db_session):
        """Test getting a prerequisite from the db."""
        course = db_session.get(Course, 1)
        prerequisites = course.prerequisites
        assert prerequisites[0].id == 1
        assert prerequisites[0].children[0].course.code == "1000"

    def test_add_prerequisite(self, new_prerequisite, db_session):
        """Test adding a prerequisite to the db."""
        db_session.add(new_prerequisite)
        db_session.commit()
        assert db_session.get(PrerequisiteAnd, 2) == new_prerequisite

    def test_merge(self, db_session: Session):
        """Test merge doesn't create new prerequisite objects."""
        prereq_ct = len(db_session.scalars(select(PrerequisiteAnd)).all())
        new_prereq = db_session.get(PrerequisiteAnd, 1).clone(
            pk_id=None, include_relationships=False
        )
        new_prereq.set_id(db_session)
        db_session.merge(new_prereq)
        db_session.commit()
        assert len(db_session.scalars(select(PrerequisiteAnd)).all()) == prereq_ct

    def test_delete_prerequisite(self, db_session):
        """Test deleting a prerequisite from the db."""
        prereq = db_session.get(PrerequisiteAnd, 1)
        course_id = prereq.children[0].course_id
        db_session.delete(prereq)
        db_session.commit()
        assert db_session.get(PrerequisiteAnd, 1) is None
        assert db_session.get(PrerequisiteOr, 1) is None
        assert db_session.get(Course, course_id) is not None

    @pytest.mark.skip(
        "_soft_delete rule prevents a delete from being emitted and a violation made"
    )
    def test_delete_prerequisite_course_error(self, db_session: Session):
        """Test that deleting a course that is a prerequisite raises an error."""
        course = db_session.get(Course, 1).prerequisites[0].children[0].course
        with pytest.raises(IntegrityError):
            db_session.delete(course)
            db_session.commit()

    def test_delete_prerequisite_course(self, db_session: Session):
        """Test that deleting a course that is a prerequisite deletes the prerequisite.

        A prerequisite should be deleted before deleting a course.
        But this is not enforceable while using soft-deletes."""
        course = db_session.get(Course, 1).prerequisites[0].children[0].course
        db_session.delete(course)
        db_session.commit()
        assert db_session.get(PrerequisiteOr, 1) is None
