from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.config import settings
from app.logging_config import setup_logging
from app.metrics import REQUEST_COUNT

logger = setup_logging()
app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    REQUEST_COUNT.labels(method="GET", endpoint="/", status_code="200").inc()
    return {"status": "online", "system": settings.PROJECT_NAME, "env": settings.ENVIRONMENT}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "secureflow-backend"}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)