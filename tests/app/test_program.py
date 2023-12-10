"""Test the program blueprint."""
from flask import Flask, session
from flask.testing import FlaskClient

from bcitflex.db import DBSession
from bcitflex.model import User
from tests import dbtest
from tests.conftest import AuthActions


@dbtest
def test_index(client):
    """Test that index page loads list of programs."""
    response = client.get("/programs")
    assert b"Programs" in response.data


@dbtest
class TestProgram:
    """Test the show page for a program."""

    def test_show(self, client):
        """Test that the show page loads the program."""
        response = client.get("/programs/1")
        assert b"Computer Systems Technology (CST)" in response.data

    def test_show_invalid_program_id_format(self, client):
        response = client.get("/programs/invalid_id")
        assert response.status_code == 404

    def test_select_no_login(self, client):
        """Test that selecting a program adds it to the session."""
        with client:
            response = client.post("/programs/1", data={"favourite": "true"})
            assert session["programs"] == [1]
        assert (
            b'<input type="checkbox" name="favourite" value="true" checked>'
            in response.data
        )

    def test_deselect_no_login(self, client: FlaskClient):
        """Test that deselecting a program removes it from the session."""
        with client.session_transaction() as session:
            session["programs"] = [1]

        response = client.post("/programs/1", data={})
        assert (
            b'<input type="checkbox" name="favourite" value="true" >' in response.data
        )

    def test_deselect_persist(self, client: FlaskClient):
        """Test that deselecting a program removes it from the session permanently."""
        with client:
            response = client.post("/programs/1", data={"favourite": "true"})
            assert session["programs"] == [1]
            assert (
                b'<input type="checkbox" name="favourite" value="true" checked>'
                in response.data
            )

            response = client.post("/programs/1", data={})
            assert session["programs"] == []
            assert (
                b'<input type="checkbox" name="favourite" value="true" >'
                in response.data
            )

            response = client.get("/programs/1")
            assert (
                b'<input type="checkbox" name="favourite" value="true" >'
                in response.data
            )

    def test_favourite_login(self, client: FlaskClient, auth: AuthActions, app: Flask):
        """Test that the selecting a program adds it to the session."""
        auth.login()

        with client:
            client.post("/programs/4", data={"favourite": "true"})
            assert session["programs"][-1] == 4
            assert DBSession.get(User, 1).preference.programs[-1] == 4

    def test_deselect_login(self, client: FlaskClient, auth: AuthActions, app: Flask):
        """Test that the selecting a program adds it to the session."""
        auth.login()
        with client:
            client.post("/programs/3", data={})
            assert DBSession.get(User, 1).preference.programs[-1] != 3
            assert session["programs"][-1] != 3
