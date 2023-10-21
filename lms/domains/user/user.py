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


# @user_domain.get("/<int:user_id>")
# def get_user(user_id):
#     """Get details of a user."""
#     user = next((u for u in users_db if u["id"] == user_id), None)
#     if not user:
#         return jsonify({"message": "User not found!"}), 404
#     return jsonify(user), 200


# @user_domain.put("/<int:user_id>")
# def update_user(user_id):
#     """Update user details."""
#     user = next((u for u in users_db if u["id"] == user_id), None)
#     if not user:
#         return jsonify({"message": "User not found!"}), 404
#     updated_data = request.json
#     user.update(updated_data)
#     return jsonify({"message": "User updated successfully!", "user": user}), 200


# @user_domain.delete("/<int:user_id>")
# def delete_user(user_id):
#     """Delete a user."""
#     global users_db
#     users_db = [u for u in users_db if u["id"] != user_id]
#     return jsonify({"message": "User deleted successfully!"}), 200
