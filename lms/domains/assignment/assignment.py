import os

from typing import Final, Literal

from flask import Blueprint, Response, jsonify, request
from werkzeug.exceptions import BadRequest

from lms.decorators import authorise_teacher

from .assignment_model import Assignment
from .assignment_service import AssignmentService

HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))

assignment_domain = Blueprint("assignment_domain", __name__, url_prefix="/assignments")


@assignment_domain.post("/create")
@authorise_teacher
def create_assignment(current_user) -> tuple[Response, Literal[422] | Literal[201]]:
    """Create a new assignment"""

    data = {}

    try:
        data = request.json
    except BadRequest:
        pass

    message, status = AssignmentService().create(current_user=current_user, params=data)

    return jsonify({"message": message}), status


@assignment_domain.get("/list")
@authorise_teacher
def list_available_assignment(current_user) -> tuple[Response, Literal[200]]:
    """List all the available assignments"""

    assignments = Assignment.query.all()

    assignments = [
        {
            "id": assignment.id,
            "title": assignment.title,
        }
        for assignment in assignments
    ]
    return jsonify(assignments), 200
