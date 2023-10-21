import os

from typing import Final, Literal

from flask import Response, jsonify, request
from werkzeug.exceptions import BadRequest

from lms.domains import UserService, assignment_domain, grade_domain, module_domain, user_domain
from lms.make_app import make_app

HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))
AUTH_TOKEN_PATH = f"{HERE}/../.auth"

app = make_app()


for domain in (assignment_domain, grade_domain, module_domain, user_domain):
    app.register_blueprint(domain)


@app.get("/")
def root() -> Response:
    return jsonify({"message": "hi!", "status": "up"})


@app.post("/login")
def login() -> Response:
    login_data = {}

    try:
        login_data = request.json
    except BadRequest:
        pass

    if login_data:
        username = login_data.get("username")
        password = login_data.get("password")

    message, status = UserService().login(username=username, password=password)

    return jsonify({"message": message}), status


@app.put("/logout")
def logout() -> tuple[Response, Literal[200]]:
    if os.path.exists(AUTH_TOKEN_PATH):
        os.remove(AUTH_TOKEN_PATH)

    return jsonify({"message": "Successfully logged-out of the app"}), 200
