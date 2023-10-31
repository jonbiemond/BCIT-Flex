"""Test the account blueprint."""
from tests import dbtest


@dbtest
class TestAccount:
    """Test the account blueprint."""

    def test_login_required(self, client):
        response = client.get("/account")
        assert response.headers["Location"] == "/auth/login"

    def test_account(self, client, auth):
        """Test that the account page loads."""
        auth.login()
        response = client.get("/account")
        assert b"test-user" in response.data
        assert b"Computer Systems Technology (CST)" in response.data
