from typing import Literal

from flask import Blueprint, Response, jsonify, request
from werkzeug.exceptions import BadRequest

from .user_model import User
from .user_service import UserService

user_domain = Blueprint("user_domain", __name__, url_prefix="/users")


@user_domain.post("/create")
def create_user() -> tuple[Response, Literal[422] | Literal[201]]:
    """Create a new user."""

    user_data = {}

    try:
        user_data = request.json
    except BadRequest:
        pass

    message, status = UserService().create(params=user_data)

    return jsonify({"message": message}), status


@user_domain.get("/list")
def get_all_users() -> tuple[Response, Literal[200]]:
    users = User.query.all()

    users = [
        {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "role_id": user.role_id,
        }
        for user in users
    ]
    return jsonify(users), 200


@user_domain.get("/<int:user_id>")
def get_user(user_id) -> tuple[Response, Literal[200]] | tuple[Response, Literal[422]]:
    """Get details of a user."""
    user = User.get(user_id)

    if user:
        return (
            jsonify(
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "username": user.username,
                    "role_id": user.role_id,
                }
            ),
            200,
        )

    return jsonify({"message": "No user found, please try again"}), 422


@user_domain.put("/<int:user_id>")
def update_user(user_id) -> tuple[Response, Literal[422, 200]]:
    """Update user details."""
    user_data = {}

    try:
        user_data = request.json
    except BadRequest:
        pass

    message, status = UserService().update(user_id=user_id, params=user_data)
    return jsonify({"message": message}), status
