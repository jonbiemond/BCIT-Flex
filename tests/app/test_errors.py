"""Test the errors blueprint."""
import pytest

from bcitflex import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for test."""
    app = create_app()
    yield app


def test_error_page(client):
    """Test that the 404 error page loads."""
    response = client.get("/nonexistent-url")

    assert response.status_code == 404
    assert b"Page Not Found - BCIT" in response.data
