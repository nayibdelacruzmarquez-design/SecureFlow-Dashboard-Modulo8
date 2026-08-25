import pytest


@pytest.mark.anyio
async def test_e2e_health_check(client):
    # Simulamos el pipeline completo llamando a la API
    res_health = await client.get("/health")
    assert res_health.status_code == 200

    res_root = await client.get("/")
    assert res_root.status_code == 200