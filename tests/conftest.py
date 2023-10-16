from typing import Generator

import pytest

from flask import Flask

from lms.app import app as _app


@pytest.fixture
def app(request) -> Generator:
    app = _app
    with app.app_context():
        yield app


@pytest.fixture()
def client(app) -> Flask:
    return app.test_client()
