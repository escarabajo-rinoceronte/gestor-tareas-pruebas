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
  <b>Proyecto:</b> HOT Tasking Manager — Reporte de Ejecución de Pruebas: Módulo de Tareas, Mapeo y Validación (Mapping & Validation) <br>
  <b>Fecha de Elaboración:</b> 15/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Reporte de Ejecución de Pruebas: Módulo de Tareas, Mapeo y Validación (Mapping & Validation)

Este documento registra el proceso de ejecución y la evolución de la cobertura de las pruebas de integración correspondientes al módulo de Tareas y Mapeo, estructurado conforme a las prácticas de documentación técnica. El reporte detalla la medición del estado base, las iteraciones de ampliación de casos de prueba y los resultados de cobertura en su fase final.

---

## 1. Fase Inicial: Medición del Estado Base

### 1.1. Alcance de la ejecución

La evaluación inicial se focalizó sobre el código fuente operativo del dominio de **Mapping & Validation**. Se ejecutaron 13 suites de pruebas de integración, aislando el análisis sobre los componentes: servicios de tareas, controladores HTTP, modelo ORM (PostGIS) y los objetos de transferencia de datos (DTOs) involucrados en el módulo.

### 1.2. Procedimiento de Ejecución (Fase Inicial)

Para recopilar la cobertura base, se ejecutaron las pruebas con el siguiente comando en el entorno de contenedores:

```sh
docker compose exec -T tm-backend coverage run -m pytest tests/api/integration/services/test_mapping_service.py tests/api/integration/services/test_validation_service.py tests/api/integration/services/grid/test_split_service.py tests/api/integration/api/tasks/ tests/api/integration/api/projects/test_activities.py tests/api/integration/api/projects/test_contributions.py tests/api/integration/api/users/test_tasks.py tests/api/integration/api/users/test_resources.py tests/api/integration/api/users/test_statistics.py tests/api/integration/api/projects/test_statistics.py tests/api/integration/api/system/test_statistics.py -p no:warnings
```

Y para la generación del reporte técnico acotado al módulo:

```sh
docker compose exec -T tm-backend coverage report -m --include="backend/api/tasks/*.py,backend/services/mapping_service.py,backend/services/validator_service.py,backend/services/grid/split_service.py,backend/models/postgis/task.py,backend/models/dtos/mapping_dto.py,backend/models/dtos/validator_dto.py,backend/models/dtos/grid_dto.py"
```

**Fragmento del Registro de Pruebas (Test Log - Inicial):**
```sh
============================= test session starts ==============================
platform linux -- Python 3.10.20, pytest-8.3.5, pluggy-1.5.0
collected 185 items

tests/api/integration/services/test_mapping_service.py .......           [  3%]
...
tests/api/integration/api/tasks/test_actions.py ........................ [ 22%]
...
tests/api/integration/api/tasks/test_resources.py .................      [ 59%]
...
======================== 185 passed in 67.51s (0:01:07) ========================
```

### 1.3. Resultados de ejecución y cobertura base

| Métrica | Resultado |
| :--- | :--- |
| Módulo evaluado | Mapping & Validation (Tareas) |
| Nivel de pruebas | Integración |
| Pruebas ejecutadas | 185 |
| Pruebas fallidas | 0 |
| Componentes evaluados | 11 archivos |
| Líneas ejecutables totales | 1766 |
| Líneas no cubiertas | 361 |
| Cobertura de sentencias | 80% |
| Tiempo de ejecución | 67.51 s |

### 1.4. Cobertura por componente (Estado Inicial)

| Componente | Stmts | Miss | Cover | Observación Técnica |
| :--- | ---: | ---: | ---: | :--- |
| `backend/api/tasks/__init__.py` | 0 | 0 | 100% | Inicialización del módulo, sin lógica. |
| `backend/api/tasks/actions.py` | 251 | 69 | 73% | Carencia de validación en bifurcaciones de error. |
| `backend/api/tasks/resources.py` | 109 | 46 | 58% | Ausencia de comprobaciones en filtros y parámetros HTTP. |
| `backend/api/tasks/statistics.py` | 24 | 0 | 100% | Validación integral confirmada. |
| `backend/models/dtos/grid_dto.py` | 14 | 0 | 100% | Validación integral confirmada. |
| `backend/models/dtos/mapping_dto.py` | 85 | 7 | 92% | Cobertura alta en transformaciones de entrada. |
| `backend/models/dtos/validator_dto.py` | 126 | 27 | 79% | Casos de excepción de validación omitidos. |
| `backend/models/postgis/task.py` | 604 | 161 | 73% | Trazabilidad histórica (TaskHistory) parcialmente evaluada. |
| `backend/services/grid/split_service.py` | 129 | 1 | 99% | Validación matemática geoespacial verificada. |
| `backend/services/mapping_service.py` | 215 | 18 | 92% | Cobertura sólida en manejo transaccional. |
| `backend/services/validator_service.py` | 209 | 32 | 85% | Validación de estado operativo confirmada. |

### 1.5. Interpretación técnica

El análisis del estado base evidenció una cobertura estable en la capa de servicios, contrastando con varianzas significativas en la capa de exposición (controladores HTTP). Los componentes `backend/api/tasks/resources.py` y `actions.py` presentaban áreas de ejecución omitidas en relación a peticiones mal formadas y restricciones de autorización. Con base en este diagnóstico, se determinó la factibilidad técnica de ampliar los escenarios de prueba.

---

## 2. Fase Intermedia: Ampliación de Escenarios de Prueba

A partir de los resultados iniciales, se integraron nuevos casos de prueba orientados a operaciones funcionales complejas, flujos masivos y gestión de auditorías.

### 2.1. Escenarios incorporados e incidentes detectados

- **Adición de `test_bulk_actions.py`**: Suites enfocadas en procesamiento masivo (`map-all`, `validate-all`, `invalidate-all`, `reset-all`). Su ejecución amplió la trazabilidad de sentencias en el componente `actions.py`.
- **Adición de `test_reversions.py`**: Pruebas dirigidas a flujos de control inverso (reversiones de tareas) y extensiones de vida útil de bloqueos de base de datos.
- **Auditoría en `test_resources.py`**: Se agregaron aserciones sobre endpoints de consulta. Durante esta ejecución se detectó un incidente de control de acceso defectuoso en `get_invalidated_tasks`. La incidencia fue documentada y subsanada, restableciendo las políticas de seguridad en la lectura de historiales.

### 2.2. Resultados de ejecución (Fase Intermedia)

| Métrica | Resultado |
| :--- | :--- |
| Módulo evaluado | Mapping & Validation (Tareas) |
| Nivel de pruebas | Integración |
| Pruebas ejecutadas | 206 (+21) |
| Pruebas fallidas | 0 |
| Líneas ejecutables totales | 1798 |
| Líneas no cubiertas | 283 |
| Cobertura de sentencias | 84% (+4%) |
| Tiempo de ejecución | 78.71 s |

---

## 3. Fase Final: Resolución ASGI e Intersecciones Geoespaciales

Las pruebas finales se diseñaron para abarcar flujos de eliminación estructurada, peticiones complejas con formatos cartográficos y la estabilidad del pipeline asíncrono.

### 3.1. Escenarios finales y refactorización técnica

- **Verificación de eliminación (`TestDeleteTasksAPI`)**: Se implementaron aserciones sobre `DELETE /api/v2/projects/{project_id}/tasks/`, verificando el comportamiento del sistema ante fallos de autorización y discrepancias en la estructura de datos (JSON schemas).
- **Consultas espaciales (`TestGridIntersectingAPI`)**: Se validó el procesamiento del payload GeoJSON para la intersección de cuadrículas en `PUT /api/v2/projects/{project_id}/tasks/queries/aoi/`.
- **Mitigación de bloqueos asíncronos**: Durante la ejecución de los nuevos endpoints transaccionales, se presentó el error técnico `TypeError("'coroutine' object is not iterable")` en el proceso de serialización ASGI (FastAPI). El análisis determinó que decoradores de seguridad personalizados (como `@tm.pm_only()`) no procesaban correctamente firmas `async def`. El fallo fue parcheado refactorizando la inspección de corrutinas en `backend/api/utils.py`, lo que restableció la integridad de la API.

### 3.2. Procedimiento de Ejecución y Evidencia (Fase Final)

La ejecución final se llevó a cabo conservando los parámetros de integración (omitiendo warnings y activando la cobertura detallada):

```sh
docker compose exec -T tm-backend coverage run -m pytest tests/api/integration/services/test_mapping_service.py tests/api/integration/services/test_validation_service.py tests/api/integration/services/grid/test_split_service.py tests/api/integration/api/tasks/ tests/api/integration/api/projects/test_activities.py tests/api/integration/api/projects/test_contributions.py tests/api/integration/api/users/test_tasks.py tests/api/integration/api/users/test_resources.py tests/api/integration/api/users/test_statistics.py tests/api/integration/api/projects/test_statistics.py tests/api/integration/api/system/test_statistics.py -p no:warnings -q
```

Generación del reporte final:

```sh
docker compose exec -T tm-backend coverage report -m --include="backend/api/tasks/*.py,backend/services/mapping_service.py,backend/services/validator_service.py,backend/services/grid/split_service.py,backend/models/postgis/task.py,backend/models/dtos/mapping_dto.py,backend/models/dtos/validator_dto.py,backend/models/dtos/grid_dto.py"
```

**Fragmento del Registro de Pruebas (Test Log - Final):**
```sh
........................................................................ [ 30%]
........................................................................ [ 60%]
........................................................................ [ 90%]
........................                                                 [100%]
240 passed in 70.42s (0:01:10)

Name                                     Stmts   Miss  Cover   Missing
----------------------------------------------------------------------
backend/api/tasks/__init__.py                0      0   100%
backend/api/tasks/actions.py               251     24    90%   105-107, 206-210, 307-309, 331-333, 396, 480, 492, 574, 660, 1029-1032, 1047, 1210
backend/api/tasks/resources.py             121     13    89%   133-139, 161, 199-200, 386-387, 493, 499, 503, 505, 508
backend/api/tasks/statistics.py             24      0   100%
backend/models/dtos/grid_dto.py             14      0   100%
backend/models/dtos/mapping_dto.py          85      7    92%   13-21
backend/models/dtos/validator_dto.py       123     25    80%   23-26, 29-32, 39-51, 56-67, 213, 219-220
backend/models/postgis/task.py             604    158    74%   101-103, 141-145, 158-176, 245-258, 289-292, 295-299, 302, 339-341, 348, 356, 367, 501-525, 532-567, 592-606, 659-676, 744, 749, 752, 765-766, 771, 858-869, 878-907, 914-926, 965-971, 992-1018, 1089, 1125-1129, 1143-1178, 1430-1431, 1435-1441, 1446-1449, 1486-1513, 1584, 1655-1680, 1732-1739, 1782-1783, 1819-1850
backend/services/grid/split_service.py     130      1    99%   304
backend/services/mapping_service.py        215     18    92%   115, 122-127, 256-282, 334, 347, 377, 390, 435-438
backend/services/validator_service.py      233     16    93%   117-138, 153, 404, 410-411, 414-415, 452, 585
----------------------------------------------------------------------
TOTAL                                     1800    262    85%
```

### 3.3. Resultados de ejecución (Final)

| Métrica | Resultado | Variación Total (Vs. Inicial) |
| :--- | :--- | :--- |
| Módulo evaluado | Mapping & Validation (Tareas) | - |
| Nivel de pruebas | Integración | - |
| Pruebas ejecutadas | 240 | +55 pruebas ejecutadas |
| Pruebas fallidas | 0 | - |
| Componentes evaluados | 11 archivos | - |
| Líneas ejecutables totales | 1800 | +34 líneas modificadas/añadidas |
| Líneas no cubiertas | 262 | -99 líneas residuales cubiertas |
| Cobertura de sentencias | 85% | +5% cobertura global |
| Tiempo de ejecución | 70.42 s | Mantenido estable |

### 3.4. Cobertura por componente (Final)

| Componente | Stmts | Miss | Cover | Variación de Cobertura |
| :--- | ---: | ---: | ---: | :--- |
| `backend/api/tasks/__init__.py` | 0 | 0 | 100% | 0% |
| `backend/api/tasks/actions.py` | 251 | 24 | 90% | +17% |
| `backend/api/tasks/resources.py` | 121 | 13 | 89% | +31% |
| `backend/api/tasks/statistics.py` | 24 | 0 | 100% | 0% |
| `backend/models/dtos/grid_dto.py` | 14 | 0 | 100% | 0% |
| `backend/models/dtos/mapping_dto.py` | 85 | 7 | 92% | 0% |
| `backend/models/dtos/validator_dto.py` | 123 | 25 | 80% | +1% |
| `backend/models/postgis/task.py` | 604 | 158 | 74% | +1% |
| `backend/services/grid/split_service.py` | 130 | 1 | 99% | 0% |
| `backend/services/mapping_service.py` | 215 | 18 | 92% | 0% |
| `backend/services/validator_service.py` | 233 | 16 | 93% | +8% |
| **TOTAL** | **1800** | **262** | **85%** | **+5%** |

---

## 4. Conclusiones Técnicas de la Ejecución

La iteración sobre los casos de prueba resultó en la adición de 55 escenarios funcionales. Se verificó el funcionamiento correcto de las transacciones de mapeo, manejo de polígonos y control de acceso.

**Interpretación de la Evolución Técnica:**
1. **Capa de Controladores:** La refactorización y adición de pruebas en la interfaz HTTP (`resources.py` y `actions.py`) resultó en incrementos de cobertura del 31% y 17% respectivamente, comprobando las respuestas del enrutador ante entradas anómalas.
2. **Estabilidad Asíncrona:** La inyección de pruebas integrales permitió la detección de bloqueos de serialización ASGI. Tras las correcciones en los decoradores, el sistema maneja flujos asíncronos concurrentes de forma estable.
3. **Lógica de Negocio:** Las pruebas confirmaron que los servicios núcleo operan según las especificaciones técnicas, cubriendo satisfactoriamente validaciones espaciales, transaccionales y de acceso.

El módulo de Mapping & Validation cumple con los criterios técnicos requeridos, evidenciando resiliencia frente a manipulaciones anómalas y peticiones concurrentes.



