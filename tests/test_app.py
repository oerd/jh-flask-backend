import pytest

from sample_app import create_app, db


@pytest.fixture
def client():
    app = create_app('testing')
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client


def test_get_root(client):
    """Start with a blank slate."""
    rv = client.get('/')
    assert b'' in rv.data


def test_get_hello(client):
    """Start with a blank slate."""
    rv = client.get('/hello')
    assert b'Hello, World!' in rv.data


def test_get_hi_name(client):
    """Start with a blank slate."""
    rv = client.get('/hello/moon')
    assert b'Hello, moon!' in rv.data
