import pytest

from main import app as _app


TEST_CONFIG = {
    'TESTING': True
}


@pytest.fixture(scope='session')    # once run
def app():
    _app.config.update(TEST_CONFIG)
    return _app


@pytest.fixture # 매 테스트 실행 마다 실행
def client(app):
    client = app.test_client(app)
    return client
