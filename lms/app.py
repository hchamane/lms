import subprocess

from flask import Response, jsonify

from lms.make_app import make_app

app = make_app()


@app.get("/")
@app.get("/status")
def check_status() -> Response:
    commit_id = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
    return jsonify({"sha": commit_id, "status": "up"})
