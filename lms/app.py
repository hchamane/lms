import subprocess

from flask import Response, jsonify

from lms.domains import user_domain
from lms.make_app import make_app

app = make_app()


for domain in (user_domain,):
    app.register_blueprint(domain)


@app.get("/")
def root() -> Response:
    return jsonify({"message": "hi!", "status": "up"})
