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
  <b>Proyecto:</b> HOT Tasking Manager — Reporte de Ejecución: Módulo de Servicios Core y Lógica de Negocio <br>
  <b>Fecha de Elaboración:</b> 24/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Reporte de Ejecución: Módulo de Servicios Core y Lógica de Negocio

Este documento contiene los resultados de la ejecución de las pruebas unitarias correspondientes a los servicios transaccionales críticos del módulo **Servicios Core y Lógica de Negocio**.

El objetivo principal de esta primera fase fue auditar el estado base de la arquitectura operativa (descartando dependencias de otros dominios como autenticación y mensajería), logrando una medición inicial de cobertura del **52%**, la cual servirá como punto de partida para futuras expansiones.

---

## 1. Alcance de la cobertura

La cobertura se calculó sobre los archivos fuente propios de los **Servicios Core**. Se ejecutaron suites de pruebas unitarias aislando mediante *mocks* y *fixtures* los servicios de proyectos, mapeos, validaciones, divisiones geométricas, organizaciones, equipos y campañas.

### Resultado general

| Métrica                       | Resultado                                         |
| :---------------------------- | :------------------------------------------------ |
| Módulo evaluado               | Servicios Core y Lógica de Negocio                |
| Tipo de pruebas               | Unitarias                                         |
| Pruebas ejecutadas            | 88                                                |
| Pruebas exitosas              | 88                                                |
| Pruebas fallidas              | 0                                                 |
| Archivos medidos              | 9                                                 |
| Líneas ejecutables analizadas | 2319                                              |
| Líneas no cubiertas           | 1105                                              |
| Cobertura total               | **52%**                                           |

### Cobertura por archivo

| Archivo                                        |    Stmts |    Miss |   Cover |
| :--------------------------------------------- | -------: | ------: | ------: |
| `backend/services/campaign_service.py`         |      172 |      76 |     56% |
| `backend/services/grid/split_service.py`       |      130 |      30 |     77% |
| `backend/services/mapping_service.py`          |      215 |      60 |     72% |
| `backend/services/organisation_service.py`     |      195 |      82 |     58% |
| `backend/services/project_admin_service.py`    |      194 |     101 |     48% |
| `backend/services/project_search_service.py`   |      424 |     231 |     46% |
| `backend/services/project_service.py`          |      368 |     193 |     48% |
| `backend/services/team_service.py`             |      388 |     212 |     45% |
| `backend/services/validator_service.py`        |      233 |     120 |     48% |
| **TOTAL**                                      | **2319** | **1105** | **52%** |

---

## 2. Ejecución de pruebas unitarias

Se ejecutaron las pruebas unitarias correspondientes al módulo empleando el siguiente comando, asegurando el entorno asíncrono y suprimiendo advertencias externas:

```sh
docker compose exec -T tm-backend coverage run -m pytest tests/api/unit/services/test_project_service.py tests/api/unit/services/test_organisation_service.py tests/api/unit/services/test_mapping_service.py tests/api/unit/services/test_validator_service.py tests/api/unit/services/grid/ tests/api/unit/services/test_team_service.py tests/api/unit/services/test_campaign_service.py tests/api/unit/services/test_project_admin_service.py tests/api/unit/services/test_project_search_service.py -p no:warnings
```

### Resultado de la ejecución (Log)

```sh
WARN[0000] The "DEFAULT_VALIDATOR_TEAM_ID" variable is not set. Defaulting to a blank string.
.......................................................................
........................................................................ [ 81%]
................
................                                                         [100%]
88 passed in 14.48s
```

---

## 3. Reporte de cobertura ejecutado

Para generar el reporte validando exclusivamente las capas operativas del módulo, se ejecutó:

```sh
docker compose exec -T tm-backend coverage report -m --include="backend/services/project_service.py,backend/services/organisation_service.py,backend/services/mapping_service.py,backend/services/validator_service.py,backend/services/grid/split_service.py,backend/services/team_service.py,backend/services/campaign_service.py,backend/services/project_admin_service.py,backend/services/project_search_service.py"
```

### Resultado del reporte (Log)

```sh
Name                                         Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------
backend/services/campaign_service.py           172     76    56%   ...
backend/services/grid/split_service.py         130     30    77%   ...
backend/services/mapping_service.py            215     60    72%   ...
backend/services/organisation_service.py       195     82    58%   ...
backend/services/project_admin_service.py      194    101    48%   ...
backend/services/project_search_service.py     424    231    46%   ...
backend/services/project_service.py            368    193    48%   ...
backend/services/team_service.py               388    212    45%   ...
backend/services/validator_service.py          233    120    48%   ...
--------------------------------------------------------------------------
TOTAL                                         2319   1105    52%
```

---

## 4. Análisis de resultados

La auditoría actual demuestra una cobertura unitaria base del **52%**. Si bien los **88 escenarios evaluados** confirman el funcionamiento íntegro de los caminos felices transaccionales (al no reportar ningún fallo de ejecución), persisten brechas considerables en flujos de error y validaciones complejas.

Los componentes con **mejor cobertura** estructural son:

| Archivo | Cobertura | Interpretación |
| :--- | ---: | :--- |
| `grid/split_service.py` | 77% | El procesamiento geoespacial y subdivisión de cuadrículas presenta una validación profunda. |
| `mapping_service.py` | 72% | El servicio core transaccional maneja bloqueos de forma controlada y cuenta con buen nivel de pruebas unitarias. |
| `organisation_service.py` | 58% | Validaciones de creación y obtención operan correctamente bajo roles estandarizados. |

Los componentes con **menor cobertura** y mayor riesgo técnico son:

| Archivo | Cobertura | Observación |
| :--- | ---: | :--- |
| `project_service.py` | 48% | Abundancia de lógica condicional y ramas de validación (como permisos específicos) sin testear. |
| `validator_service.py` | 48% | Escenarios de rollback e inconsistencias transaccionales están omitidos en las pruebas. |
| `project_search_service.py` | 46% | Gran cantidad de ramas originadas por filtros dinámicos carecen de evaluación unitaria aislada. |
| `team_service.py` | 45% | La manipulación de jerarquías y membresías no alcanza siquiera el 50% de líneas probadas. |

---

## 5. Alcance y nivel de confianza actual

| Dimensión | Alcance | Nivel de Confianza | Observaciones |
| :--- | :--- | :--- | :--- |
| **Operaciones Core de Tareas (Mapping)** | 72% | **Medio-Alto** | La concurrencia básica de tareas está garantizada. |
| **División Geométrica (Grid)** | 77% | **Alto** | La manipulación de los polígonos asimétricos y cuadrados es robusta. |
| **Administración de Proyectos (Project/Admin/Search)** | < 50% | **Bajo** | Falta validación para filtros y fallas en permisos HTTP inyectados. |
| **Roles, Organizaciones y Equipos** | 45 - 58% | **Medio-Bajo** | Vulnerable a escenarios de "Broken Access Control" debido a la baja cobertura. |

---

## 6. Conclusión del Estado Actual

El entorno local para la suite de **Servicios Core** ha sido estabilizado, erradicando los falsos negativos de infraestructura asíncrona. No obstante, con una cobertura total del **52%** y **1105 líneas no cubiertas**, el módulo requiere un plan de mitigación intensivo basado en Test-Driven Development (TDD) para simular inyecciones de error de base de datos (`IntegrityError`) y aserciones de control de roles (`403 Forbidden`). Este estado base proporciona la métrica real que servirá de pilar para las siguientes fases del proyecto de pruebas.

---

## 7. Ejecución de Pruebas Unitarias (Fase 2)

Se ejecutaron las siguientes suites de pruebas unitarias para el módulo actual. No se agregaron nuevas suites y se optó por agregar más casos de pruebas para las suites existentes:

```sh
============================= test session starts ==============================
platform linux -- Python 3.10.20, pytest-8.3.5, pluggy-1.5.0
rootdir: /usr/src/app
configfile: pyproject.toml
plugins: anyio-4.9.0, cov-7.1.0
collected 124 items

tests/api/unit/services/test_project_service.py .......................  [ 18%]
tests/api/unit/services/test_organisation_service.py ...........         [ 27%]
tests/api/unit/services/test_mapping_service.py ..................       [ 41%]
tests/api/unit/services/test_validator_service.py ................       [ 54%]
tests/api/unit/services/grid/test_grid_service.py ...........            [ 63%]
tests/api/unit/services/grid/test_split_service.py .....                 [ 67%]
tests/api/unit/services/test_team_service.py .......                     [ 73%]
tests/api/unit/services/test_campaign_service.py ...                     [ 75%]
tests/api/unit/services/test_project_admin_service.py .........          [ 83%]
tests/api/unit/services/test_project_search_service.py ................. [ 96%]
....                                                                     [100%]

============================= 124 passed in 21.35s =============================

```

## Resultado del reporte Log (Fase 2)

```sh
Name                                         Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------
backend/services/campaign_service.py           172     76    56%   29, 44, 51-61, 67-80, 87-88, 112-148, 154-160, 197-198, 234-242, 254-267, 292-324, 333-364, 407, 421-428
backend/services/grid/split_service.py         130     30    77%   34-59, 66-101, 255, 304
backend/services/mapping_service.py            215     60    72%   57-65, 115, 119, 127, 234, 258-282, 334-340, 347, 369-413, 424-457, 544, 551, 555
backend/services/organisation_service.py       195     79    59%   91-92, 160-176, 181, 191, 196-228, 234-243, 254-258, 271-277, 283-302, 310-314, 326-341, 383-385, 427-429, 456-470, 478, 510-537
backend/services/project_admin_service.py      194     75    61%   40, 54-110, 115-117, 131-132, 140, 144, 151-152, 159, 184, 190, 246-251, 271, 325, 338-376, 398, 409-416
backend/services/project_search_service.py     424     47    89%   45, 169-171, 228-246, 344-354, 499-500, 523-527, 681-682, 734, 745, 762, 790, 910-928, 957, 965-967, 981-993, 1009-1011
backend/services/project_service.py            368    107    71%   82-86, 102, 106, 111-123, 178-179, 185-197, 222, 231, 245-276, 287-288, 294-295, 315-317, 324-340, 348-358, 374, 434-448, 466, 527-535, 540-541, 549-551, 608, 640-641, 646-647, 656-678, 698-699, 702-703, 709-710, 722-727, 731-736
backend/services/team_service.py               388    206    47%   40, 47, 64-97, 109-135, 158-161, 169-184, 192-208, 219, 247-268, 289-304, 313-321, 324-329, 332-337, 354, 357-361, 384-387, 399-401, 423, 446, 505-510, 524-534, 566-571, 580-583, 592-595, 600-603, 608-609, 631-632, 636-644, 649-663, 670-683, 690-701, 735-753, 798-822, 830-843, 855-967
backend/services/validator_service.py          234    117    50%   83, 101, 105, 109-113, 128-139, 168-241, 249-257, 275-284, 294-323, 357-377, 399-479, 583, 606-624
--------------------------------------------------------------------------
TOTAL                                         2320    797    66%
```


