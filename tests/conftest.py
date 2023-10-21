from typing import Generator

import pytest

from flask import Flask
from sqlalchemy import text

from lms.adapters import db as _db
from lms.app import app as _app


@pytest.fixture
def app(request) -> Generator:
    app = _app
    with app.app_context():
        yield app


@pytest.fixture()
def client(app) -> Flask:
    return app.test_client()


@pytest.fixture
def db(app, request, monkeypatch) -> Generator:
    connection = _db.engine.connect()
    transaction = connection.begin()

    monkeypatch.setattr(_db, "get_engine", lambda *args, **kwargs: connection)

    try:
        yield _db
    finally:
        _db.session.remove()
        transaction.rollback()
        connection.close()


@pytest.fixture
def wipe_users_table(db) -> Generator:
    yield
    db.session.execute(text("TRUNCATE users CASCADE;"))
    db.session.commit()
