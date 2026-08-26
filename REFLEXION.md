# Reflexión Técnica: Implementación de Pipeline CI/CD y Despliegue Automatizado

## Resumen del Proyecto
Durante la implementación del dashboard **SecureFlow**, se logró estructurar una canalización de Integración y Despliegue Continuo (CI/CD) completamente automatizada en GitHub Actions, garantizando altos estándares de calidad de software, cobertura de pruebas y seguridad en la compilación de contenedores.

## Desafíos Técnicos y Soluciones

### 1. Gestión de Pruebas Asíncronas y Runners en CI/CD
* **Problema:** La suite de pruebas con `pytest` presentaba un comportamiento de "bloqueo" (*hanging runner*) durante la ejecución en entornos Linux (GitHub Actions), principalmente en pruebas que involucraban el recolector de métricas de Prometheus y clientes HTTP asíncronos.
* **Solución:** Se alineó la arquitectura de pruebas utilizando `fastapi.testclient.TestClient` en modo síncrono y se configuró la variable de entorno `GEVENT_NO_MONKEY=1` junto con la bandera `--ignore` para aislar los scripts de pruebas de carga (`locust`) del alcance de `pytest`.

### 2. Optimización del Contexto de Construcción en Docker
* **Problema:** El job de compilación Docker (`Build & Push Docker Image`) fallaba al no encontrar directorios clave como `src/` o `deployment/`.
* **Solución:** Se reestructuró el archivo `.dockerignore` para permitir únicamente la exclusión de entornos virtuales, directorios de caché de Python (`__pycache__`) y artefactos temporales de cobertura, liberando el acceso a las fuentes principales de la aplicación.

## Conclusión
La arquitectura final garantiza que cada `push` o `pull request` hacia la rama principal ejecute automáticamente análisis de seguridad estático (SAST con Bandit), ejecute la suite de pruebas unitarias/E2E con una cobertura superior al 95%, y valide la salud del servicio en un entorno de staging con mecanismos de rollback automático.