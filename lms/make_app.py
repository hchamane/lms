import os
import secrets

from typing import Final

from dotenv import load_dotenv
from flask import Flask
from flask_compress import Compress
from flask_cors import CORS

from lms.adapters import db

HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))


def make_app() -> Flask:
    compress = Compress()
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(24)
    compress.init_app(app)

    CORS(app)
    load_dotenv()

    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True, "pool_recycle": 280, "pool_size": 90}

    db.init_app(app)

    return app


def database_uri() -> str:
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")
    host = os.environ.get("HOST")
    port = os.environ.get("PORT")
    database = os.environ.get("DATABASE")
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"
