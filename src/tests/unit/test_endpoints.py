import pytest


@pytest.mark.parametrize("endpoint, expected_status", [
    ("/health", 200),
    ("/", 200),
    ("/metrics", 200),
])
@pytest.mark.anyio
async def test_api_endpoints_param(client, endpoint, expected_status):
    response = await client.get(endpoint)
    assert response.status_code == expected_status