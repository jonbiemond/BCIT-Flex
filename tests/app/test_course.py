"""Test the course blueprint."""
from tests import dbtest


@dbtest
class TestCourse:
    def test_auth(self, client, auth):
        """Test that the response changes based on authentication."""
        response = client.get("/")
        assert b"Log In" in response.data
        assert b"Register" in response.data

        auth.login()
        response = client.get("/")
        assert b"test-user" in response.data

    def test_index(self, client):
        """Test that index page loads list of courses."""
        response = client.get("/")
        assert b"COMP" in response.data

    def test_filter_courses(self, client):
        """Test that filter courses returns only courses with the given subject."""
        response = client.get("/courses?subject=COMP")
        assert b"COMP" in response.data

    def test_filter_courses_by_code(self, client):
        """Test that filter courses returns only courses with the given code."""
        response = client.get("/courses?code=9999")
        assert b"1234" not in response.data

    def test_filter_courses_by_available(self, client):
        """Test that filter courses returns only courses with the given availability."""
        response = client.get("/courses?available=True")
        assert b"COMP" in response.data

    def test_paginate_courses(self, client):
        """Test that filter courses returns only courses with the given availability."""
        response = client.get("/courses?page=1")
        assert b"Page 1" in response.data

    def test_paginate_courses_and_subject(self, client):
        """Test that filter courses returns only courses with the given availability."""
        response = client.get("/courses?page=1&subject=COMP")
        assert b"Page 1" in response.data
        assert b"COMP" in response.data

    def test_filter_courses_by_campus(self, client):
        """Test that filter courses returns only courses with the given campus."""
        response = client.post("/courses", data={"campus": "Burnaby"})
        assert b"1234" not in response.data
