import pytest
from app import create_app


@pytest.fixture(scope="module")
def test_app():
    """Create and configure a new app instance for each test."""
    app = create_app("testing")
    yield app


@pytest.fixture(scope="module")
def test_client(test_app):
    """A test client for the app."""
    return test_app.test_client()
