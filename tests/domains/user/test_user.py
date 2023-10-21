import json

import pytest

from tests.factories import UserFactory


@pytest.mark.usefixtures("wipe_users_table")
class TestUser:
    def test_create_user(self, client) -> None:
        user = UserFactory.build()

        params = {
            "username": user.username,
            "password": user.password,
            "role": "admin",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

        response = client.post("/users/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 201
        assert data.get("message") == f"User with email {user.email} successfully created"

    def test_create_user_with_missing_argument(self, client) -> None:
        user = UserFactory.build()

        params = {
            "password": user.password,
            "role": "admin",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

        response = client.post("/users/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 422
        assert data.get("message") == "Something does't look right, lease double check the parameters and try again"

    def test_create_user_with_existing_email_address(self, client) -> None:
        user = UserFactory.create()

        params = {
            "username": "username",
            "password": user.password,
            "role": "admin",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

        response = client.post("/users/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 422
        assert (
            data.get("message")
            == f"User with email {user.email} already exists, please double check the parameters and try again"
        )
