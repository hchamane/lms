import json

import pytest

from lms.domains import User
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

    def test_list_all_users(self, client) -> None:
        user = UserFactory.create()

        response = client.get("/users/list")
        data = json.loads(response.data)

        assert data == [
            {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role_id": 1,
                "username": user.username,
            }
        ]

        UserFactory.create()

        response = client.get("/users/list")
        data = json.loads(response.data)

        assert len(data) == 2

    def test_get_single_user(self, client) -> None:
        user = UserFactory.create()

        response = client.get(f"/users/{user.id}")
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data == {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role_id": 1,
            "username": user.username,
        }

    def test_get_single_user_with_no_matching_users(self, client) -> None:
        response = client.get("/users/8486814619864")
        data = json.loads(response.data)

        assert data == {"message": "No user found, please try again"}
        assert response.status_code == 422

    def test_update_user(self, client) -> None:
        user = UserFactory.create(first_name="John")

        user = User.get(user.id)
        assert user.first_name == "John"

        response = client.put(f"/users/{user.id}", json={"first_name": "Bob"})

        data = json.loads(response.data)

        assert data == {"message": "User succesfully updated"}
        assert response.status_code == 200

        user = User.get(user.id)
        assert user.first_name == "Bob"

    def test_update_user_with_non_existing_user_id(self, client) -> None:
        response = client.put("/users/8374198364", json={"first_name": "Bob"})

        data = json.loads(response.data)

        assert data == {"message": "We couldn't find the specified user, please try again"}
        assert response.status_code == 422

    def test_update_user_with_invalid_role(self, client) -> None:
        user = UserFactory.create()
        response = client.put(f"/users/{user.id}", json={"role": "invalid"})

        data = json.loads(response.data)

        assert data == {"message": "You've specified an invalid role, please double check the parameters and try again"}
        assert response.status_code == 422
