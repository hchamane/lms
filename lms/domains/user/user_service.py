import os
import secrets

from typing import Final, Literal

import bcrypt

from .user_model import User, UserRole

HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))


class UserService:
    def create(self, params: dict[str, str | int]) -> tuple[str, Literal[422] | Literal[201]]:
        username = params.get("username")
        password = params.get("password")
        role = params.get("role")
        first_name = params.get("first_name")
        last_name = params.get("last_name")
        email = params.get("email")

        if not all([username, password, role, first_name, last_name, email]):
            return "Something does't look right, lease double check the parameters and try again", 422

        user = User.find_by(email=email)

        if user:
            return f"User with email {email} already exists, please double check the parameters and try again", 422

        try:
            role_id = UserRole[role.upper()].value
        except KeyError:
            return "You've specified an invalid role, please double check the parameters and try again", 422

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        User.create(
            username=username,
            password=hashed_password.decode("utf-8"),
            role_id=role_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            auth_token=secrets.token_hex(24),
        )

        return f"User with email {email} successfully created", 201

    def update(self, user_id: int, params: dict[str, str | int]) -> tuple[str, Literal[422] | Literal[200]]:
        message = "An error occured while trying to update the user, please try again"
        status_code = 422
        user = User.get(user_id)

        role = params.get("role")

        if not user:
            return "We couldn't find the specified user, please try again", 422

        if role:
            try:
                role_id = UserRole[role.upper()].value
                params["role_id"] = role_id
                del params["role"]
            except KeyError:
                return "You've specified an invalid role, please double check the parameters and try again", 422

        try:
            user.update(update_params=params)
            message = "User succesfully updated"
            status_code = 200
        except ValueError:
            pass

        return message, status_code

    def login(
        self, username: str, password: str
    ) -> tuple[Literal["Succesfully logged-in"], Literal[200]] | tuple[str, Literal[422]]:
        user = User.find_by(username=username)

        if user:
            user_password = password.encode("utf-8")
            if bcrypt.checkpw(user_password, user.password.encode("utf-8")):
                # For simplicity in the CLI, we store the user auth token in the file
                # We wouldn't do this in a production system
                with open(f"{HERE}/../../../.auth", "w") as file:
                    file.write(user.auth_token)
                return "Succesfully logged-in", 200

        return "An error occured while trying to log-in, please double check your credentials and try again.", 422
