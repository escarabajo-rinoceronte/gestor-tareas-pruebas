<style>
  .cover-page {
    max-width: 700px;
    margin: 0 auto;
    padding: 60px 50px;
    font-family: 'Georgia', 'Times New Roman', serif;
    text-align: center;
    color: #1a1a1a;
    border-top: 4px solid #8B0000;
    border-bottom: 4px solid #8B0000;
  }
  .cover-page .institucion { font-size: 20px; font-weight: 700; letter-spacing: 0.05em; margin: 0 0 6px; text-transform: uppercase; }
  .cover-page .facultad, .cover-page .escuela { font-size: 14px; font-weight: 400; color: #444; margin: 0 0 4px; line-height: 1.4; }
  .cover-page .logo-wrap { margin: 32px auto; width: 130px; height: 130px; display: flex; align-items: center; justify-content: center; }
  .cover-page .logo-wrap img { max-width: 100%; max-height: 100%; }
  .cover-page .ficha { display: inline-block; text-align: left; margin-top: 20px; border-top: 1px solid #ddd; padding-top: 20px; }
  .cover-page .ficha table { border-collapse: collapse; }
  .cover-page .ficha td { padding: 6px 14px 6px 0; font-size: 13px; vertical-align: top; }
  .cover-page .ficha td.label { color: #777; font-weight: 600; white-space: nowrap; text-transform: uppercase; font-size: 11px; letter-spacing: 0.03em; }
  .cover-page .ubicacion { margin-top: 36px; font-size: 13px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #8B0000; }
</style>

<div class="cover-page">
  <p class="institucion">Universidad Nacional de San Agustín</p>
  <p class="facultad">Facultad de Ingeniería de Producción y Servicios</p>
  <p class="escuela">Escuela Profesional de Ingeniería de Sistemas</p>

  <div class="logo-wrap">
    <img src="/tests-docs/logo-unsa.png" alt="Logo UNSA" />
  </div>

  <div class="ficha">
    <table>
      <tr><td class="label">Curso</td><td>Pruebas de Software</td></tr>
      <tr><td class="label">Docente</td><td>Ing. Robert Edison Arisaca Mamani</td></tr>
      <tr><td class="label">Semestre</td><td>VII</td></tr>
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — Reporte de EjecuciÃ³n de Pruebas: MÃ³dulo de Tareas, Mapeo y ValidaciÃ³n (Mapping & Validation)</td></tr>
      <tr><td class="label">Fecha</td><td>15/07/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# Reporte de EjecuciÃ³n de Pruebas: MÃ³dulo de Tareas, Mapeo y ValidaciÃ³n (Mapping & Validation)

Este documento registra el proceso de ejecuciÃ³n y la evoluciÃ³n de la cobertura de las pruebas de integraciÃ³n correspondientes al mÃ³dulo de Tareas y Mapeo, estructurado conforme a las prÃ¡cticas de documentaciÃ³n tÃ©cnica. El reporte detalla la mediciÃ³n del estado base, las iteraciones de ampliaciÃ³n de casos de prueba y los resultados de cobertura en su fase final.

---

## 1. Fase Inicial: MediciÃ³n del Estado Base

### 1.1. Alcance de la ejecuciÃ³n

La evaluaciÃ³n inicial se focalizÃ³ sobre el cÃ³digo fuente operativo del dominio de **Mapping & Validation**. Se ejecutaron 13 suites de pruebas de integraciÃ³n, aislando el anÃ¡lisis sobre los componentes: servicios de tareas, controladores HTTP, modelo ORM (PostGIS) y los objetos de transferencia de datos (DTOs) involucrados en el mÃ³dulo.

### 1.2. Procedimiento de EjecuciÃ³n (Fase Inicial)

Para recopilar la cobertura base, se ejecutaron las pruebas con el siguiente comando en el entorno de contenedores:

```sh
docker compose exec -T tm-backend coverage run -m pytest tests/api/integration/services/test_mapping_service.py tests/api/integration/services/test_validation_service.py tests/api/integration/services/grid/test_split_service.py tests/api/integration/api/tasks/ tests/api/integration/api/projects/test_activities.py tests/api/integration/api/projects/test_contributions.py tests/api/integration/api/users/test_tasks.py tests/api/integration/api/users/test_resources.py tests/api/integration/api/users/test_statistics.py tests/api/integration/api/projects/test_statistics.py tests/api/integration/api/system/test_statistics.py -p no:warnings
```

Y para la generaciÃ³n del reporte tÃ©cnico acotado al mÃ³dulo:

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

### 1.3. Resultados de ejecuciÃ³n y cobertura base

| MÃ©trica | Resultado |
| :--- | :--- |
| MÃ³dulo evaluado | Mapping & Validation (Tareas) |
| Nivel de pruebas | IntegraciÃ³n |
| Pruebas ejecutadas | 185 |
| Pruebas fallidas | 0 |
| Componentes evaluados | 11 archivos |
| LÃ­neas ejecutables totales | 1766 |
| LÃ­neas no cubiertas | 361 |
| Cobertura de sentencias | 80% |
| Tiempo de ejecuciÃ³n | 67.51 s |

### 1.4. Cobertura por componente (Estado Inicial)

| Componente | Stmts | Miss | Cover | ObservaciÃ³n TÃ©cnica |
| :--- | ---: | ---: | ---: | :--- |
| `backend/api/tasks/__init__.py` | 0 | 0 | 100% | InicializaciÃ³n del mÃ³dulo, sin lÃ³gica. |
| `backend/api/tasks/actions.py` | 251 | 69 | 73% | Carencia de validaciÃ³n en bifurcaciones de error. |
| `backend/api/tasks/resources.py` | 109 | 46 | 58% | Ausencia de comprobaciones en filtros y parÃ¡metros HTTP. |
| `backend/api/tasks/statistics.py` | 24 | 0 | 100% | ValidaciÃ³n integral confirmada. |
| `backend/models/dtos/grid_dto.py` | 14 | 0 | 100% | ValidaciÃ³n integral confirmada. |
| `backend/models/dtos/mapping_dto.py` | 85 | 7 | 92% | Cobertura alta en transformaciones de entrada. |
| `backend/models/dtos/validator_dto.py` | 126 | 27 | 79% | Casos de excepciÃ³n de validaciÃ³n omitidos. |
| `backend/models/postgis/task.py` | 604 | 161 | 73% | Trazabilidad histÃ³rica (TaskHistory) parcialmente evaluada. |
| `backend/services/grid/split_service.py` | 129 | 1 | 99% | ValidaciÃ³n matemÃ¡tica geoespacial verificada. |
| `backend/services/mapping_service.py` | 215 | 18 | 92% | Cobertura sÃ³lida en manejo transaccional. |
| `backend/services/validator_service.py` | 209 | 32 | 85% | ValidaciÃ³n de estado operativo confirmada. |

### 1.5. InterpretaciÃ³n tÃ©cnica

El anÃ¡lisis del estado base evidenciÃ³ una cobertura estable en la capa de servicios, contrastando con varianzas significativas en la capa de exposiciÃ³n (controladores HTTP). Los componentes `backend/api/tasks/resources.py` y `actions.py` presentaban Ã¡reas de ejecuciÃ³n omitidas en relaciÃ³n a peticiones mal formadas y restricciones de autorizaciÃ³n. Con base en este diagnÃ³stico, se determinÃ³ la factibilidad tÃ©cnica de ampliar los escenarios de prueba.

---

## 2. Fase Intermedia: AmpliaciÃ³n de Escenarios de Prueba

A partir de los resultados iniciales, se integraron nuevos casos de prueba orientados a operaciones funcionales complejas, flujos masivos y gestiÃ³n de auditorÃ­as.

### 2.1. Escenarios incorporados e incidentes detectados

- **AdiciÃ³n de `test_bulk_actions.py`**: Suites enfocadas en procesamiento masivo (`map-all`, `validate-all`, `invalidate-all`, `reset-all`). Su ejecuciÃ³n ampliÃ³ la trazabilidad de sentencias en el componente `actions.py`.
- **AdiciÃ³n de `test_reversions.py`**: Pruebas dirigidas a flujos de control inverso (reversiones de tareas) y extensiones de vida Ãºtil de bloqueos de base de datos.
- **AuditorÃ­a en `test_resources.py`**: Se agregaron aserciones sobre endpoints de consulta. Durante esta ejecuciÃ³n se detectÃ³ un incidente de control de acceso defectuoso en `get_invalidated_tasks`. La incidencia fue documentada y subsanada, restableciendo las polÃ­ticas de seguridad en la lectura de historiales.

### 2.2. Resultados de ejecuciÃ³n (Fase Intermedia)

| MÃ©trica | Resultado |
| :--- | :--- |
| MÃ³dulo evaluado | Mapping & Validation (Tareas) |
| Nivel de pruebas | IntegraciÃ³n |
| Pruebas ejecutadas | 206 (+21) |
| Pruebas fallidas | 0 |
| LÃ­neas ejecutables totales | 1798 |
| LÃ­neas no cubiertas | 283 |
| Cobertura de sentencias | 84% (+4%) |
| Tiempo de ejecuciÃ³n | 78.71 s |

---

## 3. Fase Final: ResoluciÃ³n ASGI e Intersecciones Geoespaciales

Las pruebas finales se diseÃ±aron para abarcar flujos de eliminaciÃ³n estructurada, peticiones complejas con formatos cartogrÃ¡ficos y la estabilidad del pipeline asÃ­ncrono.

### 3.1. Escenarios finales y refactorizaciÃ³n tÃ©cnica

- **VerificaciÃ³n de eliminaciÃ³n (`TestDeleteTasksAPI`)**: Se implementaron aserciones sobre `DELETE /api/v2/projects/{project_id}/tasks/`, verificando el comportamiento del sistema ante fallos de autorizaciÃ³n y discrepancias en la estructura de datos (JSON schemas).
- **Consultas espaciales (`TestGridIntersectingAPI`)**: Se validÃ³ el procesamiento del payload GeoJSON para la intersecciÃ³n de cuadrÃ­culas en `PUT /api/v2/projects/{project_id}/tasks/queries/aoi/`.
- **MitigaciÃ³n de bloqueos asÃ­ncronos**: Durante la ejecuciÃ³n de los nuevos endpoints transaccionales, se presentÃ³ el error tÃ©cnico `TypeError("'coroutine' object is not iterable")` en el proceso de serializaciÃ³n ASGI (FastAPI). El anÃ¡lisis determinÃ³ que decoradores de seguridad personalizados (como `@tm.pm_only()`) no procesaban correctamente firmas `async def`. El fallo fue parcheado refactorizando la inspecciÃ³n de corrutinas en `backend/api/utils.py`, lo que restableciÃ³ la integridad de la API.

### 3.2. Procedimiento de EjecuciÃ³n y Evidencia (Fase Final)

La ejecuciÃ³n final se llevÃ³ a cabo conservando los parÃ¡metros de integraciÃ³n (omitiendo warnings y activando la cobertura detallada):

```sh
docker compose exec -T tm-backend coverage run -m pytest tests/api/integration/services/test_mapping_service.py tests/api/integration/services/test_validation_service.py tests/api/integration/services/grid/test_split_service.py tests/api/integration/api/tasks/ tests/api/integration/api/projects/test_activities.py tests/api/integration/api/projects/test_contributions.py tests/api/integration/api/users/test_tasks.py tests/api/integration/api/users/test_resources.py tests/api/integration/api/users/test_statistics.py tests/api/integration/api/projects/test_statistics.py tests/api/integration/api/system/test_statistics.py -p no:warnings -q
```

GeneraciÃ³n del reporte final:

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

### 3.3. Resultados de ejecuciÃ³n (Final)

| MÃ©trica | Resultado | VariaciÃ³n Total (Vs. Inicial) |
| :--- | :--- | :--- |
| MÃ³dulo evaluado | Mapping & Validation (Tareas) | - |
| Nivel de pruebas | IntegraciÃ³n | - |
| Pruebas ejecutadas | 240 | +55 pruebas ejecutadas |
| Pruebas fallidas | 0 | - |
| Componentes evaluados | 11 archivos | - |
| LÃ­neas ejecutables totales | 1800 | +34 lÃ­neas modificadas/aÃ±adidas |
| LÃ­neas no cubiertas | 262 | -99 lÃ­neas residuales cubiertas |
| Cobertura de sentencias | 85% | +5% cobertura global |
| Tiempo de ejecuciÃ³n | 70.42 s | Mantenido estable |

### 3.4. Cobertura por componente (Final)

| Componente | Stmts | Miss | Cover | VariaciÃ³n de Cobertura |
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

## 4. Conclusiones TÃ©cnicas de la EjecuciÃ³n

La iteraciÃ³n sobre los casos de prueba resultÃ³ en la adiciÃ³n de 55 escenarios funcionales. Se verificÃ³ el funcionamiento correcto de las transacciones de mapeo, manejo de polÃ­gonos y control de acceso.

**InterpretaciÃ³n de la EvoluciÃ³n TÃ©cnica:**
1. **Capa de Controladores:** La refactorizaciÃ³n y adiciÃ³n de pruebas en la interfaz HTTP (`resources.py` y `actions.py`) resultÃ³ en incrementos de cobertura del 31% y 17% respectivamente, comprobando las respuestas del enrutador ante entradas anÃ³malas.
2. **Estabilidad AsÃ­ncrona:** La inyecciÃ³n de pruebas integrales permitiÃ³ la detecciÃ³n de bloqueos de serializaciÃ³n ASGI. Tras las correcciones en los decoradores, el sistema maneja flujos asÃ­ncronos concurrentes de forma estable.
3. **LÃ³gica de Negocio:** Las pruebas confirmaron que los servicios nÃºcleo operan segÃºn las especificaciones tÃ©cnicas, cubriendo satisfactoriamente validaciones espaciales, transaccionales y de acceso.

El mÃ³dulo de Mapping & Validation cumple con los criterios tÃ©cnicos requeridos, evidenciando resiliencia frente a manipulaciones anÃ³malas y peticiones concurrentes.

