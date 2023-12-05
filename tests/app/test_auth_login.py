import pytest
from flask import g

from bcitflex import create_app
from bcitflex.auth import login_required


@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    # Tu môžete pridať ďalšie nastavenia pre testovanie, napríklad konfiguráciu databázy
    return app


def mock_view():
    return "mock_view_response"


def test_login_required_with_user_logged_in(monkeypatch, app):
    """Test login_required decorator when the user is logged in."""
    with app.test_request_context():
        # Set up a mock user
        g.user = "mock_user"

        # Apply the decorator to the mock view
        decorated_view = login_required(mock_view)

        # Call the decorated view
        response = decorated_view()

        # Check that the response is from the mock_view
        assert response == "mock_view_response"
