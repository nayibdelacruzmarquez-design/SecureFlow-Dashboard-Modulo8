# Documento de Diseño Arquitectónico: SecureFlow Systems

## 1. Visión General de la Arquitectura
**SecureFlow Systems** adopta una **Arquitectura de Microservicios Modularizada** encapsulada en contenedores Docker y expuesta a través de un proxy inverso Nginx. Esta elección garantiza un acoplamiento débil, alta disponibilidad, escalabilidad horizontal independiente de componentes y una superficie de ataque reducida.

---

## 2. Topología de Red y Entornos de Despliegue

### 2.1 Entorno Intranet (Acceso Corporativo Interno)
* **Propósito:** Gestión interna de flujos de trabajo por personal autorizado de la organización.
* **Características:** Red privada LAN/VPC aislada, alta velocidad de transferencia, autenticación unificada.
* **Diagrama de Flujo:**
```text
[Cliente Interno (LAN)]
        │ (HTTP/HTTPS interno)
        ▼
┌─────────────────────────────────────────┐
│ Firewall Interno / Segmentación LAN     │
└───────────────────┬─────────────────────┘
                    ▼
┌─────────────────────────────────────────┐
│ Nginx Reverse Proxy (Internal Load Bal) │
└───────────────────┬─────────────────────┘
                    ▼
┌─────────────────────────────────────────┐
│ SecureFlow Backend (FastAPI / Gunicorn) │
└─────────────────────────────────────────┘
```
## 2.2 Entorno Extranet (Arquitectura Zero Trust para Partners)
* Propósito: Intercambio de datos con socios de negocio y contratistas externos.
* Modelo de Seguridad: Zero Trust Network Architecture (ZTNA). Exige verificación continua de identidad, autorización explícita por petición y microsegmentación de red ("Nunca confíes, siempre verifica").
* Diagrama de Flujo:
```text
[Partner Externo (Internet)]
        │ (HTTPS - TLS 1.3)
        ▼
┌─────────────────────────────────────────┐
│ WAF / Firewall Perimetral               │
└───────────────────┬─────────────────────┘
                    ▼
┌─────────────────────────────────────────┐
│ Identity & Access Gateway (mTLS + JWT)  │
└───────────────────┬─────────────────────┘
                    ▼
┌─────────────────────────────────────────┐
│ Nginx Reverse Proxy (Zero Trust Ingress)│
└───────────────────┬─────────────────────┘
                    ▼
┌─────────────────────────────────────────┐
│ SecureFlow API Service (Isolated DMZ)   │
└─────────────────────────────────────────┘
```
## 2.3 Entorno Internet (Portal Público Escalable)
* Propósito: Servicios públicos, consulta de estado y documentación interactiva de APIs.
* Características: Balanceo de carga pasivo/activo, terminación TLS estricta, protección contra ataques DDoS/OWASP Top 10 y caché de activos estáticos.
* Diagrama de Flujo:
```text
[Usuario Público / API Client]
        │ (HTTPS - Puerto 443)
        ▼
┌─────────────────────────────────────────┐
│ DNS / Cloud WAF (Rate Limiting)         │
└───────────────────┬─────────────────────┘
                    ▼
┌─────────────────────────────────────────┐
│ Nginx Ingress Controller (SSL/TLS Term) │
└───────────────────┬─────────────────────┘
          ┌─────────┴─────────┐
          ▼                   ▼
┌──────────────────┐ ┌──────────────────┐
│ Gunicorn Worker 1│ │ Gunicorn Worker 2│
└──────────────────┘ └──────────────────┘
```
## 3. Roles de Componentes Perimetrales y de Red
* Nginx Reverse Proxy: Actúa como único punto de entrada (Ingress), gestiona la terminación TLS, sirve archivos estáticos directamente, aplica cabeceras de seguridad HTTP y distribuye la carga entre los workers de aplicación.
* Servidor ASGI (Uvicorn / Gunicorn): Gunicorn gestiona los procesos worker mientras que Uvicorn maneja el bucle de eventos asíncrono de FastAPI para alta concurrencia.
* Firewall / WAF: Aplica filtrado de IP, prevención de ataques de fuerza bruta y mitigación de vulnerabilidades OWASP Top 10.

## 4. Justificación Técnica de Decisiones y Trade-Offs
| Decisión Arquitectónica | Ventajas Obtenidas | Trade-Off / Mitigación |
| :--- | :--- | :--- |
| **FastAPI + Uvicorn/Gunicorn** | Alta velocidad de respuesta I/O asíncrona, especificación OpenAPI automática. | Mayor complejidad en depuración asíncrona -> Mitigado con logging estructurado JSON. |
| **Nginx Proxy Inverso** | Descarga de TLS, protección del backend, balanceo de carga nativo. | Punto único de fallo si no hay redundancia -> Mitigado con contenedores aislados y verificaciones de salud (`healthchecks`). |
| **Zero Trust en Extranet** | Mínimo privilegio, aislamiento total de subredes corporativas. | Sobrecarga en validación de tokens por petición -> Mitigado con verificación de firmas JWT en memoria sin I/O a base de datos. |