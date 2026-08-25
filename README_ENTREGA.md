# SecureFlow Dashboard - Módulo 8: Despliegue, Monitoreo y Documentación

Bienvenido al repositorio central de **SecureFlow Dashboard**, una plataforma orientada a la arquitectura segura, monitoreo de métricas en tiempo real y alta disponibilidad mediante servicios containerizados.

---

## Arquitectura del Sistema

La solución está orquestada con **Docker Compose** e incluye una arquitectura multicapa:

* **Nginx (Reverse Proxy & SSL):** Punto de entrada seguro en los puertos `80` (HTTP) y `443` (HTTPS) con terminación TLS.
* **Backend (FastAPI / Gunicorn):** Aplicación ejecutable no-root con validaciones de salud (`/health`) y métricas (`/metrics`).
* **Prometheus:** Recolección dinámica de métricas del backend en intervalos de 15s.
* **Grafana:** Dashboard de observabilidad en tiempo real para visualización de salud e infraestructura.

---

## Observabilidad y Monitoreo

El stack integra un panel de control en Grafana (`monitoring/grafana_dashboard.json`) configurado para rastrear las 5 métricas críticas de SRE:

1. **Uso de CPU:** Consumo de procesamiento del contenedor Backend.
2. **Uso de Memoria (RAM):** Consumo de memoria residente en bytes.
3. **Peticiones por Segundo (RPS):** Tasa de tráfico entrante (`http_requests_total`).
4. **Latencia Promedio:** Tiempo de respuesta por endpoint.
5. **Tasa de Errores HTTP (5xx):** Monitoreo de fallos del lado del servidor.

---

## Guía de Despliegue Rápido

### Requisitos Previos
* Docker Engine `20.10+`
* Docker Compose `v2+`
* Python `3.11+` (para scripts de verificación local)

### Pasos para Ejecutar

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/DevSecureFlow_Modulo8_DeLaCruzNayib.git](https://github.com/tu-usuario/DevSecureFlow_Modulo8_DeLaCruzNayib.git)
   cd DevSecureFlow_Modulo8_DeLaCruzNayib
   ```
   
2. **Levantar el Stack Completo:**
   ```bash
    cd deployment
    docker compose up -d --build
   ```
   
3. **Verificar Estado de los Servicios:**
   ```bash
    docker compose ps
   ```
4 . **Ejecutar Verificación Automática (Opcional):**
   ```bash
    cd ..
    python verify_deployment.py
   ```

## Enlaces y Servicios Disponibles
* Aplicación Principal (Nginx / SSL): https://localhost

* Prometheus UI: http://localhost:9090

* Grafana Dashboards: http://localhost:3000 (Credenciales por defecto: admin / admin)

## Documentación Técnica

* Manual de Operación (Runbook): Procedimientos de despliegue, escalado de réplicas y resolución de incidentes (Troubleshooting).
* Manual de Usuario: Guía de uso de la plataforma orientada a usuarios finales.
* Documentación de Arquitectura: Diagrama de red, topología y decisiones de seguridad.

