import json
import os

from tests.conftest import AUTH_TOKEN_PATH


class TestApp:
    def test_root(self, client) -> None:
        response = client.get("/")
        data = json.loads(response.data)

        assert response.status_code == 200
        assert isinstance(data, dict)
        assert "message" in data
        assert "status" in data
        assert data["message"] == "hi!"
        assert data["status"] == "up"

    def test_login(self, client, admin_user) -> None:
        username = "john"
        password = "password"

        params = {
            "username": username,
            "password": password,
            "role": "admin",
            "first_name": "John",
            "last_name": "Smith",
            "email": "johm@test.com",
        }
        client.post("/users/create", json=params)

        response = client.post("/login", json={"username": username, "password": password})
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data == {"message": "Succesfully logged-in"}

    def test_login_with_invalid_password(self, client) -> None:
        username = "john"
        password = "password"

        params = {
            "username": username,
            "password": password,
            "role": "admin",
            "first_name": "John",
            "last_name": "Smith",
            "email": "johm@test.com",
        }
        client.post("/users/create", json=params)

        response = client.post("/login", json={"username": username, "password": "invalid_password"})
        data = json.loads(response.data)

        assert response.status_code == 422
        assert data == {
            "message": "An error occured while trying to log-in, please double check your credentials and try again."
        }

    def test_login_with_invalid_user(self, client) -> None:
        username = "jack"
        password = "password"

        response = client.post("/login", json={"username": username, "password": password})
        data = json.loads(response.data)

        assert response.status_code == 422
        assert data == {
            "message": "An error occured while trying to log-in, please double check your credentials and try again."
        }

    def test_logout(self, client, admin_user) -> None:
        assert os.path.exists(AUTH_TOKEN_PATH)
        response = client.put("/logout")
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data == {"message": "Successfully logged-out of the app"}
        assert not os.path.exists(AUTH_TOKEN_PATH)
