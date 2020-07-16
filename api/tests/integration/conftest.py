import pytest
import faker
import os
import tempfile


from app.main import app as flask_app


@pytest.fixture
def fake():
    return faker.Faker()


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as client:
        yield client
