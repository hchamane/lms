import pytest

from lms.domains import UserService
from tests.factories import UserFactory


@pytest.mark.usefixtures("wipe_users_table")
class TestUserService:
    def test_create_user(self) -> None:
        user = UserFactory.build()

        params = {
            "username": user.username,
            "password": user.password,
            "role": "admin",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

        message, status = UserService().create(params=params)

        assert message == f"User with email {user.email} successfully created"
        assert status == 201

    def test_create_user_with_missing_params(self) -> None:
        user = UserFactory.build()

        params = {
            "password": user.password,
            "role": "admin",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

        message, status = UserService().create(params=params)

        assert message == "Something does't look right, lease double check the parameters and try again"
        assert status == 422

    def test_create_user_with_same_email_address(self) -> None:
        user = UserFactory.create()

        params = {
            "username": user.username,
            "password": user.password,
            "role": "admin",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

        message, status = UserService().create(params=params)

        assert (
            message == f"User with email {user.email} already exists, please double check the parameters and try again"
        )
        assert status == 422

    def test_create_user_with_invalid_role(self) -> None:
        user = UserFactory.build()

        params = {
            "username": user.username,
            "password": user.password,
            "role": "invalid",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

        message, status = UserService().create(params=params)

        assert message == "You've specified an invalid role, please double check the parameters and try again"
        assert status == 422
