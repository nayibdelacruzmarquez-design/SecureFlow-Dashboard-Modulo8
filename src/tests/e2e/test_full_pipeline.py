def test_e2e_health_and_root_flow(client):
    """Flujo E2E 1: Navegación de estado y raíz de la aplicación."""
    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["service"] == "secureflow-backend"

    res_root = client.get("/")
    assert res_root.status_code == 200


def test_e2e_metrics_observability_flow(client):
    """Flujo E2E 2: Flujo crítico de métricas de observabilidad."""
    res_metrics = client.get("/metrics")
    assert res_metrics.status_code == 200