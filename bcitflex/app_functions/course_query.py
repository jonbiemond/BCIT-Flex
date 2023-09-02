"""Filter courses."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from bcitflex.model import Course


def filter_courses(
    session: Session,
    subject: str | None = None,
    course_code: str | None = None,
    available: bool | None = None,
) -> list[Course]:
    """Return a list of courses that match the given criteria."""
    # Create a list of filters to apply to the query
    joins = []
    filters = []

    if subject:
        filters.append(Course.subject_id == subject)
    if course_code:
        filters.append(Course.code == course_code)

    # Apply the filters to the query
    query = select(Course)
    for join in joins:
        query.join(join)
    query = query.where(*filters)

    # Execute the query
    courses = session.scalars(query).all()

    # Apply object filters
    if available:
        courses = [course for course in courses if course.is_available]

    return courses
