"""Test for the load_programs.py script."""
import os.path
from unittest.mock import MagicMock

import pytest
from flask import Flask
from flask.testing import FlaskCliRunner
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bcitflex.model import Course
from bcitflex.model.program import Program
from bcitflex.scripts.load_programs import (
    delete_and_load_programs,
    extract_programs,
    filter_programs,
    lowercase_keys,
)
from tests import dbtest


@pytest.fixture
def programs():
    """Mock programs data."""
    return [
        {
            "name": "Small Business Management",
            "credential": "Certificate",
            "url": "https://www.bcit.ca/study/programs/6405acert",
            "courses": ["TEST1234"],
        },
        {
            "name": "Big Business Management",
            "credential": "Diploma",
            "url": "https://www.bcit.ca/study/programs/6405acert",
            "courses": ["TEST9999"],
        },
    ]


class TestExtractPrograms:
    """Test reading programs from JSON file."""

    def test_lowercase_keys(self):
        """Test converting keys to lowercase."""
        data = {"Key1": "Value1", "Key2": {"Key3": "Value3"}}
        expected = {"key1": "Value1", "key2": {"key3": "Value3"}}
        assert lowercase_keys(data) == expected

    def test_extract_programs(self):
        """Test extracting programs from JSON file."""
        expected_name = "Small Business Management"
        expected_courses = [
            "BUSA2205",
            "FMGT1152",
            "HRMG3105",
            "MKTG1102",
            "MKTG1324",
            "OPMT1187",
        ]
        test_dir = os.path.dirname(os.path.dirname(__file__))
        filename = os.path.join(test_dir, "test_data", "programs.json")
        programs = extract_programs(filename)
        program = programs[0]
        assert program["name"] == expected_name
        assert program["courses"] == expected_courses

    def test_filter_programs(self, programs: list[dict]):
        """Test filtering programs to those with courses in the database."""
        course = Course(subject_id="TEST", code="1234", name="Test Course")
        assert len(filter_programs([course], programs)) == 1


@dbtest
class TestProgramsDB:
    """Test loading programs into the database."""

    def test_delete_and_load_programs(self, session: Session, programs: list[dict]):
        """Test deleting and loading programs."""

        assert len(session.execute(select(Program)).scalars().all()) == 1

        # remove courses from programs
        for program in programs:
            program.pop("courses")

        delete_and_load_programs(session, programs)
        db_programs = session.execute(select(Program)).scalars().all()
        assert len(db_programs) == 2

    def test_delete_and_load_programs_rollback(
        self, session: Session, programs: list[dict], monkeypatch
    ):
        """Test deleting and loading programs with rollback."""

        program_ct = len(session.execute(select(Program)).scalars().all())

        # remove courses from programs and force integrity error
        for program in programs:
            program.pop("courses")
            program["program_id"] = 1

        with pytest.raises(IntegrityError):
            delete_and_load_programs(session, programs)

        # confirm programs were not removed or added
        db_programs = session.execute(select(Program)).scalars().all()
        assert len(db_programs) == program_ct


@dbtest
class TestLoadProgramsCLI:
    """Test load-programs CLI command."""

    def test_load_programs(
        self, app: Flask, runner: FlaskCliRunner, programs: list[dict], monkeypatch
    ):
        """Test load-programs CLI command."""

        # mock extract_programs
        monkeypatch.setattr(
            "bcitflex.db.extract_programs", MagicMock(return_value=programs)
        )

        # mock delete_and_load_programs
        mock_delete_and_load_programs = MagicMock(return_value=2)
        monkeypatch.setattr(
            "bcitflex.db.delete_and_load_programs", mock_delete_and_load_programs
        )

        # run command
        with app.app_context():
            result = runner.invoke(args=["load-programs"])

        # assert command ran successfully
        assert result.exit_code == 0
        assert mock_delete_and_load_programs.called
        assert "Loaded 2 programs into database." in result.output
