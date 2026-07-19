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
  <b>Proyecto:</b> HOT Tasking Manager — Reporte de EjecuciÃ³n: MÃ³dulo de GestiÃ³n de Proyectos (Project Management) <br>
  <b>Fecha de Elaboración:</b> 16/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Reporte de EjecuciÃ³n: MÃ³dulo de GestiÃ³n de Proyectos (Project Management)

Este documento contiene los resultados de la ejecuciÃ³n de las pruebas de integraciÃ³n diseÃ±adas y ampliadas para el mÃ³dulo de **GestiÃ³n de Proyectos**.

El objetivo principal fue incrementar la cobertura del mÃ³dulo hasta alcanzar el umbral mÃ­nimo de **85%**, reforzando pruebas sobre controladores, servicios, modelos PostGIS y DTOs relacionados con proyectos.

---

## 1. Alcance de la cobertura

La cobertura se calculÃ³ sobre los archivos fuente propios de **Project Management**. Se ejecutaron suites de pruebas de integraciÃ³n y el reporte se filtrÃ³ para medir exclusivamente los controladores de proyectos, servicios de proyectos, modelos PostGIS y sus respectivos DTOs.

### Resultado general

| MÃ©trica                       | Resultado                                 |
| :---------------------------- | :---------------------------------------- |
| MÃ³dulo evaluado               | Project Management (GestiÃ³n de Proyectos) |
| Tipo de pruebas               | IntegraciÃ³n                               |
| Pruebas ejecutadas            | 208                                       |
| Pruebas exitosas              | 208                                       |
| Pruebas fallidas              | 0                                         |
| Archivos medidos              | 21                                        |
| LÃ­neas ejecutables analizadas | 3126                                      |
| LÃ­neas no cubiertas           | 471                                       |
| Cobertura total               | 85%                                       |

### Cobertura por archivo

| Archivo                                           |    Stmts |    Miss |   Cover |
| :------------------------------------------------ | -------: | ------: | ------: |
| `backend/api/projects/__init__.py`                |        0 |       0 |    100% |
| `backend/api/projects/actions.py`                 |       92 |       7 |     92% |
| `backend/api/projects/activities.py`              |       35 |      12 |     66% |
| `backend/api/projects/campaigns.py`               |       32 |       0 |    100% |
| `backend/api/projects/contributions.py`           |       27 |       6 |     78% |
| `backend/api/projects/favorites.py`               |       26 |       0 |    100% |
| `backend/api/projects/partnerships.py`            |       55 |       3 |     95% |
| `backend/api/projects/resources.py`               |      292 |      83 |     72% |
| `backend/api/projects/statistics.py`              |       18 |       2 |     89% |
| `backend/api/projects/teams.py`                   |       57 |      16 |     72% |
| `backend/models/dtos/project_dto.py`              |      406 |      50 |     88% |
| `backend/models/dtos/project_partner_dto.py`      |       41 |       5 |     88% |
| `backend/models/postgis/priority_area.py`         |       33 |       4 |     88% |
| `backend/models/postgis/project.py`               |      733 |     103 |     86% |
| `backend/models/postgis/project_chat.py`          |       48 |       1 |     98% |
| `backend/models/postgis/project_info.py`          |       85 |      18 |     79% |
| `backend/models/postgis/project_partner.py`       |       75 |       9 |     88% |
| `backend/services/project_admin_service.py`       |      194 |      17 |     91% |
| `backend/services/project_partnership_service.py` |       85 |       6 |     93% |
| `backend/services/project_search_service.py`      |      424 |      28 |     93% |
| `backend/services/project_service.py`             |      368 |     101 |     73% |
| **TOTAL**                                         | **3126** | **471** | **85%** |

---

## 2. EjecuciÃ³n de pruebas de integraciÃ³n

Se ejecutaron las pruebas de integraciÃ³n correspondientes al mÃ³dulo empleando el siguiente comando:

```sh
docker compose exec -T tm-backend coverage run -m pytest tests/api/integration/api/projects/ tests/api/integration/models/test_project.py tests/api/integration/models/test_project_clone.py tests/api/integration/models/test_project_chat.py tests/api/integration/services/test_project_service_permissions.py tests/api/integration/services/test_project_admin_service.py tests/api/integration/services/test_project_service.py tests/api/integration/services/test_project_search_service.py tests/api/integration/services/test_featured_projects_services.py -p no:warnings
```

### Resultado de la ejecuciÃ³n

```sh
============================= test session starts ==============================
platform linux -- Python 3.10.20, pytest-8.3.5, pluggy-1.5.0
rootdir: /usr/src/app
configfile: pyproject.toml
plugins: anyio-4.9.0
collected 208 items

tests/api/integration/api/projects/test_actions.py ..................... 
tests/api/integration/api/projects/test_actions_additional.py ...
tests/api/integration/api/projects/test_activities.py ....
tests/api/integration/api/projects/test_campaigns.py ...............
tests/api/integration/api/projects/test_contributions.py ......
tests/api/integration/api/projects/test_favourites.py ..........
tests/api/integration/api/projects/test_partnerships.py ........
tests/api/integration/api/projects/test_resources.py ...................
..............................................................
tests/api/integration/api/projects/test_statistics.py .....
tests/api/integration/api/projects/test_teams.py .........
tests/api/integration/models/test_project.py .......
tests/api/integration/models/test_project_clone.py ..
tests/api/integration/models/test_project_chat.py ...
tests/api/integration/services/test_project_service_permissions.py .
tests/api/integration/services/test_project_admin_service.py ...........
.......
tests/api/integration/services/test_project_service.py ......
tests/api/integration/services/test_project_search_service.py ......
tests/api/integration/services/test_featured_projects_services.py .

======================== 208 passed ========================
```

---

## 3. Reporte de cobertura ejecutado

Para generar el reporte validando exclusivamente las capas operativas del mÃ³dulo, se ejecutÃ³:

```sh
docker compose exec -T tm-backend coverage report -m --include="backend/api/projects/*.py,backend/services/project_service.py,backend/services/project_admin_service.py,backend/services/project_search_service.py,backend/services/project_partnership_service.py,backend/models/postgis/project.py,backend/models/postgis/project_info.py,backend/models/postgis/project_partner.py,backend/models/postgis/project_chat.py,backend/models/postgis/priority_area.py,backend/models/dtos/project_dto.py,backend/models/dtos/project_partner_dto.py"
```

### Resultado del reporte

```sh
Name                                              Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------------
backend/api/projects/__init__.py                      0      0   100%
backend/api/projects/actions.py                      92      7    92%   79-80, 178-180, 449, 465
backend/api/projects/activities.py                   35     12    66%   58-74, 119-135
backend/api/projects/campaigns.py                    32      0   100%
backend/api/projects/contributions.py                27      6    78%   53-69
backend/api/projects/favorites.py                    26      0   100%
backend/api/projects/partnerships.py                 55      3    95%   143, 230, 298
backend/api/projects/resources.py                   292     83    72%   ...
backend/api/projects/statistics.py                   18      2    89%   30-31
backend/api/projects/teams.py                        57     16    72%   ...
backend/models/dtos/project_dto.py                  406     50    88%   ...
backend/models/dtos/project_partner_dto.py           41      5    88%   10-19
backend/models/postgis/priority_area.py              33      4    88%   37, 40, 57, 76
backend/models/postgis/project.py                   733    103    86%   ...
backend/models/postgis/project_chat.py               48      1    98%   180
backend/models/postgis/project_info.py               85     18    79%   47-50, 136-137, 145-184
backend/models/postgis/project_partner.py            75      9    88%   51, 62, 203-209
backend/services/project_admin_service.py           194     17    91%   ...
backend/services/project_partnership_service.py      85      6    93%   21, 77, 106, 133, 150, 166
backend/services/project_search_service.py          424     28    93%   ...
backend/services/project_service.py                 368    101    73%   ...
-------------------------------------------------------------------------------
TOTAL                                              3126    471    85%
```

---

## 4. AnÃ¡lisis de resultados

El mÃ³dulo de **Project Management** demuestra una cobertura sÃ³lida del **85%**, evaluada sobre una base amplia de cÃ³digo de **3126 lÃ­neas ejecutables exclusivas**. Las **208 pruebas superadas exitosamente** comprueban un nivel alto de estabilidad en los flujos principales de gestiÃ³n de proyectos.

Los archivos con mejor cobertura fueron:

| Archivo                                      | Cobertura | InterpretaciÃ³n                                                                                                |
| :------------------------------------------- | --------: | :------------------------------------------------------------------------------------------------------------ |
| `backend/api/projects/campaigns.py`          |      100% | Los flujos de campaÃ±as asociadas a proyectos estÃ¡n totalmente verificados.                                    |
| `backend/api/projects/favorites.py`          |      100% | Las operaciones de favoritos sobre proyectos se encuentran completamente cubiertas.                           |
| `backend/models/postgis/project_chat.py`     |       98% | La creaciÃ³n, sanitizaciÃ³n y consulta paginada de mensajes de chat estÃ¡ casi totalmente validada.              |
| `backend/api/projects/partnerships.py`       |       95% | Los flujos de alianzas o partnerships de proyectos presentan una cobertura muy alta.                          |
| `backend/services/project_search_service.py` |       93% | El filtrado y bÃºsqueda avanzada de proyectos tiene una cobertura sÃ³lida.                                      |
| `backend/api/projects/actions.py`            |       92% | Las acciones administrativas de proyectos fueron reforzadas mediante nuevos casos de Ã©xito, error y permisos. |
| `backend/services/project_admin_service.py`  |       91% | La lÃ³gica administrativa del proyecto presenta alta confiabilidad.                                            |

Los archivos con menor cobertura fueron:

| Archivo                               | Cobertura | ObservaciÃ³n                                                                                              |
| :------------------------------------ | --------: | :------------------------------------------------------------------------------------------------------- |
| `backend/api/projects/activities.py`  |       66% | Ciertos flujos de consulta de actividades no se ejercitan completamente.                                 |
| `backend/api/projects/resources.py`   |       72% | Es uno de los controladores mÃ¡s extensos del mÃ³dulo y conserva ramas HTTP no cubiertas.                  |
| `backend/api/projects/teams.py`       |       72% | Persisten casos borde relacionados con permisos y errores en operaciones de equipos.                     |
| `backend/services/project_service.py` |       73% | Aunque se reforzaron reglas crÃ­ticas de permisos, todavÃ­a existen ramas complejas de negocio pendientes. |

---

## 5. Alcance y nivel de confianza actual

| DimensiÃ³n                                 | Alcance                     | Nivel de Confianza | Observaciones                                                                                                |
| :---------------------------------------- | :-------------------------- | :----------------- | :----------------------------------------------------------------------------------------------------------- |
| **Acciones administrativas de proyectos** | 92%                         | **Muy Alto**       | Respaldado por pruebas sobre `feature`, `remove_feature` y `set_interests`.                                  |
| **BÃºsqueda avanzada de proyectos**        | 93%                         | **Muy Alto**       | El servicio de bÃºsqueda cubre filtros, exportaciÃ³n y escenarios principales de consulta.                     |
| **Partnerships de proyectos**             | 95%                         | **Muy Alto**       | Las alianzas vinculadas a proyectos presentan alta validaciÃ³n.                                               |
| **Chat de proyectos**                     | 98%                         | **Muy Alto**       | La lÃ³gica de mensajes, sanitizaciÃ³n y paginaciÃ³n estÃ¡ casi completamente cubierta.                           |
| **ClonaciÃ³n de proyectos**                | 86% en `project.py`         | **Alto**           | Se validÃ³ la copia de entidades relacionadas y reinicio de atributos del nuevo proyecto.                     |
| **Permisos de mapeo y validaciÃ³n**        | 73% en `project_service.py` | **Medio-Alto**     | Se cubrieron reglas crÃ­ticas como usuario bloqueado, proyecto no publicado, equipo, nivel y tarea bloqueada. |
| **Endpoints generales de recursos**       | 72% en `resources.py`       | **Medio-Alto**     | Persisten ramas HTTP y casos borde sin ejercitar.                                                            |

---

## 6. ConclusiÃ³n del Estado Actual

Los resultados comprobados sobre **las capas operativas reales** del backend determinan que el mÃ³dulo de **Project Management es robusto, presentando una cobertura total del 85% sobre 21 componentes crÃ­ticos**.

Se ejecutaron **208 pruebas funcionales e integrales** enfocadas en los flujos centrales de gestiÃ³n de proyectos: acciones administrativas, clonaciÃ³n de proyectos, permisos de mapeo y validaciÃ³n, bÃºsqueda avanzada, partnerships, equipos, favoritos, recursos, estadÃ­sticas y mensajerÃ­a de proyectos.

La mejora mÃ¡s relevante se observÃ³ en `backend/api/projects/actions.py`, que alcanzÃ³ **92%** de cobertura tras incorporar pruebas para destacar proyectos, remover destacados y actualizar intereses. Asimismo, `backend/models/postgis/project_chat.py` llegÃ³ a **98%**, reforzando la confianza sobre la creaciÃ³n, sanitizaciÃ³n y consulta de mensajes asociados a proyectos.

**Oportunidades de Mejora:**
Para sobrepasar el umbral de 90% en futuras iteraciones, los esfuerzos deben focalizarse en robustecer las pruebas de integraciÃ³n en `backend/api/projects/resources.py` (72%), `backend/api/projects/activities.py` (66%), `backend/api/projects/teams.py` (72%) y ramas complejas de negocio dentro de `backend/services/project_service.py` (73%).

---

## 7. EjecuciÃ³n de pruebas post-reestructuraciÃ³n (Fase 2)

Con el fin de incrementar la cobertura hasta el umbral de **85%** en el mÃ³dulo de GestiÃ³n de Proyectos, se incorporaron nuevas suites especializadas y se ampliaron escenarios existentes sobre acciones administrativas, modelos PostGIS y servicios de permisos.

### Nuevas suites incorporadas y contribuciÃ³n

* **`tests/api/integration/models/test_project_clone.py`**: AÃ±adida para cubrir la clonaciÃ³n completa de proyectos. Esta suite permitiÃ³ validar la copia de informaciÃ³n relacionada, equipos, campaÃ±as, intereses, editor personalizado, reinicio de contadores y cambio de estado del nuevo proyecto a `DRAFT`.
* **`tests/api/integration/models/test_project_chat.py`**: AÃ±adida para validar la creaciÃ³n de mensajes de chat, sanitizaciÃ³n de contenido Markdown/HTML y recuperaciÃ³n paginada de mensajes asociados a proyectos. ContribuyÃ³ a elevar `backend/models/postgis/project_chat.py` hasta **98%**.
* **`tests/api/integration/services/test_project_service_permissions.py`**: AÃ±adida para cubrir reglas crÃ­ticas de permisos de mapeo y validaciÃ³n, incluyendo usuario bloqueado, proyecto en borrador, permisos por equipo, nivel insuficiente, tarea bloqueada y flujo permitido para manager.
* **`tests/api/integration/api/projects/test_actions_additional.py`**: AÃ±adida para aislar flujos administrativos de `actions.py`: destacar proyecto, remover destacado y actualizar intereses. Su contribuciÃ³n elevÃ³ `backend/api/projects/actions.py` de **63% a 92%**.
* Se conservaron y ejecutaron las suites existentes de `test_project.py`, `test_project_admin_service.py`, `test_project_service.py`, `test_project_search_service.py`, `test_featured_projects_services.py` y las pruebas de controladores bajo `tests/api/integration/api/projects/`.

### Resultado general actualizado

| MÃ©trica                       | Resultado                                 |
| :---------------------------- | :---------------------------------------- |
| MÃ³dulo evaluado               | Project Management (GestiÃ³n de Proyectos) |
| Tipo de pruebas               | IntegraciÃ³n                               |
| Pruebas ejecutadas            | 208                                       |
| Pruebas exitosas              | 208                                       |
| Pruebas fallidas              | 0                                         |
| Archivos medidos              | 21                                        |
| LÃ­neas ejecutables analizadas | 3126                                      |
| LÃ­neas no cubiertas           | 471                                       |
| Cobertura total               | 85%                                       |

### Cobertura por archivo post-implementaciÃ³n

| Archivo                                           |    Stmts |    Miss |   Cover |
| :------------------------------------------------ | -------: | ------: | ------: |
| `backend/api/projects/__init__.py`                |        0 |       0 |    100% |
| `backend/api/projects/actions.py`                 |       92 |       7 |     92% |
| `backend/api/projects/activities.py`              |       35 |      12 |     66% |
| `backend/api/projects/campaigns.py`               |       32 |       0 |    100% |
| `backend/api/projects/contributions.py`           |       27 |       6 |     78% |
| `backend/api/projects/favorites.py`               |       26 |       0 |    100% |
| `backend/api/projects/partnerships.py`            |       55 |       3 |     95% |
| `backend/api/projects/resources.py`               |      292 |      83 |     72% |
| `backend/api/projects/statistics.py`              |       18 |       2 |     89% |
| `backend/api/projects/teams.py`                   |       57 |      16 |     72% |
| `backend/models/dtos/project_dto.py`              |      406 |      50 |     88% |
| `backend/models/dtos/project_partner_dto.py`      |       41 |       5 |     88% |
| `backend/models/postgis/priority_area.py`         |       33 |       4 |     88% |
| `backend/models/postgis/project.py`               |      733 |     103 |     86% |
| `backend/models/postgis/project_chat.py`          |       48 |       1 |     98% |
| `backend/models/postgis/project_info.py`          |       85 |      18 |     79% |
| `backend/models/postgis/project_partner.py`       |       75 |       9 |     88% |
| `backend/services/project_admin_service.py`       |      194 |      17 |     91% |
| `backend/services/project_partnership_service.py` |       85 |       6 |     93% |
| `backend/services/project_search_service.py`      |      424 |      28 |     93% |
| `backend/services/project_service.py`             |      368 |     101 |     73% |
| **TOTAL**                                         | **3126** | **471** | **85%** |

### Resultado de la ejecuciÃ³n (Log)

```sh
============================= test session starts ==============================
platform linux -- Python 3.10.20, pytest-8.3.5, pluggy-1.5.0
rootdir: /usr/src/app
configfile: pyproject.toml
plugins: anyio-4.9.0
collected 208 items

tests/api/integration/api/projects/test_actions.py .....................
tests/api/integration/api/projects/test_actions_additional.py ...
tests/api/integration/api/projects/test_activities.py ....
tests/api/integration/api/projects/test_campaigns.py ...............
tests/api/integration/api/projects/test_contributions.py ......
tests/api/integration/api/projects/test_favourites.py ..........
tests/api/integration/api/projects/test_partnerships.py ........
tests/api/integration/api/projects/test_resources.py ...................
..............................................................
tests/api/integration/api/projects/test_statistics.py .....
tests/api/integration/api/projects/test_teams.py .........
tests/api/integration/models/test_project.py .......
tests/api/integration/models/test_project_clone.py ..
tests/api/integration/models/test_project_chat.py ...
tests/api/integration/services/test_project_service_permissions.py .
tests/api/integration/services/test_project_admin_service.py ...........
.......
tests/api/integration/services/test_project_service.py ......
tests/api/integration/services/test_project_search_service.py ......
tests/api/integration/services/test_featured_projects_services.py .

======================== 208 passed ========================
```

### Reporte de cobertura (Log)

```sh
Name                                              Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------------
backend/api/projects/__init__.py                      0      0   100%
backend/api/projects/actions.py                      92      7    92%   79-80, 178-180, 449, 465
backend/api/projects/activities.py                   35     12    66%   58-74, 119-135
backend/api/projects/campaigns.py                    32      0   100%
backend/api/projects/contributions.py                27      6    78%   53-69
backend/api/projects/favorites.py                    26      0   100%
backend/api/projects/partnerships.py                 55      3    95%   143, 230, 298
backend/api/projects/resources.py                   292     83    72%   ...
backend/api/projects/statistics.py                   18      2    89%   30-31
backend/api/projects/teams.py                        57     16    72%   ...
backend/models/dtos/project_dto.py                  406     50    88%   ...
backend/models/dtos/project_partner_dto.py           41      5    88%   10-19
backend/models/postgis/priority_area.py              33      4    88%   37, 40, 57, 76
backend/models/postgis/project.py                   733    103    86%   ...
backend/models/postgis/project_chat.py               48      1    98%   180
backend/models/postgis/project_info.py               85     18    79%   47-50, 136-137, 145-184
backend/models/postgis/project_partner.py            75      9    88%   51, 62, 203-209
backend/services/project_admin_service.py           194     17    91%   ...
backend/services/project_partnership_service.py      85      6    93%   21, 77, 106, 133, 150, 166
backend/services/project_search_service.py          424     28    93%   ...
backend/services/project_service.py                 368    101    73%   ...
-------------------------------------------------------------------------------
TOTAL                                              3126    471    85%
```

### AnÃ¡lisis Final

Con la incorporaciÃ³n de las nuevas pruebas de integraciÃ³n se logrÃ³ alcanzar el objetivo de cobertura del mÃ³dulo, elevando el total hasta **85%**. La mejora se obtuvo sin modificar la lÃ³gica de negocio del backend, sino ampliando Ãºnicamente la base de pruebas.

El avance mÃ¡s significativo se produjo en `backend/api/projects/actions.py`, que aumentÃ³ de **63% a 92%** al cubrir flujos de permisos, Ã©xito y errores en acciones administrativas. AdemÃ¡s, `backend/models/postgis/project_chat.py` alcanzÃ³ **98%**, fortaleciendo la confianza sobre el manejo de mensajes asociados a proyectos.

El mÃ³dulo queda con un nivel de confianza alto en sus funcionalidades principales: gestiÃ³n administrativa, clonaciÃ³n, bÃºsqueda, permisos, partnerships y chat. Las oportunidades futuras se concentran en `resources.py`, `activities.py`, `teams.py` y ramas complejas de `project_service.py`.


