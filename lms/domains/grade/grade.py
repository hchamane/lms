import os

from typing import Final

from flask import Blueprint, Response, jsonify, request
from werkzeug.exceptions import BadRequest

from lms.decorators import authorize_student_or_teacher, authorize_teacher

from .grade_service import GradeService

HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))

grade_domain = Blueprint("grade_domain", __name__, url_prefix="/grades")


@grade_domain.post("/create")
@authorize_teacher
def create_grade(current_user) -> tuple[Response, int]:
    """Create a new grade"""

    data = {}

    try:
        data = request.json
    except BadRequest:
        pass

    message, status = GradeService().create(params=data)

    return jsonify({"message": message}), status


@grade_domain.get("/view")
@authorize_student_or_teacher
def view_grades(current_user) -> tuple[Response, int]:
    """View all the grades for a student"""

    if not current_user.is_student():
        return jsonify({"message": "You are not a student, so there is no grades to see"}), 422

    return jsonify(current_user.grades), 200
