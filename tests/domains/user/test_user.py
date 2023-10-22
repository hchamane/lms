import json

import pytest

from lms.domains import User, UserRole
from tests.factories import StudentFactory, UserFactory


@pytest.mark.usefixtures("wipe_users_table")
class TestUser:
    def test_create_user(self, client, admin_user) -> None:
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

    def test_create_user_with_missing_argument(self, client, admin_user) -> None:
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

    def test_create_user_with_existing_email_address(self, client, admin_user) -> None:
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

    def test_list_all_users(self, client, admin_user) -> None:
        UserFactory.create()
        UserFactory.create()

        response = client.get("/users/list")
        data = json.loads(response.data)

        assert isinstance(data, list)
        assert len(data) >= 1
        assert "email" in data[0]
        assert "first_name" in data[0]
        assert "last_name" in data[0]
        assert "role_id" in data[0]
        assert "username" in data[0]

    def test_list_all_users_as_a_teacher(self, client, teacher_user) -> None:
        UserFactory.create()
        UserFactory.create()

        response = client.get("/users/list")
        data = json.loads(response.data)

        assert isinstance(data, list)
        assert len(data) >= 1
        assert "email" in data[0]
        assert "first_name" in data[0]
        assert "last_name" in data[0]
        assert "role_id" in data[0]
        assert "username" in data[0]

    def test_list_all_users_as_a_student(self, client, student_user) -> None:
        UserFactory.create()
        UserFactory.create()

        response = client.get("/users/list")
        data = json.loads(response.data)

        assert response.status_code == 401

        assert data == {
            "message": (
                "It appears you are not authorised to perform this action. "
                "Please double-check your authorization and try again."
            )
        }

    def test_get_single_user(self, client, admin_user) -> None:
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

    def test_get_single_user_with_no_matching_users(self, client, admin_user) -> None:
        response = client.get("/users/8486814619864")
        data = json.loads(response.data)

        assert data == {"message": "No user found, please try again"}
        assert response.status_code == 422

    def test_update_user(self, client, admin_user) -> None:
        student_user = UserFactory.create(first_name="John", role_id=UserRole.STUDENT.value)

        student_user = User.get(student_user.id)
        assert student_user.first_name == "John"

        response = client.put(f"/users/{student_user.id}", json={"first_name": "Bob"})

        data = json.loads(response.data)

        assert data == {"message": "User succesfully updated"}
        assert response.status_code == 200

        user = User.get(student_user.id)
        assert user.first_name == "Bob"

    def test_update_user_with_non_existing_user_id(self, client, admin_user) -> None:
        UserFactory.create()

        response = client.put("/users/8374198364", json={"first_name": "Bob"})

        data = json.loads(response.data)

        assert data == {"message": "We couldn't find the specified user, please try again"}
        assert response.status_code == 422

    def test_update_user_with_invalid_role(self, client, admin_user) -> None:
        user = UserFactory.create()
        response = client.put(f"/users/{user.id}", json={"role": "invalid"})

        data = json.loads(response.data)

        assert data == {"message": "You've specified an invalid role, please double check the parameters and try again"}
        assert response.status_code == 422

    def test_update_user_with_incorrect_permissions(self, client, student_user) -> None:
        another_student_user = UserFactory.create(first_name="John", role_id=UserRole.STUDENT.value)

        another_student_user = User.get(another_student_user.id)
        assert another_student_user.first_name == "John"

        response = client.put(f"/users/{another_student_user.id}", json={"first_name": "Bob"})

        data = json.loads(response.data)

        assert data == {
            "message": (
                "It appears you are not authorised to perform this action. "
                "Please double-check your authorization and try again."
            )
        }
        assert response.status_code == 401

    def test_list_all_students_as_a_teacher(self, client, teacher_user) -> None:
        StudentFactory.create()
        StudentFactory.create()

        response = client.get("/users/list_students")
        data = json.loads(response.data)

        assert isinstance(data, list)
        assert len(data) >= 1
        assert "id" in data[0]
        assert "first_name" in data[0]
        assert "last_name" in data[0]

    def test_list_all_students_as_a_student(self, client, student_user) -> None:
        StudentFactory.create()
        StudentFactory.create()

        response = client.get("/users/list_students")
        data = json.loads(response.data)

        assert response.status_code == 401

        assert data == {
            "message": (
                "It appears you are not authorised to perform this action. "
                "Please double-check your authorization and try again."
            )
        }
