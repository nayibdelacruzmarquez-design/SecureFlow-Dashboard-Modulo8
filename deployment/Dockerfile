# Build Stage
FROM python:3.11-slim AS builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final Stage (Multi-stage build & non-root user)
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app/src

RUN addgroup --system appgroup && adduser --system --group appuser

COPY --from=builder /install /usr/local

# Copiamos tanto deployment como src
COPY deployment /app/deployment
COPY src /app/src

# Asignamos permisos correctos al usuario no root
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

# Comando por defecto (apunta a app.main:app porque PYTHONPATH=/app/src)
CMD ["gunicorn", "-c", "deployment/gunicorn_config.py", "app.main:app"]