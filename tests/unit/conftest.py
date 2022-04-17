import os
import warnings

os.environ['ENV'] = 'test'

import alembic.command
import pytest
from alembic.config import Config


from main import app as _app


TEST_CONFIG = {
    'TESTING': True
}


@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture(scope='session')
def app(apply_migrations):
    _app.config.update(TEST_CONFIG)
    return _app


@pytest.fixture
def client(app):
    client = app.test_client(app)
    return client
