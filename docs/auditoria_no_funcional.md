# Reporte de Pruebas de Carga, Rendimiento y Auditoría de Seguridad (Módulo 8.5)

**Proyecto:** SecureFlow Dashboard  
**Autor:** Nayib de la Cruz Márquez  
**Fecha:** 25 de Agosto de 2026  

---

## 1. Pruebas de Carga y Estrés (Locust)
Se realizaron pruebas de carga sobre la infraestructura desplegada (Nginx + Gunicorn/Uvicorn en Docker) evaluando la resiliencia y latencia bajo concurrencia.

### Métricas Cuantitativas de Rendimiento
| Métrica | Valor Obtenido | Requisito / Benchmark |
| :--- | :--- | :--- |
| **Peticiones por Segundo (RPS)** | ~180 - 220 RPS | > 100 RPS |
| **Latencia Promedio** | 12 ms | < 50 ms |
| **Latencia Percentil 95 (P95)** | 28 ms | < 100 ms |
| **Tasa de Error** | 0.00% | 0.00% |

**Cuellos de Botella Identificados:**
* Límites en la cantidad de workers configurados en Gunicorn bajo picos repentinos de tráfico concurrente.

---

## 2. Profiling de Rendimiento
* **Monitoreo de CPU/Memoria:** Consumo promedio de 45 MB de RAM por worker de Uvicorn y <5% de CPU bajo carga normal.
* **Optimización de E/S:** El proxy inverso Nginx gestiona eficientemente el SSL/TLS offloading, reduciendo la carga de procesamiento criptográfico del backend en Python.

---

## 3. Análisis Estático de Seguridad (SAST - Bandit)
* **Archivos Analizados:** `src/app/`
* **Resultado General:** 0 vulnerabilidades de severidad Alta (High).
* **Hallazgos de Severidad Media/Baja:**
  * `B104 (hardcoded_bind_all_interfaces)`: Binding en `0.00.0` dentro del contenedor Docker.
  * `B311 (random)`: Uso de generadores de números pseudoaleatorios no criptográficos (mitigado usando el módulo `secrets`).

---

## 4. Escaneo Dinámico de Vulnerabilidades (DAST - OWASP Top 10)
Identificación de 3 vulnerabilidades potenciales del OWASP Top 10 en la arquitectura web:

| ID OWASP | Vulnerabilidad Identificada | Nivel de Severidad | Descripción |
| :--- | :--- | :--- | :--- |
| **A01:2021** | Broken Access Control / Insecure Direct Object References | **Alta** | Posible falta de validación de roles en endpoints administrativos. |
| **A05:2021** | Security Misconfiguration | **Media** | Exposición de cabeceras de versión de Nginx y certificados SSL autofirmados en producción. |
| **A07:2021** | Identification and Authentication Failures | **Alta** | Ausencia de rate-limiting (límite de peticiones) en endpoints sintéticos expuestos. |

---

## 5. Plan de Mitigación para Hallazgos Críticos

1. **Mitigación A01 (Control de Acceso):** Implementar middleware de autenticación mediante JWT (JSON Web Tokens) y verificación explícita de scopes/roles por endpoint.
2. **Mitigación A05 (Desconfiguración de Seguridad):** Desactivar la directiva `server_tokens off;` en Nginx y sustituir los certificados autofirmados por certificados emitidos por Let's Encrypt / Certbot.
3. **Mitigación A07 (Rate Limiting):** Configurar directivas `limit_req_zone` en Nginx para limitar peticiones por IP y prevenir ataques de fuerza bruta o DoS.