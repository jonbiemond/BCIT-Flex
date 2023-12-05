"""Test the program blueprint."""
from tests import dbtest


@dbtest
def test_index(client):
    response = client.get("/programs")
    assert b"Programs" in response.data


@dbtest
def test_show(client):
    response = client.get("/programs/1")
    assert b"Computer Systems Technology (CST)" in response.data


@dbtest
def test_show_invalid_program_id_format(client):
    response = client.get("/programs/invalid_id")
    assert response.status_code == 404
