import os

from typing import Generator

import pytest

from flask import Flask
from sqlalchemy import text

from lms.adapters import db as _db
from lms.app import app as _app
from lms.common import HERE
from tests.factories import UserFactory

AUTH_TOKEN_PATH = f"{HERE}/../.auth"


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


@pytest.fixture
def admin_user(db) -> Generator:
    admin_user = UserFactory.create()
    update_token(admin_user.auth_token)

    yield admin_user


@pytest.fixture
def student_user(db) -> Generator:
    student_user = UserFactory.create(role_id=3)
    update_token(student_user.auth_token)

    yield student_user


def update_token(token) -> None:
    if os.path.exists(AUTH_TOKEN_PATH):
        os.remove(AUTH_TOKEN_PATH)

    with open(AUTH_TOKEN_PATH, "w") as file:
        file.write(token)
