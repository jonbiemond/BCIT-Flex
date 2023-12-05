"""Test the app db connection."""
from unittest.mock import MagicMock, mock_open, patch

import psycopg2
import pytest
from flask import Flask
from flask.testing import FlaskCliRunner
from sqlalchemy import text

from bcitflex import create_app
from bcitflex.db import DBSession, config_db_url, create_db, db_connection_factory
from tests import dbtest


class TestDBHelpers:
    """Test helper functions"""

    def test_db_connection_factory(self):
        """Test db connection factory returns a function."""
        db_connection = db_connection_factory()
        assert callable(db_connection)

    def test_db_connection(self, monkeypatch):
        """Test db connection returns a connection."""

        # mock psycopg2.connect so postgres is not required
        class MockConnection:
            def __init__(self):
                self.autocommit = True

        mock_connect = MagicMock(return_value=MockConnection())

        # patch psycopg2.connect()
        monkeypatch.setattr(psycopg2, "connect", mock_connect)

        db_connection = db_connection_factory()
        assert isinstance(db_connection(), MockConnection)

    @pytest.mark.parametrize(
        "db_exists, drop, expected_ddl, assertion",
        [
            (
                    False,
                    False,
                    "SELECT datname FROM pg_database WHERE datname = 'test_db';",
                    True,
            ),
            (False, False, "CREATE DATABASE test_db ENCODING = 'UTF8';", True),
            (True, False, "CREATE DATABASE test_db ENCODING = 'UTF8';", False),
            (True, True, "DROP SCHEMA public CASCADE;CREATE SCHEMA public;", True),
            (False, True, "DROP SCHEMA public CASCADE;CREATE SCHEMA public;", False),
        ],
    )
    def test_create_db(self, monkeypatch, db_exists, drop, expected_ddl, assertion):
        """Test create_db creates a database."""
        emitted_ddl = []

        # mock psycopg2 so postgres is not required
        class MockCursor:
            def execute(self, ddl):
                # split ddl by linefeed, strip, combine, and append to emitted_ddl
                ddl = "".join([line.strip() for line in ddl.split("\n")])
                emitted_ddl.append(ddl)

            def fetchone(self):
                return db_exists or None

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

        class MockConnection:
            def __init__(self):
                self.autocommit = True

            def cursor(self):
                return MockCursor()

        mock_connect = MagicMock(return_value=MockConnection())

        # patch psycopg2.connect()
        monkeypatch.setattr(psycopg2, "connect", mock_connect)

        db_connection = db_connection_factory()
        create_db("test_db", db_connection, drop=drop)
        assert (expected_ddl in emitted_ddl) is assertion

    @dbtest
    @pytest.mark.parametrize(
        "config_exists, read_data, assertion, overwrite, db_password, expected_insert",
        [
            (
                    False,
                    "",
                    True,
                    False,
                    "test_password",
                    'SQLALCHEMY_DATABASE_URI = "postgresql://test_user:test_password@localhost:5432/test_db"\n',
            ),
            (
                    True,
                    "",
                    True,
                    False,
                    "test_password",
                    'SQLALCHEMY_DATABASE_URI = "postgresql://test_user:test_password@localhost:5432/test_db"\n',
            ),
            (
                    True,
                    "SQLALCHEMY_DATABASE_URI = url",
                    False,
                    False,
                    "test_password",
                    'SQLALCHEMY_DATABASE_URI = "postgresql://test_user:test_password@localhost:5432/test_db"\n',
            ),
            (
                    True,
                    "SQLALCHEMY_DATABASE_URI = url",
                    True,
                    True,
                    None,
                    'SQLALCHEMY_DATABASE_URI = "postgresql://test_user@localhost:5432/test_db"\n',
            ),
        ],
    )
    def test_config_db_url(
            self,
            mock_app,
            monkeypatch,
            config_exists,
            read_data,
            assertion,
            overwrite,
            db_password,
            expected_insert,
    ):
        """Test config_db_url writes to config.py."""

        # mock open()
        mo = mock_open(read_data=read_data)
        monkeypatch.setattr("builtins.open", mo)

        # mock Path().exists()
        mock_exists = MagicMock(return_value=config_exists)
        monkeypatch.setattr("pathlib.Path.exists", mock_exists)

        with mock_app.app_context():
            config_db_url(
                "test_db", "test_user", db_password, "localhost", 5432, overwrite
            )
        if assertion:
            mo().write.assert_called_once_with(expected_insert)
        else:
            mo().write.assert_not_called()


class TestDBCommands:
    """Test DB CLI commands."""

    @pytest.mark.parametrize(
        "db_created, db_url, expected",
        [
            (True, "test_url", "Database test_db created."),
            (False, "test_url", "Database test_db already exists."),
            (True, None, "Database url already set in instance\\config.py"),
        ],
    )
    def test_create_db_command(
            self, mock_app, mock_runner, monkeypatch, db_created, db_url, expected
    ):
        # TODO: test more cases
        # mock psycopg2.connect so postgres is not required
        mock_connect = MagicMock()
        monkeypatch.setattr("psycopg2.connect", mock_connect)

        # mock create_db()
        mock_create_db = MagicMock(return_value=db_created)
        monkeypatch.setattr("bcitflex.db.create_db", mock_create_db)

        # mock config_db_url()
        mock_config_db_url = MagicMock(return_value=db_url)
        monkeypatch.setattr("bcitflex.db.config_db_url", mock_config_db_url)

        # set mock_app.instance_path
        mock_app.instance_path = "instance"

        with mock_app.app_context():
            result = mock_runner.invoke(args=["create-db", "--dbname=test_db"])

        assert result.exit_code == 0
        assert expected in result.output

    @pytest.mark.parametrize(
        "role_exists, provided_password, expected_role_creation, expected_password_message, db_url, db_name, db_role",
        [
            (False, "custom_password", True, "custom_password", "textx1", "textx1", "textx1"),
            (True, "known_password", False, "Role test_role already exists", 'testx2', 'testx2', 'testx2'),
        ]
    )
    def test_create_db_command_role_logic(self,
                                          mock_app, mock_runner, monkeypatch,
                                          role_exists, provided_password, expected_role_creation,
                                          expected_password_message, db_url, db_name, db_role
                                          ):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = role_exists
        mock_connection = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        monkeypatch.setattr("psycopg2.connect", MagicMock(return_value=mock_connection))

        def execute_test():
            # mock config_db_url()
            mock_config_db_url = MagicMock(return_value=db_url)
            monkeypatch.setattr("bcitflex.db.config_db_url", mock_config_db_url)

            # set mock_app.instance_path
            mock_app.instance_path = "instance"

            with mock_app.app_context():
                args = ["create-db", "--dbname="+db_name, "--role-name="+db_role]
                if provided_password:
                    args += ["--role-password", provided_password]
                result = mock_runner.invoke(args=args)

            assert result.exit_code == 0
            if expected_role_creation:
                assert f"Role {db_role} created." in result.output
                assert expected_password_message in result.output
            else:
                assert f"Role {db_role} already exists." in result.output

        if provided_password is None:
            with patch("secrets.choice", MagicMock(side_effect="a")):
                execute_test()
        else:
            execute_test()

    @pytest.mark.parametrize(
        "db_exists, expected",
        [
            (True, "Database already up to date."),
            (False, "Database upgraded."),
        ],
    )
    def test_upgrade_db_command(
        self, db_exists, expected, mock_app, mock_runner, monkeypatch
    ):
        """Test upgrade-db command."""

        return True

        # mock SQLAlchemy
        class MockSQLAlchemy:
            def __init__(self, model):
                self.Model = model

        monkeypatch.setattr("bcitflex.db.SQLAlchemy", MockSQLAlchemy)

        # mock check_current_head()
        mock_check_current_head = MagicMock(return_value=db_exists)
        monkeypatch.setattr("bcitflex.db.check_current_head", mock_check_current_head)

        # mock alembic.config.command.upgrade()
        mock_upgrade = MagicMock()
        monkeypatch.setattr("alembic.config.command.upgrade", mock_upgrade)

        with mock_app.app_context():
            result = mock_runner.invoke(args=["upgrade-db"])

        assert result.exit_code == 0
        assert f"{expected}\n" == result.output


@dbtest
class TestDBCommandsDB:
    """Test DB CLI commands with DB connections."""

    def test_load_subjects_command(
            self, app: Flask, runner: FlaskCliRunner, monkeypatch
    ):
        """Test load-subjects command."""

        # mock result.rowcount
        mock_result = MagicMock()
        mock_result.rowcount = 2

        # mock session.execute()
        # [2023-10-21 Jonathan B.]
        #   The mocking here has no effect on the test.
        #   Because I don't know how to mock the context session.
        mock_execute = MagicMock(return_value=mock_result)
        monkeypatch.setattr("bcitflex.db.DBSession.execute", mock_execute)

        # run command
        with app.app_context():
            result = runner.invoke(args=["load-subjects"])

        # assert command ran successfully
        assert result.exit_code == 0
        assert result.output.endswith("subjects into database.\n")


@dbtest
def test_get_close_db(app):
    """Test connection to db is closed after context."""
    with app.app_context():
        db = DBSession()
        assert db is DBSession()

    with pytest.raises(RuntimeError) as e:
        db.execute(text("SELECT 1"))

    assert "Working outside of application context." in str(e.value)


def test_init_app(monkeypatch):
    # mock db.init_app()
    mock_init_app = MagicMock()
    monkeypatch.setattr("bcitflex.db.db.init_app", mock_init_app)

    create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "url"})
    mock_init_app.assert_called_once()
    mock_init_app.reset_mock()

    create_app({"TESTING": True})
    mock_init_app.assert_not_called()

    with pytest.warns(UserWarning):
        create_app({"SQLALCHEMY_DATABASE_URI": None})
