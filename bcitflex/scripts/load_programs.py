"""Script to load programs from JSON file into database."""
import json
from typing import Sequence

from sqlalchemy import delete
from sqlalchemy.orm import Session

from bcitflex.model import Course
from bcitflex.model.program import Program


def lowercase_keys(data: dict | list) -> dict | list:
    """Convert keys to lowercase."""
    if isinstance(data, dict):
        return {key.lower(): lowercase_keys(value) for key, value in data.items()}

    if isinstance(data, list):
        return [lowercase_keys(item) for item in data]

    return data


def extract_programs(filename: str) -> list[dict]:
    """Extract programs from JSON file."""
    with open(filename, "r") as file:
        return lowercase_keys(json.load(file)["Programs"])


def filter_programs(courses: Sequence[Course], programs: list[dict]) -> list[dict]:
    """Filter to list of programs with courses in the database."""

    # Create dictionary of courses by fullcode
    course_dict = {course.fullcode.replace(" ", ""): course for course in courses}

    # Filter to programs with courses in the database and add courses
    filtered_programs = []
    for program in programs:
        program["courses"] = [
            course_dict[course_id]
            for course_id in program["courses"]
            if course_id in course_dict.keys()
        ]
        if program["courses"]:
            filtered_programs.append(program)

    return filtered_programs


def delete_and_load_programs(session: Session, programs: list[dict]) -> int:
    """Delete existing programs and load new programs rolling back in case of error."""

    try:
        # delete existing programs
        session.execute(delete(Program))

        # add programs
        session.add_all(Program(**program) for program in programs)

        session.commit()

    except Exception as exc:
        session.rollback()
        session.close()
        raise exc

    return len(programs)
