# Build Stage
FROM python:3.11-slim AS builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && rm -rf /var/lib/apt/lists/*
COPY src/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final Stage (Multi-stage build & non-root user)
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app/src

RUN addgroup --system appgroup && adduser --system --group appuser

COPY --from=builder /install /usr/local
COPY src /app/src

USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]