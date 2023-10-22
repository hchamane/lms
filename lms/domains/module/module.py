import os

from typing import Final, Literal

from flask import Blueprint, Response, jsonify, request
from werkzeug.exceptions import BadRequest

from lms.decorators import authorise_teacher

from .module_service import ModuleService

HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))

module_domain = Blueprint("module_domain", __name__, url_prefix="/modules")


@module_domain.post("/create")
@authorise_teacher
def create_module(current_user) -> tuple[Response, Literal[422] | Literal[201]]:
    """Create a new module"""

    user_data = {}

    try:
        user_data = request.json
    except BadRequest:
        pass

    message, status = ModuleService().create(current_user=current_user, params=user_data)

    return jsonify({"message": message}), status
