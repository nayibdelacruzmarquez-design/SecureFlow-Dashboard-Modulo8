"""Módulo principal de la aplicación FastAPI para SecureFlow Dashboard.

Este módulo inicializa la aplicación web, configura los middlewares,
expone los endpoints de la API REST e integra las métricas de Prometheus.
"""

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.config import settings
from app.logging_config import setup_logging
from app.metrics import REQUEST_COUNT

logger = setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API REST interactiva para la gestión y monitoreo del sistema SecureFlow Dashboard.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.get("/", tags=["General"])
def read_root():
    """Retorna el estado raíz del servicio y la información del entorno.

    Returns:
        dict: Estado operativo, nombre del sistema y entorno actual.
    """
    logger.info("Root endpoint accessed")
    REQUEST_COUNT.labels(method="GET", endpoint="/", status_code="200").inc()
    return {
        "status": "online",
        "system": settings.PROJECT_NAME,
        "env": settings.ENVIRONMENT,
    }


@app.get("/health", tags=["Salud"])
def health_check():
    """Verifica la disponibilidad de la aplicación para sondas de salud.

    Returns:
        dict: Estado de salud de la aplicación backend.
    """
    return {"status": "healthy", "service": "secureflow-backend"}


@app.get("/metrics", tags=["Observabilidad"])
def metrics():
    """Expone las métricas recolectadas por Prometheus en formato estándar.

    Returns:
        Response: Métricas HTTP y del sistema formateadas para scraping.
    """
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)