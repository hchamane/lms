import secrets

from flask import Flask
from flask_compress import Compress
from flask_cors import CORS


def make_app() -> Flask:
    compress = Compress()
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(24)
    compress.init_app(app)

    CORS(app)

    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    return app
