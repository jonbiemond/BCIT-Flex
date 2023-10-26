"""Test the course blueprint."""
from bs4 import BeautifulSoup

from tests import dbtest


@dbtest
def test_index(client, auth):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    assert b"test-user" in response.data


@dbtest
def test_courses_name_filter(client, auth):
    data = {"name": "Test"}
    response = client.post("/courses", data=data)
    soup = BeautifulSoup(response.data, "html.parser")
    number_rows = len(soup.find_all("tr", id="course_data"))
    assert b"Test Course" in response.data
    assert b"Second Course" not in response.data
    assert number_rows == 1


@dbtest
def test_courses_with_cours(client, auth):
    data = {"name": "cours"}
    response = client.post("/courses", data=data)
    soup = BeautifulSoup(response.data, "html.parser")
    number_rows = len(soup.find_all("tr", id="course_data"))
    assert b"Test Course" in response.data
    assert b"Second Course" in response.data
    assert number_rows == 2
