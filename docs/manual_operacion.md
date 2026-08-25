# Manual de Operación (Runbook) - SecureFlow Dashboard

## 1. Procedimiento de Despliegue
```bash
cd deployment
docker compose up -d --build
python ../verify_deployment.py
```
## 2. Escalado Horizontal

```bash
docker compose up -d --scale web=3
```
## 3. Resoluciones de Incidencias (Troubleshooting)
### Escenario A: Nginx responde con 502 Bad Gateway
1. Verificar estado de los contenedores: docker compose ps

2. Revisar logs del backend: docker compose logs web

3. Reiniciar el servicio: docker compose restart web

### Escenario B: Picos de Consumo de Memoria o CPU
1. Monitorear métricas en Grafana (process_resident_memory_bytes).

2. Consultar trazas en logs/app.log.

3. Escalar backend horizontalmente o reiniciar el contenedor.

### Escenario C: Fallo de Certificado SSL / Puerto 443
1. Validar la existencia de archivos en deployment/nginx/ssl/.

2. Probar conectividad con el script local: python verify_deployment.py.

