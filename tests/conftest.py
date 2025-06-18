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


@pytest.fixture()
def db(test_app):
    from app.extensions import db as _db

    with test_app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()
