import pytest


@pytest.mark.anyio
async def test_metrics_endpoint(client):
    response = await client.get("/metrics")
    assert response.status_code == 200