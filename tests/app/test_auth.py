import pytest
from flask import g, session

from bcitflex.db import DBSession
from bcitflex.model import User
from tests import dbtest


@dbtest
def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post("/auth/register", data={"username": "a", "password": "a"})
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert User.get_by_unique(DBSession(), "a") is not None


@dbtest
@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("a", "", b"Password is required."),
        ("test-user", "test", b"already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert message in response.data


@dbtest
def test_login(client, auth):
    """Test that login view sets the session and redirects to index."""
    assert client.get("/auth/login").status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get("/")
        assert session.get("user_id") == 1
        assert g.user["username"] == "test-user"


@dbtest
@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("a", "test", b"Incorrect username."),
        ("test-user", "a", b"Incorrect password."),
    ),
)
def test_login_validate_input(auth, username, password, message):
    """Test that login view validates the username and password."""
    response = auth.login(username, password)
    assert message in response.data


@dbtest
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
