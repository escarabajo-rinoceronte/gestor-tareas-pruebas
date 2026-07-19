<div align="center">
  <h3>UNIVERSIDAD NACIONAL DE SAN AGUSTÍN</h3>
  <h4>FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS</h4>
  <h4>ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS</h4>
  <br>
  <img src="/tests-docs/img/logo-unsa.png" alt="Logo UNSA" width="200"/>
  <br><br>
  <b>Curso:</b> Pruebas de Software <br>
  <b>Docente:</b> Ing. Robert Edison Arisaca Mamani <br>
  <b>Semestre:</b> VII <br>
  <b>Proyecto:</b> HOT Tasking Manager — Plan de Pruebas de Sistema <br>
  <b>Fecha de Elaboración:</b> 03/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Plan de Pruebas de Sistema
**Proyecto:** HOT OSM Tasking Manager
**VersiÃ³n del Documento:** 2.0
**EstÃ¡ndares de Referencia:** ISO/IEC/IEEE 29119-3, IEEE 829

---

## 1. IntroducciÃ³n y Alcance

### 1.1. Objetivo
Definir la estrategia global, el alcance, los recursos y el cronograma para la ejecuciÃ³n de las **Pruebas de Sistema**. Este documento unifica y reemplaza todos los planes anteriores (incluyendo planes aislados de E2E). ValidarÃ¡ que todos los componentes (Frontend en React, Backend en FastAPI, Base de Datos PostGIS) funcionan conjuntamente bajo escenarios funcionales, de rendimiento y de seguridad.

### 1.2. Alcance
El alcance incluye las siguientes tres dimensiones integradas de pruebas a nivel de sistema:
* **E2E Funcional:** Flujos de negocio priorizados y completos (Mapeo, ValidaciÃ³n y AdministraciÃ³n de Proyectos).
* **Rendimiento:** ValidaciÃ³n de los lÃ­mites de carga, estrÃ©s y resistencia del backend en su infraestructura de contenedores.
* **Seguridad:** AnÃ¡lisis de vulnerabilidades y exposiciÃ³n de endpoints.

**Quedan excluidos del alcance:**
* Pruebas unitarias y de integraciÃ³n (aisladas).
* Flujo de autenticaciÃ³n OAuth real contra servidores de OSM de producciÃ³n en pruebas automatizadas E2E (se usarÃ¡n tokens de sesiÃ³n controlados).

---

## 2. Necesidades del Entorno

La siguiente tabla describe la configuraciÃ³n exacta requerida, alineada con la infraestructura de despliegue (`docker-compose.yml` y `docker-compose.e2e.yml`):

| Componente | EspecificaciÃ³n TÃ©cnica | ConfiguraciÃ³n de Contenedor |
| :--- | :--- | :--- |
| **Backend API** | FastAPI, Python 3.10+ | `ghcr.io/hotosm/tasking-manager/backend:main` (LÃ­mites: 1 CPU, 1.5GB RAM). Puerto expuesto (E2E): `:5000` |
| **Base de Datos** | PostgreSQL 14 / PostGIS 3.3 | `postgis/postgis:14-3.3`. Puerto expuesto (E2E): `:5434`. InicializaciÃ³n mediante Alembic. |
| **Frontend UI** | React, Node.js | `ghcr.io/hotosm/tasking-manager/frontend:main`. Expuesto vÃ­a Traefik en puerto `:3000` (Dev). |
| **OrquestaciÃ³n** | Docker Engine, Docker Compose | Red aislada: `tm-net`. |
| **AutomatizaciÃ³n E2E** | Playwright Test, Chromium | Configurado en `frontend/e2e` con entorno `E2E_BACKEND=real`. |

---

## 3. Criterios de AceptaciÃ³n y Rechazo

### 3.1. Criterios de AceptaciÃ³n
| Tipo de Prueba | Criterios MÃ­nimos Aprobatorios |
| :--- | :--- |
| **E2E Funcional** | 100% de los casos de flujos crÃ­ticos aprobados sin errores de bloqueo; ejecuciÃ³n del seed script idempotente exitosa. |
| **Rendimiento** | Tiempos de respuesta para endpoints crÃ­ticos (ej. guardado de tareas) en el percentil 95 (P95) < 2 segundos bajo carga base. 0% tasa de error. |
| **Seguridad** | 0 vulnerabilidades crÃ­ticas u altas identificadas (segÃºn OWASP Top 10) en anÃ¡lisis estÃ¡ticos o dinÃ¡micos. |

### 3.2. Criterios de Rechazo (SuspensiÃ³n)
* Defectos bloqueantes que impidan la autenticaciÃ³n o visualizaciÃ³n del mapa.
* Tasa de error superior al 5% durante las pruebas de carga iniciales.
* Consumo de recursos de backend superior al lÃ­mite de contenedor (1.5GB RAM, 1 CPU) induciendo caÃ­das por OOM (Out Of Memory).

---

## 4. Riesgos y Contingencias

| Riesgo | Probabilidad | Impacto | Estrategia de MitigaciÃ³n |
| :--- | :--- | :--- | :--- |
| Intermitencia de red y dependencia de OSM | Alta | Alto | Utilizar la funciÃ³n `storageState` de Playwright para inyectar tokens de autenticaciÃ³n firmados sin llamar a OAuth real. |
| Cuellos de botella en la inicializaciÃ³n de PostGIS | Media | Medio | Emplear `healthcheck` estricto de PostgreSQL en Docker y ejecutar dependencias (`tm-migration`) solo tras salud de BD. |
| Estado inconsistente de los datos de prueba | Baja | Alto | Ejecutar `scripts/e2e-seed.py` obligatoriamente antes de cada suite automatizada. |

---

## 5. Estrategia y Enfoques de Prueba

### 5.1. E2E Funcional
TÃ©cnica de caja negra validando flujos completos (Happy Paths) usando automatizaciÃ³n 100% con Playwright simulando navegadores Chromium, respaldado por la pre-carga controlada de usuarios (`e2e_mapper`, `e2e_admin`).

### 5.2. Rendimiento (Carga y EstrÃ©s)
Uso de herramientas de inyecciÃ³n de carga contra los endpoints de backend (`:5000`) mÃ¡s demandantes, priorizando aquellos con consultas espaciales en PostGIS (creaciÃ³n de AOI, listado de tareas espaciales).

### 5.3. Seguridad (AnÃ¡lisis de Vulnerabilidades)
EvaluaciÃ³n focalizada en Inyecciones SQL (PostGIS), controles de acceso a nivel de objeto (BOLA) y manejo adecuado de los tokens JWT de sesiÃ³n.

---

## 6. Entregables
* **Planes de Prueba:** Presente documento.
* **DiseÃ±os de Prueba:** Archivos detallados en `tests-docs/02-diseno-de-pruebas/sistema/`.
* **Scripts Automatizados:** Configurados en el repositorio (`frontend/e2e`).
* **Reportes de EjecuciÃ³n:** Informes resultantes tras la integraciÃ³n en GitHub Actions (CI/CD).



