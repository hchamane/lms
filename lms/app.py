from flask import Response, jsonify, request
from werkzeug.exceptions import BadRequest

from lms.domains import UserService, user_domain
from lms.make_app import make_app

app = make_app()


for domain in (user_domain,):
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
