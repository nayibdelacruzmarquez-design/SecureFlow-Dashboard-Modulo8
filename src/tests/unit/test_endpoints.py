import pytest
from unittest.mock import patch

# 1. Test con Parametrización
@pytest.mark.parametrize("endpoint, expected_status", [
    ("/health", 200),
    ("/", 200),
    ("/metrics", 200),
])
@pytest.mark.anyio
async def test_api_endpoints_param(client, endpoint, expected_status):
    response = await client.get(endpoint)
    assert response.status_code == expected_status


# 2. Test Unitario utilizando Mocks / Stubs
@pytest.mark.anyio
async def test_health_with_mock(client):
    # Hacemos mock sobre datetime donde realmente se usa (en logging_config)
    with patch("app.logging_config.datetime") as mock_datetime:
        mock_datetime.now.return_value.isoformat.return_value = "2026-08-25T00:00:00Z"
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"