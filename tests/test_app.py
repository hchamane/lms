import json


class TestApp:
    def test_check_status(self, client) -> None:
        response = client.get("/status")
        data = json.loads(response.data)

        assert response.status_code == 200
        assert isinstance(data, dict)
        assert "sha" in data
        assert "status" in data
        assert data["status"] == "up"
        assert len(data["sha"]) == 40
