from unittest.mock import patch
import pytest


# 1. Test con Parametrización
@pytest.mark.parametrize(
    "endpoint, expected_status",
    [
        ("/health", 200),
        ("/", 200),
        ("/metrics", 200),
    ],
)
def test_api_endpoints_param(client, endpoint, expected_status):
    response = client.get(endpoint)
    assert response.status_code == expected_status


# 2. Test Unitario utilizando Mocks / Stubs
def test_health_with_mock(client):
    with patch("app.logging_config.datetime") as mock_datetime:
        mock_datetime.now.return_value.isoformat.return_value = (
            "2026-08-25T00:00:00Z"
        )
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"