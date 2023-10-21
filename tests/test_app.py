import json


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
