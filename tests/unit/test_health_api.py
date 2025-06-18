import json


def test_health_check(test_client):
    """Test the health check endpoint."""
    response = test_client.get("/v1/health/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"status": "ok"}
