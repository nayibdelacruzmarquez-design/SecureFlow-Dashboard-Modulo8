# Auto-crítica y Reflexión Técnica - SecureFlow Systems (Módulo 8)

---

## 1. Arquitectura y Decisiones Técnicas

### Elección de Arquitectura
Para **SecureFlow Systems** se seleccionó una **arquitectura por capas orientada a microservicios/servicios independientes**, orquestada mediante Docker Compose y protegida por un Reverse Proxy (Nginx). 

### Impacto en Entornos (Internet, Intranet y Extranet)
* **Internet:** Nginx actúa como fachada pública gestionando terminación TLS/SSL (puertos 80/443), bloqueando tráfico no deseado y aislando los servicios internos de la exposición directa.
* **Intranet:** Los servicios como la aplicación backend (`app`), Prometheus y Grafana operan en redes internas containerizadas, garantizando que el tráfico entre componentes no pase por interfaces públicas.
* **Extranet:** Se implementaron políticas de *Zero Trust* e inspección de rutas restringidas para la interacción segura con clientes externos autorizados.

### Trade-offs y Mitigaciones
* **Complejidad de Orquestación vs. Aislamiento:** Gestionar múltiples contenedores incrementa la sobrecarga de configuración. Esto se mitigó estandarizando los contextos de *build* en `docker-compose.yml` y definiendo un *healthcheck* explícito para evitar condiciones de carrera entre Nginx y el Backend.
* **Consumo de Recursos vs. Observabilidad:** Levantar prometheus y grafana consume RAM/CPU adicional. Se mitigó ajustando los intervalos de *scrape* a 15 segundos y optimizando los *queries* de métricas.

---

## 2. Calidad y Automatización

### Cobertura y Pipeline CI/CD
Las pruebas unitarias e integración validadas con `pytest` y la automatización en el flujo de despliegue permitieron detectar fallos en rutas, permisos de usuario y errores de dependencias de forma temprana (antes de la construcción final del contenedor).

### Métricas de Rendimiento y Cobertura
* **Métricas de Cobertura:** Se alcanzó una cobertura de código adecuada en las rutas críticas del backend (`/health`, `/metrics` y endpoints principales).
* **Rendimiento:** Latencias de respuesta por debajo de los umbrales esperados gracias al servidor WSGI/ASGI (`gunicorn` con trabajadores optimizados).

### Limitaciones Identificadas
* Las pruebas de carga locales dependen de los recursos limitados del entorno de desarrollo de Docker Desktop (Windows/WSL2), lo cual puede generar variaciones en la medición de latencia real bajo estrés extremo en comparación con un entorno de nube dedicado.

---

## 3. Operación y Documentación

### Utilidad Práctica de Manuales y Artefactos
* **Manual de Operación (Runbook):** Proporciona procedimientos paso a paso para el despliegue, escalado dinámico de servicios y resolución de incidentes (troubleshooting para fallos de montaje, contenedores *unhealthy* y puertos).
* **Manual de Usuario:** Traduce la funcionalidad técnica a un lenguaje claro para usuarios finales y partes interesadas.
* **Documentación Técnica y Swagger:** La especificación de la API facilita la integración rápida sin necesidad de inspeccionar el código fuente.

### Onboarding y Soporte
Estos artefactos reducen drásticamente la curva de aprendizaje para nuevos desarrolladores que se sumen al repositorio, permitiéndoles replicar el entorno de desarrollo en minutos con `docker compose up` y resolver errores operativos comunes sin necesidad de escalar incidentes al equipo de arquitectura.