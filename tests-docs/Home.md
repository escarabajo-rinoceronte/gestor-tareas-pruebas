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
  <b>Proyecto:</b> HOT Tasking Manager — Hito 3 Final: Sistema y Automatización Completa <br>
  <b>Fecha de Elaboración:</b> 19/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# HITO 3 — Pruebas de Software: Escarabajo Rinoceronte

**Repositorio:** [escarabajo-rinoceronte/gestor-tareas-pruebas](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas)

## Descripción General

Este repositorio contiene todos los artefactos producidos durante el **Hito 3** del proyecto de testing sobre **HOT OSM Tasking Manager**, una plataforma de código abierto utilizada mundialmente para coordinar el mapeo colaborativo en respuesta a emergencias humanitarias. El sistema cuenta con un backend en Python/FastAPI y un frontend en React/Vite, desplegados mediante Docker.

El esfuerzo de validación se concentró en tres módulos críticos del negocio: **Ejecución de Mapeo**, **Proceso de Validación** y **Administración de Proyectos**, abarcando pruebas unitarias, funcionales, de integración y de sistema (rendimiento, seguridad y E2E).

---

## Integrantes y Autoevaluación

| Nombre y Apellidos | Rol en el Sprint | % Esfuerzo Hito 3 |
|---|---|---|
| Quispe Arratea, Alexandra Raquel | Pruebas de Sistema (Desempeño y Seguridad) | 100% |
| Cari Lipe, Paul Andre | Pruebas de Integración y Unitarias Frontend | 100% |
| Arias Quispe, Jhonatan David | Pruebas de Sistema E2E y Bot de WhatsApp | 100% |
| Mamani Huarsaya Jorge | Pruebas de Integración y Unitarias Backend | 100% |
| Boza Portilla, Yordano Hernan | Pruebas de Integración (Backend) | 100% |
| Mollo Chuquicaña, Dolly Yadhira | Pruebas Funcionales | 100% |

---

## Artefactos del Hito 3

### 1. Plan de Pruebas Unitarias

Documento maestro que establece el alcance, la estrategia de pruebas, las herramientas, la arquitectura de entornos (DEV y QA), las métricas de calidad con umbral mínimo del 85% de cobertura, y los criterios de suspensión y reanudación.

- **GitHub Wiki:** https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/plan-pruebas-unitarias

---

### 2. Implementación de Pruebas Unitarias

#### Frontend (React/Vite)

Pruebas unitarias implementadas con Jest + React Testing Library sobre los componentes y vistas del frontend. Se desarrolló un script propio (coverage-rino) para medir la cobertura de los 3 módulos prioritarios, obteniendo métricas realistas de la lógica de negocio principal.

- **Reporte de Ejecución (Wiki):** https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/01-ejecucion-pruebas-unitarias-frontend
- **Pruebas ejecutadas:** más de 1,220 casos — **Tasa de éxito: 98.8%**
- **Cobertura alcanzada:** **85.32%** (Statements, Branches, Functions y Lines)
- **CI/CD Workflow:** GitHub Actions → .github/workflows/pr_test_frontend.yml (se ejecuta automáticamente en cada Pull Request)

#### Backend (FastAPI/Python)

Pruebas unitarias implementadas con pytest + pytest-cov sobre los módulos Core del backend (Modelos PostGIS y Servicios de Negocio). La estrategia incluyó estabilización de infraestructura de tests, incremento de cobertura en archivos críticos, y análisis de defectos de borde.

- **Diseño de Pruebas (Wiki):** https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/01-seguridad-usuarios-comms
- **Reporte de Ejecución (Wiki):** https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/02-ejecucion-pruebas-unitarias-backend
- **Pruebas ejecutadas:** 270 — **263 exitosas (97.4%)**
- **Cobertura alcanzada:** **~86%** en el Módulo Core (Modelos PostGIS: ~88%, Servicios: ~84%)

---

### 3. Informe de Pruebas Funcionales (Caja Negra)

Pruebas funcionales manuales aplicadas sobre **7 módulos del sistema** en un entorno QA controlado. Se aplicaron técnicas de caja negra: **Partición de Equivalencias (PE)** y **Análisis de Valores Límite (AVL)**, diseñando un total de **128 casos de prueba**.

El equipo elaboró el diseño completo para los 7 módulos y focalizó la **ejecución rigurosa con evidencia** en los **3 módulos priorizados** (flujos críticos del negocio), ejecutando **75 casos al 100%** con capturas de pantalla reales como evidencia.

| Módulo | Diseño de Casos | Ejecución con Evidencia |
|---|---|---|
| **MOD-01 Autenticación y Perfil** | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/01-autenticacion-perfil) | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/01-ejecucion-auntenticacion-perfil) |
| **MOD-02 Exploración de Proyectos** | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/02-exploracion-proyectos) | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/02-ejecucion-exploracion-proyectos) |
| **MOD-03 Ejecución de Mapeo** ⭐ | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/03-ejecucion-de-mapeo) | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/03-ejecucion-ejecucion-de-mapeo) |
| **MOD-04 Proceso de Validación** ⭐ | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/04-proceso-de-validacion) | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/04-ejecucion-proceso-de-validacion) |
| **MOD-05 Administración de Proyectos** ⭐ | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/05-administracion-de-proyectos) | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/05-ejecucion-administracion-de-proyectos) |
| **MOD-06 Gobernanza Organizaciones Equipos** | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/06-gobernanza-organizaciones-equipos) | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/06-ejecucion-gobernanza-organizaciones-equipos) |
| **MOD-07 Comunicación Notificaciones** | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/07-Comunicacion-notificaciones) | [Wiki](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/07-ejecucion-comunicacion-notificaciones) |

> Los módulos priorizados ⭐ representan los flujos críticos del sistema (bloqueo de tareas, validación de mapeo y gestión de proyectos). De los 75 casos ejecutados, **73 pasaron exitosamente (97.3%)** y 2 fallaron, cuyos defectos quedaron documentados. El diseño para los 7 módulos está disponible completo en la Wiki.

---

### 4. Pruebas de Integración

El proyecto base ya contaba con una serie de pruebas de integración rudimentarias. El esfuerzo del equipo consistió en refactorizar, estabilizar y crear nuevos casos de prueba robustos enfocándose estrictamente en los **3 módulos críticos**, alcanzando un **85% de cobertura**. 

**¿Por qué se eligieron estos módulos?**
Se seleccionaron debido a que manejan la **lógica de negocio principal** (asignación de tareas y validación) y los **datos sensibles/críticos** (autenticación y roles). Sin la correcta persistencia y comunicación de estos componentes con la base de datos PostGIS, la aplicación sería inoperable en situaciones de emergencia.

- **Plan de Integración (Wiki):** https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/plan-pruebas-integracion
- **Módulo Tareas/Mapeo:** https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/03-ejecucion-modulo-tareas-mapeo
- **Módulo Usuarios/Autenticación:** https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/04-ejecucion-modulo-usuarios-autenticacion
- **Módulo Proyectos:** https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/integration-projects-module

---

### 5. Pruebas de Sistema (ISO/IEC 25010)

Ejecución de pruebas de sistema automatizadas integradas al pipeline CI/CD. Los criterios de aceptación para estas pruebas fueron extraídos directamente de los requerimientos no funcionales del sistema (tiempos de respuesta < 2s) y los **estándares de calidad de software ISO/IEC 25010** (Evaluación del Producto).

- **Funcionalidad (Playwright E2E):** Ejecución de 3 flujos completos reales (Mapeo, Validación, Administración).
- **Eficiencia de Desempeño (K6):** Pruebas de carga y estrés con 50 VUs (Virtual Users) para validar la contención del servidor frente a tráfico recurrente de mapeadores.
- **Seguridad (SonarQube & Gitleaks):** Análisis SAST en más de 76,000 líneas de código y verificación estricta de ausencia de secretos/credenciales quemadas en el repositorio.
- **Reporte Consolidado (Wiki):** https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki/ejecucion-pruebas-sistema

---

### GitHub Projects (Tablero Kanban)

Gestión de issues y seguimiento del sprint bajo metodología ágil. Refleja la planificación, asignación y estado de cada tarea del Hito 3. Todas las tareas críticas finalizaron con estado **Done**.

- **GitHub Projects:** https://github.com/orgs/escarabajo-rinoceronte/projects/1/views/1

### GitHub Wiki (Documentación completa)

Portal de consulta unificado para todo el ciclo de pruebas (planes, diseños, informes de ejecución y evidencias).

- **Inicio Wiki:** https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas/wiki

### GitHub Actions (CI/CD) y Automatizaciones

El proyecto implementa pipelines de automatización clave utilizando GitHub Actions. Esto garantiza que la calidad, la seguridad y la documentación se validen de forma continua en cada cambio:

1. **Pipeline de Pruebas Frontend** (pr_test_frontend.yml): Ejecuta automáticamente la suite de pruebas unitarias de React ante cada Pull Request, actuando como compuerta de calidad obligatoria antes del merge.
2. **Pipeline de Pruebas Backend** (pr_test_backend.yml): Ejecuta validaciones de formato (PEP8), pruebas unitarias y pruebas de integración levantando automáticamente contenedores efímeros (PostGIS) en cada PR.
3. **Pruebas de Seguridad** (seguridad-sonarqube.yml): Automatiza el análisis de seguridad SAST ejecutando Gitleaks (escaneo de secretos) y SonarCloud en cada push a las ramas principales.
4. **Auto-Sincronización de la Wiki** (wiki-sync.yml): Detecta cambios en los informes Markdown y sincroniza la GitHub Wiki automáticamente en cada push a develop, incluyendo resolución de rutas de imágenes. Garantiza que la documentación refleje siempre el último estado real del proyecto sin intervención manual.

---

## Notas Técnicas

- La wiki se actualiza **automáticamente** al hacer push a develop mediante GitHub Actions.
- Las pruebas unitarias del frontend se ejecutan automáticamente en cada Pull Request.
- Método estadístico utilizado en diseño de pruebas funcionales: **Partición de Equivalencias (PE)** y **Análisis de Valores Límite (AVL)**.
