<div align="center">
  <h3>UNIVERSIDAD NACIONAL DE SAN AGUSTÍN</h3>
  <h4>FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS</h4>
  <h4>ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS</h4>
  <br>
  <img src="/tests-docs/logo-unsa.png" alt="Logo UNSA" width="200"/>
  <br><br>
  <b>Curso:</b> Pruebas de Software <br>
  <b>Docente:</b> Ing. Robert Edison Arisaca Mamani <br>
  <b>Semestre:</b> VII <br>
  <b>Proyecto:</b> HOT Tasking Manager — EspecificaciÃ³n TÃ©cnica: Pruebas de Rendimiento <br>
  <b>Fecha de Elaboración:</b> 17/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# EspecificaciÃ³n TÃ©cnica: Pruebas de Rendimiento
**Proyecto:** HOT OSM Tasking Manager
**Componentes Evaluados:** API REST (FastAPI) y Motor Geoespacial (PostgreSQL/PostGIS)

---

## 1. Estrategia y Objetivos de EjecuciÃ³n

| Fase de Prueba | PropÃ³sito TÃ©cnico | MÃ©trica CrÃ­tica de ValidaciÃ³n | JustificaciÃ³n de DiseÃ±o |
| :--- | :--- | :--- | :--- |
| **Prueba de Carga (Load Testing)** | Medir latencia de respuesta procesando 50 sesiones concurrentes interactuando con tareas. | P95 < 2000ms; Error Rate = 0%. | Validar que el *event loop* de FastAPI no sufra bloqueos de E/S bajo el trÃ¡fico nominal esperado durante campaÃ±as de mapeo activo. |
| **Prueba de EstrÃ©s (Stress Testing)** | Sobrecargar intencionalmente el motor PostGIS (150 VUs enviando polÃ­gonos densos) para ubicar el umbral crÃ­tico de fallo (Timeouts / HTTP 504). | IdentificaciÃ³n del punto exacto de OOM (Out Of Memory) o agotamiento de CPU. | Determinar la resiliencia del *connection pool* de AsyncPG y los lÃ­mites de las operaciones espaciales de inserciÃ³n. |
| **Prueba de Resistencia (Endurance)** | Inyectar 20 VUs continuos durante 120 minutos sobre un flujo mixto (BÃºsqueda y Mapeo). | Consumo de RAM estable post-recolecciÃ³n de basura (Garbage Collector). | Evidenciar fugas de memoria (Memory Leaks) en la instanciaciÃ³n de modelos de SQLAlchemy/GeoAlchemy tras exposiciÃ³n prolongada. |

## 2. Stack TecnolÃ³gico y TopologÃ­a

| Componente | Herramienta Asignada | JustificaciÃ³n TÃ©cnica de la SelecciÃ³n |
| :--- | :--- | :--- |
| **Motor de InyecciÃ³n** | **k6 (Grafana)** | Escrito en Go, utiliza *goroutines* garantizando altÃ­sima concurrencia con mÃ­nimo consumo de RAM en el nodo atacante, evitando falsos cuellos de botella locales (habituales en JMeter). Permite aserciones nativas (*Thresholds*) automatizables en pipelines. |
| **TelemetrÃ­a de Recursos** | **Docker Stats** | Intercepta el cgroup del kernel de Linux, proporcionando el consumo real de RAM/CPU de los contenedores sin instalar agentes invasivos que alteren el rendimiento del backend bajo prueba. |

**TopologÃ­a de Red:** El motor k6 se despliega en el host local inyectando peticiones a la interfaz de loopback (`localhost:5000`) ruteadas hacia la red interna `tm-net`. Esto suprime la latencia de WAN/LAN externa, asegurando que las mÃ©tricas reflejen puramente los tiempos de procesamiento de FastAPI y PostGIS.

## 3. PreparaciÃ³n del Entorno y Datos de Prueba

| Requisito / Artefacto | ConfiguraciÃ³n TÃ©cnica y Procedimiento |
| :--- | :--- |
| **LÃ­mites de Contenedores** | Restringir el servicio `tm-backend` en `docker-compose.yml` obligatoriamente a `cpus: "1"` y `memory: "1500M"`. CondiciÃ³n sine qua non para reflejar el entorno de staging. |
| **PoblaciÃ³n Inicial (Seed)** | Ejecutar `docker compose exec tm-backend python scripts/e2e-seed.py` pre-iniciando 1 proyecto con 1000 tareas para dotar a PostGIS de Ã­ndices B-Tree y GiST realistas. |
| **Pool de AutenticaciÃ³n** | Pre-firmar 100 tokens JWT. Exportarlos a un archivo `tokens.json` para que k6 rote aleatoriamente las cabeceras `Authorization: Bearer <token>`, evitando el cachÃ© de sesiÃ³n del backend en un solo usuario. |
| **Cargas Ãštiles Geoespaciales** | Proveer arreglos de multipolÃ­gonos GeoJSON (mÃ­nimo 500 vÃ©rtices) en `/tests-docs/02-diseno-de-pruebas/sistema/payloads/` para estresar el motor de intersecciÃ³n espacial. |

## 4. Escenarios de Prueba y ConfiguraciÃ³n de k6

| ParÃ¡metro | Escenario 1: Carga Nominal (Flujo de Bloqueo de Tareas) |
| :--- | :--- |
| **Vector de Carga** | 1. `GET /api/v2/projects/1/tasks/` <br> 2. `sleep(2 a 5s)` <br> 3. `POST /api/v2/tasks/1/lock/` |
| **ConfiguraciÃ³n VUs (k6 stages)** | `{ duration: '1m', target: 50 }` (Ramp-up) <br> `{ duration: '10m', target: 50 }` (Sostenimiento) <br> `{ duration: '1m', target: 0 }` (Ramp-down) |
| **JustificaciÃ³n del Flujo** | Simula el comportamiento humano exacto: obtener la grilla espacial, visualizar (think time) y enviar la orden transaccional de bloqueo. Pone a prueba las condiciones de carrera (Race Conditions) de la base de datos al realizar locks concurrentes. |
| **ValidaciÃ³n (Thresholds)** | `http_req_duration: ['p(95)<2000']` (Latencia estricta para garantizar usabilidad del mapa). <br> `http_req_failed: ['rate==0.0']` (Tolerancia cero a fallos transaccionales). |

<br>

| ParÃ¡metro | Escenario 2: EstrÃ©s Geoespacial (CreaciÃ³n de Proyectos) |
| :--- | :--- |
| **Vector de Carga** | `POST /api/v2/projects/` (InyecciÃ³n iterativa de polÃ­gonos GeoJSON de alta densidad). |
| **ConfiguraciÃ³n VUs (k6 stages)** | `{ duration: '2m', target: 150 }` (Ramp-up agresivo) <br> `{ duration: '5m', target: 150 }` (Sostenimiento en sobrecarga) |
| **JustificaciÃ³n del Flujo** | La transformaciÃ³n de GeoJSON a tipos `geometry` en PostGIS demanda procesamiento matemÃ¡tico intensivo. 150 solicitudes paralelas obligarÃ¡n a la CPU a encolar procesos, evaluando cÃ³mo FastAPI rechaza peticiones (*Load Shedding*) sin colapsar el proceso principal. |
| **ValidaciÃ³n (Thresholds)** | RecolecciÃ³n de logs de caÃ­das. AceptaciÃ³n de tasa de errores `502 Bad Gateway` y `504 Gateway Timeout` controlados (FastAPI descartando conexiones en lugar de sufrir un evento de *OOM kill* por parte del kernel). |

## 5. Procedimiento de EjecuciÃ³n y Monitoreo

| Etapa | Comando de Consola | PropÃ³sito TÃ©cnico |
| :--- | :--- | :--- |
| **1. Arranque Limpio** | `docker compose down -v && docker compose -f docker-compose.yml -f docker-compose.e2e.yml up -d` | Destruir volÃºmenes previos para purgar cachÃ© de PostgreSQL y asegurar que PostGIS cargue los Ã­ndices a RAM desde cero (*Cold Start*). |
| **2. Siembra (Seed)** | `docker compose exec tm-backend python scripts/e2e-seed.py` | EstabilizaciÃ³n del modelo relacional previo al estrÃ©s. |
| **3. Monitoreo Activo** | `docker stats tm-backend tm-db --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"` | Vigilancia ininterrumpida para detectar si se cruza el lÃ­mite de 1.5GB RAM o 100% de CPU. |
| **4. InyecciÃ³n k6** | `k6 run scripts-k6/load-test.js --out json=results_load.json` | Despliegue del ataque de carga, serializando telemetrÃ­a en JSON para agregaciÃ³n automatizada. |
| **5. AnÃ¡lisis Forense** | EvaluaciÃ³n del volcado JSON (`results_load.json`). | Contraste empÃ­rico contra los Thresholds. Si P95 > 2s, se procede a auditar los logs de *Slow Queries* en PostgreSQL para identificar cuellos de botella en Ã­ndices. |

## 6. Consideraciones de Riesgo y Tolerancias

| Factor de Riesgo | JustificaciÃ³n del Impacto | Mecanismo de MitigaciÃ³n Integrado |
| :--- | :--- | :--- |
| **Agotamiento del Connection Pool** | Si los 50 VUs exceden las conexiones permitidas por AsyncPG, el middleware de la API colgarÃ¡ transacciones esperando hilos libres (Timeout interno). | Configurar la variable `POOL_SIZE` en `tasking-manager.env` con un valor `>= 50` previo al inicio, garantizando que el lÃ­mite evaluado sea el de procesamiento y no un estrangulamiento artificial de la BD. |
| **Interferencia de IOps del Host** | Sistemas de archivos locales lentos ralentizan los `fsync` del WAL de PostgreSQL, contaminando las latencias medidas. | Asegurar que el entorno de ejecuciÃ³n k6 resida sobre almacenamiento NVMe/SSD, o usar `tmpfs` para el volumen de datos de Docker si Ãºnicamente se requiere medir el rendimiento puramente computacional de la API. |


