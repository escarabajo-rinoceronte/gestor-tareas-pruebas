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
  <b>Proyecto:</b> HOT Tasking Manager — MÃ³dulo de GestiÃ³n de Proyectos (Project Management) <br>
  <b>Fecha de Elaboración:</b> 04/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# MÃ³dulo de GestiÃ³n de Proyectos (Project Management)

## 1. Criterio de SelecciÃ³n

Para que un archivo de prueba sea considerado parte del mÃ³dulo **GestiÃ³n de Proyectos**, debe cumplir al menos uno de los siguientes requisitos:

1. **GestiÃ³n del ciclo de vida del proyecto:** el test debe validar operaciones relacionadas con creaciÃ³n, consulta, ediciÃ³n, eliminaciÃ³n, publicaciÃ³n, transferencia o administraciÃ³n de proyectos.
2. **AdministraciÃ³n de configuraciÃ³n del proyecto:** el test debe verificar informaciÃ³n del proyecto como nombre, descripciÃ³n, instrucciones, prioridad, privacidad, campaÃ±as, equipos, partners o estado del proyecto.
3. **Persistencia de entidades propias del proyecto:** el test debe interactuar con modelos directamente asociados a proyectos, como `Project`, `ProjectInfo`, `ProjectPartner`, `ProjectChat` o `PriorityArea`.
4. **ExposiciÃ³n de endpoints de proyectos:** el punto de entrada debe ser un endpoint ubicado en `backend/api/projects/`.
5. **LÃ³gica de negocio propia de proyectos:** el test debe validar servicios como `ProjectService`, `ProjectAdminService`, `ProjectSearchService` o `ProjectPartnershipService`.

---

## 2. Archivos del mÃ³dulo considerados para cobertura

Para medir la cobertura del mÃ³dulo se consideraron Ãºnicamente los archivos propios de **GestiÃ³n de Proyectos**, organizados por capas.

### A. API / Controladores

| Archivo | JustificaciÃ³n de InclusiÃ³n |
| :--- | :--- |
| `backend/api/projects/__init__.py` | Inicializa el paquete de endpoints del mÃ³dulo de proyectos. |
| `backend/api/projects/resources.py` | Expone los endpoints principales para crear, consultar, editar, eliminar y listar proyectos. |
| `backend/api/projects/actions.py` | Contiene acciones administrativas sobre proyectos, como transferencia, destacado, mensajes e intereses. |
| `backend/api/projects/activities.py` | Permite consultar actividades o lÃ­nea de tiempo asociada a proyectos. |
| `backend/api/projects/campaigns.py` | Gestiona la relaciÃ³n entre proyectos y campaÃ±as. |
| `backend/api/projects/contributions.py` | Expone informaciÃ³n de contribuciones relacionadas con proyectos. |
| `backend/api/projects/favorites.py` | Gestiona la funcionalidad de marcar o quitar proyectos favoritos. |
| `backend/api/projects/partnerships.py` | Expone endpoints para asociaciones entre proyectos y partners. |
| `backend/api/projects/statistics.py` | Expone estadÃ­sticas del proyecto. |
| `backend/api/projects/teams.py` | Gestiona la relaciÃ³n entre proyectos y equipos. |

### B. Servicios / LÃ³gica de negocio

| Archivo | JustificaciÃ³n de InclusiÃ³n |
| :--- | :--- |
| `backend/services/project_service.py` | Servicio principal de operaciones generales del proyecto. |
| `backend/services/project_admin_service.py` | Servicio administrativo para creaciÃ³n, ediciÃ³n, permisos, transferencia y eliminaciÃ³n de proyectos. |
| `backend/services/project_search_service.py` | Servicio encargado de bÃºsqueda, filtros, Ã¡reas, bbox y consulta avanzada de proyectos. |
| `backend/services/project_partnership_service.py` | Servicio especÃ­fico para relaciones entre proyectos y partners. |

### C. Modelos PostGIS / Base de datos

| Archivo | JustificaciÃ³n de InclusiÃ³n |
| :--- | :--- |
| `backend/models/postgis/project.py` | Modelo principal del proyecto; contiene datos centrales, estados, geometrÃ­a, AOI y relaciones. |
| `backend/models/postgis/project_info.py` | Modelo para informaciÃ³n descriptiva o localizada del proyecto. |
| `backend/models/postgis/project_partner.py` | Modelo de relaciÃ³n entre proyecto y partner. |
| `backend/models/postgis/project_chat.py` | Modelo para mensajes o chat asociados al proyecto. |
| `backend/models/postgis/priority_area.py` | Modelo para Ã¡reas prioritarias dentro del proyecto. |

### D. DTOs / Esquemas

| Archivo | JustificaciÃ³n de InclusiÃ³n |
| :--- | :--- |
| `backend/models/dtos/project_dto.py` | DTO principal para entrada y salida de datos del proyecto. |
| `backend/models/dtos/project_partner_dto.py` | DTO relacionado con asociaciones entre proyectos y partners. |

---

## 3. Listado de suites de pruebas de integraciÃ³n actuales

El conjunto seleccionado para el mÃ³dulo **GestiÃ³n de Proyectos** consta de pruebas ubicadas en `tests/api/integration/`.

### Archivos Incluidos

| Archivo de Prueba | JustificaciÃ³n de InclusiÃ³n |
| :--- | :--- |
| `api/projects/test_actions.py` | Valida acciones administrativas sobre proyectos, como transferencia, destacado, intereses, mensajes y cÃ¡lculo de tiles intersectados. |
| `api/projects/test_activities.py` | Verifica la recuperaciÃ³n de actividades o eventos asociados al proyecto. |
| `api/projects/test_campaigns.py` | Cubre la asignaciÃ³n y eliminaciÃ³n de campaÃ±as relacionadas con proyectos. |
| `api/projects/test_contributions.py` | EvalÃºa la obtenciÃ³n de contribuciones de usuarios dentro de proyectos. |
| `api/projects/test_favourites.py` | Valida la funcionalidad de agregar y quitar proyectos favoritos. |
| `api/projects/test_resources.py` | Cubre endpoints principales del mÃ³dulo: creaciÃ³n, consulta, ediciÃ³n, privacidad, draft, listado y eliminaciÃ³n de proyectos. |
| `api/projects/test_statistics.py` | Verifica endpoints de estadÃ­sticas del proyecto. |
| `models/test_project.py` | Valida comportamiento del modelo `Project`, persistencia, DTOs y actualizaciÃ³n de datos. |
| `services/test_project_admin_service.py` | Cubre la lÃ³gica administrativa del proyecto: creaciÃ³n de draft, clonaciÃ³n, permisos y tareas asociadas. |
| `services/test_project_service.py` | Valida operaciones generales del servicio de proyectos y permisos de visualizaciÃ³n/uso. |
| `services/test_project_search_service.py` | Prueba bÃºsqueda de proyectos por Ã¡rea, intersecciÃ³n y bbox. |
| `services/test_featured_projects_services.py` | EvalÃºa lÃ³gica relacionada con proyectos destacados. |

### Archivos Excluidos

* `api/tasks/test_actions.py`: se excluye porque pertenece al flujo de tareas, mapeo y validaciÃ³n, no al ciclo de vida administrativo del proyecto.
* `api/tasks/test_resources.py`: aunque las tareas dependen de proyectos, este archivo valida recursos de tareas individuales.
* `services/grid/test_split_service.py`: se excluye porque pertenece a la lÃ³gica de grilla y divisiÃ³n de tareas; se considera dependencia del proyecto, no nÃºcleo del mÃ³dulo.
* `services/license_service.py`: se excluye del alcance de cobertura del mÃ³dulo porque pertenece al manejo de licencias, aunque sea usado durante la validaciÃ³n de imÃ¡genes.
* `api/users/*`: se excluye porque pertenece al mÃ³dulo de usuarios, aunque los proyectos dependan de autores, managers o validadores.
* `api/organisations/*` y `api/teams/*`: se excluyen porque pertenecen a mÃ³dulos externos de gobernanza, aunque existan relaciones con proyectos.

---

## 4. AnÃ¡lisis Funcional por Archivo

### A. GestiÃ³n principal de proyectos (`api/projects/test_resources.py`)

* **Objetivo:** validar los endpoints principales del mÃ³dulo de proyectos.
* **Flujos Cubiertos:** creaciÃ³n de proyecto, obtenciÃ³n de proyecto, ediciÃ³n, eliminaciÃ³n, listado, proyectos privados, drafts y validaciones de acceso.
* **Componentes:** `Project`, `ProjectDTO`, `ProjectService`, `ProjectAdminService`, endpoints de `backend/api/projects/resources.py`.

### B. Acciones administrativas (`api/projects/test_actions.py`)

* **Objetivo:** asegurar que las acciones administrativas se ejecuten respetando permisos y reglas de negocio.
* **Flujos Cubiertos:** transferencia de propiedad, marcar proyecto como destacado, quitar destacado, envÃ­o de mensajes a contribuidores, asignaciÃ³n de intereses y cÃ¡lculo de tiles intersectados.
* **Componentes:** `ProjectAdminService`, `ProjectService`, `Project`, `User`, permisos administrativos.

### C. CampaÃ±as, favoritos y estadÃ­sticas (`api/projects/test_campaigns.py`, `test_favourites.py`, `test_statistics.py`)

* **Objetivo:** validar funcionalidades complementarias del ciclo de vida del proyecto.
* **Flujos Cubiertos:** asociar campaÃ±as, eliminar campaÃ±as, marcar favoritos, quitar favoritos y consultar estadÃ­sticas.
* **Componentes:** `Project`, `Campaign`, `User`, endpoints de campaÃ±as, favoritos y estadÃ­sticas.

### D. Modelo y persistencia del proyecto (`models/test_project.py`)

* **Objetivo:** verificar que el modelo `Project` persista y transforme correctamente la informaciÃ³n.
* **Flujos Cubiertos:** creaciÃ³n de entidad, actualizaciÃ³n de campos, conversiÃ³n a DTO, manejo de AOI y relaciones bÃ¡sicas.
* **Componentes:** `Project`, `ProjectInfo`, `PriorityArea`, PostgreSQL/PostGIS.

### E. Servicios administrativos y bÃºsqueda (`services/test_project_admin_service.py`, `test_project_search_service.py`)

* **Objetivo:** probar la lÃ³gica de negocio del mÃ³dulo sin depender Ãºnicamente de los endpoints HTTP.
* **Flujos Cubiertos:** creaciÃ³n de borradores, clonaciÃ³n de proyectos, permisos de administraciÃ³n, bÃºsqueda por Ã¡rea, bbox e intersecciÃ³n.
* **Componentes:** `ProjectAdminService`, `ProjectSearchService`, `Project`, PostGIS.

### F. Servicio general de proyectos (`services/test_project_service.py`)

* **Objetivo:** validar reglas generales de acceso y consulta sobre proyectos.
* **Flujos Cubiertos:** obtenciÃ³n de DTO para mapper, manejo de proyectos draft, proyectos privados y permisos.
* **Componentes:** `ProjectService`, `Project`, `User`, DTOs del mÃ³dulo.

---

## 5. Diagrama de InteracciÃ³n de las Pruebas de IntegraciÃ³n

Este diagrama muestra cÃ³mo las pruebas de integraciÃ³n del mÃ³dulo ejercen varias capas del sistema:

```mermaid
sequenceDiagram
    participant Test as Integration Test (Project Management)
    participant API as FastAPI Controllers
    participant Service as Project Services
    participant DB as PostgreSQL + PostGIS
    participant DTO as Project DTOs

    Test->>API: POST /projects/
    API->>Service: create_draft_project()
    Service->>DB: INSERT project + project_info
    DB-->>Service: Project persisted
    Service->>DTO: Build ProjectDTO
    DTO-->>API: Serialized response
    API-->>Test: Assert HTTP response + project data

    Test->>API: PATCH /projects/{project_id}
    API->>Service: update_project()
    Service->>DB: UPDATE project metadata / status
    DB-->>Service: Updated project
    Service-->>API: Project updated
    API-->>Test: Assert updated fields

    Test->>API: GET /projects/?bbox=...
    API->>Service: search_projects()
    Service->>DB: Spatial query using PostGIS
    DB-->>Service: Matching projects
    Service-->>API: Search results
    API-->>Test: Assert filtered projects
```

---

## 6. Alcance de la cobertura

La cobertura se calculÃ³ sobre los archivos fuente propios del mÃ³dulo, no sobre los archivos de prueba. Es decir, se ejecutaron pruebas de integraciÃ³n y luego se filtrÃ³ el reporte para medir Ãºnicamente el cÃ³digo correspondiente a **API, servicios, modelos PostGIS y DTOs de GestiÃ³n de Proyectos**.

### Resultado general

| MÃ©trica | Resultado |
| :--- | :--- |
| MÃ³dulo evaluado | GestiÃ³n de Proyectos |
| Tipo de pruebas | IntegraciÃ³n |
| Pruebas ejecutadas | 179 |
| Pruebas exitosas | 179 |
| Pruebas fallidas | 0 |
| Archivos medidos | 21 |
| LÃ­neas ejecutables analizadas | 3126 |
| LÃ­neas no cubiertas | 840 |
| Cobertura total | 73% |
| Tiempo de ejecuciÃ³n | 73.84 s |

### Cobertura por archivo

| Archivo | Stmts | Miss | Cover |
| :--- | ---: | ---: | ---: |
| `backend/api/projects/__init__.py` | 0 | 0 | 100% |
| `backend/api/projects/actions.py` | 92 | 34 | 63% |
| `backend/api/projects/activities.py` | 35 | 12 | 66% |
| `backend/api/projects/campaigns.py` | 32 | 0 | 100% |
| `backend/api/projects/contributions.py` | 27 | 6 | 78% |
| `backend/api/projects/favorites.py` | 26 | 0 | 100% |
| `backend/api/projects/partnerships.py` | 55 | 32 | 42% |
| `backend/api/projects/resources.py` | 292 | 83 | 72% |
| `backend/api/projects/statistics.py` | 18 | 2 | 89% |
| `backend/api/projects/teams.py` | 57 | 38 | 33% |
| `backend/models/dtos/project_dto.py` | 406 | 50 | 88% |
| `backend/models/dtos/project_partner_dto.py` | 41 | 5 | 88% |
| `backend/models/postgis/priority_area.py` | 33 | 4 | 88% |
| `backend/models/postgis/project.py` | 733 | 161 | 78% |
| `backend/models/postgis/project_chat.py` | 48 | 25 | 48% |
| `backend/models/postgis/project_info.py` | 85 | 18 | 79% |
| `backend/models/postgis/project_partner.py` | 75 | 41 | 45% |
| `backend/services/project_admin_service.py` | 194 | 17 | 91% |
| `backend/services/project_partnership_service.py` | 85 | 62 | 27% |
| `backend/services/project_search_service.py` | 424 | 95 | 78% |
| `backend/services/project_service.py` | 368 | 155 | 58% |
| **TOTAL** | **3126** | **840** | **73%** |

---

## 7. EjecuciÃ³n de pruebas de integraciÃ³n

Se ejecutaron las pruebas de integraciÃ³n del mÃ³dulo mediante el siguiente comando:

```sh
docker compose exec -T tm-backend coverage run -m pytest tests/api/integration/api/projects/ tests/api/integration/models/test_project.py tests/api/integration/services/test_project_admin_service.py tests/api/integration/services/test_project_service.py tests/api/integration/services/test_project_search_service.py tests/api/integration/services/test_featured_projects_services.py -p no:warnings
```

### Resultado de la ejecuciÃ³n

```sh
============================= test session starts ==============================
platform linux -- Python 3.10.20, pytest-8.3.5, pluggy-1.5.0
rootdir: /usr/src/app
configfile: pyproject.toml
plugins: anyio-4.9.0
collected 179 items

tests/api/integration/api/projects/test_actions.py ..................... [ 11%]
..                                                                       [ 12%]
tests/api/integration/api/projects/test_activities.py ....               [ 15%]
tests/api/integration/api/projects/test_campaigns.py ...............     [ 23%]
tests/api/integration/api/projects/test_contributions.py ......          [ 26%]
tests/api/integration/api/projects/test_favourites.py ..........         [ 32%]
tests/api/integration/api/projects/test_resources.py ................... [ 43%]
..............................................................           [ 77%]
tests/api/integration/api/projects/test_statistics.py .....              [ 80%]
tests/api/integration/models/test_project.py .......                     [ 84%]
tests/api/integration/services/test_project_admin_service.py ........... [ 90%]
.......                                                                  [ 94%]
tests/api/integration/services/test_project_service.py ......            [ 97%]
tests/api/integration/services/test_project_search_service.py ...        [ 99%]
tests/api/integration/services/test_featured_projects_services.py .      [100%]

======================== 179 passed in 73.84s (0:01:13) ========================
```

---

## 8. Reporte de cobertura ejecutado

Para generar el reporte filtrado del mÃ³dulo se ejecutÃ³:

```sh
docker compose exec -T tm-backend coverage report -m --include="backend/api/projects/*.py,backend/services/project_service.py,backend/services/project_admin_service.py,backend/services/project_search_service.py,backend/services/project_partnership_service.py,backend/models/postgis/project.py,backend/models/postgis/project_info.py,backend/models/postgis/project_partner.py,backend/models/postgis/project_chat.py,backend/models/postgis/priority_area.py,backend/models/dtos/project_dto.py,backend/models/dtos/project_partner_dto.py"
```

### Resultado del reporte

```sh
Name                                              Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------------
backend/api/projects/__init__.py                      0      0   100%
backend/api/projects/actions.py                      92     34    63%
backend/api/projects/activities.py                   35     12    66%
backend/api/projects/campaigns.py                    32      0   100%
backend/api/projects/contributions.py                27      6    78%
backend/api/projects/favorites.py                    26      0   100%
backend/api/projects/partnerships.py                 55     32    42%
backend/api/projects/resources.py                   292     83    72%
backend/api/projects/statistics.py                   18      2    89%
backend/api/projects/teams.py                        57     38    33%
backend/models/dtos/project_dto.py                  406     50    88%
backend/models/dtos/project_partner_dto.py           41      5    88%
backend/models/postgis/priority_area.py              33      4    88%
backend/models/postgis/project.py                   733    161    78%
backend/models/postgis/project_chat.py               48     25    48%
backend/models/postgis/project_info.py               85     18    79%
backend/models/postgis/project_partner.py            75     41    45%
backend/services/project_admin_service.py           194     17    91%
backend/services/project_partnership_service.py      85     62    27%
backend/services/project_search_service.py          424     95    78%
backend/services/project_service.py                 368    155    58%
-------------------------------------------------------------------------------
TOTAL                                              3126    840    73%
```

---

## 9. AnÃ¡lisis de resultados

El mÃ³dulo presenta una cobertura total de **73%**, lo que indica una base importante de pruebas de integraciÃ³n. Las 179 pruebas ejecutadas pasaron correctamente, por lo que el comportamiento validado se encuentra estable en el entorno de pruebas.

Los archivos con mejor cobertura fueron:

| Archivo | Cobertura | InterpretaciÃ³n |
| :--- | ---: | :--- |
| `backend/api/projects/campaigns.py` | 100% | Los endpoints de campaÃ±as estÃ¡n completamente cubiertos. |
| `backend/api/projects/favorites.py` | 100% | La funcionalidad de favoritos estÃ¡ completamente cubierta. |
| `backend/services/project_admin_service.py` | 91% | La lÃ³gica administrativa principal tiene cobertura alta. |
| `backend/api/projects/statistics.py` | 89% | Las estadÃ­sticas del proyecto estÃ¡n bien cubiertas. |
| `backend/models/dtos/project_dto.py` | 88% | Los DTOs principales estÃ¡n bien ejercitados por las pruebas. |
| `backend/models/postgis/priority_area.py` | 88% | La persistencia de Ã¡reas prioritarias tiene buena cobertura. |

Los archivos con menor cobertura fueron:

| Archivo | Cobertura | ObservaciÃ³n |
| :--- | ---: | :--- |
| `backend/services/project_partnership_service.py` | 27% | Falta reforzar pruebas de integraciÃ³n para relaciones proyecto-partner. |
| `backend/api/projects/teams.py` | 33% | Faltan pruebas especÃ­ficas para endpoints que relacionan proyectos con equipos. |
| `backend/api/projects/partnerships.py` | 42% | Los endpoints de partnerships estÃ¡n poco cubiertos. |
| `backend/models/postgis/project_partner.py` | 45% | Faltan pruebas sobre persistencia y transformaciÃ³n de relaciones con partners. |
| `backend/models/postgis/project_chat.py` | 48% | Falta cubrir mÃ¡s escenarios de mensajes o chat de proyecto. |
| `backend/services/project_service.py` | 58% | El servicio general aÃºn tiene ramas y mÃ©todos no ejercitados. |

---

## 10. Alcance y nivel de confianza

| DimensiÃ³n | Alcance | Nivel de Confianza | Observaciones |
| :--- | :--- | :--- | :--- |
| **CreaciÃ³n y administraciÃ³n de proyectos** | 90% | **Alto** | `project_admin_service.py` obtuvo 91%, lo que indica buena cobertura de la lÃ³gica administrativa. |
| **Endpoints principales de proyectos** | 72% | **Medio-Alto** | `resources.py` tiene cobertura aceptable, aunque todavÃ­a existen ramas no cubiertas. |
| **CampaÃ±as y favoritos** | 100% | **Muy Alto** | Ambos archivos alcanzaron cobertura completa. |
| **BÃºsqueda de proyectos** | 78% | **Alto** | `project_search_service.py` cubre gran parte de la consulta espacial y filtros. |
| **Modelo principal de proyecto** | 78% | **Alto** | `project.py` tiene una cobertura sÃ³lida considerando su tamaÃ±o y complejidad. |
| **DTOs del mÃ³dulo** | 88% | **Alto** | Los esquemas de entrada y salida estÃ¡n bien ejercitados por los tests. |
| **Partnerships** | 27%-45% | **Bajo** | Es la zona mÃ¡s dÃ©bil del mÃ³dulo. Faltan pruebas para endpoints, servicio y modelo. |
| **Equipos asociados a proyectos** | 33% | **Bajo** | Falta reforzar pruebas para `backend/api/projects/teams.py`. |
| **Chat de proyecto** | 48% | **Bajo-Medio** | Falta cubrir mÃ¡s escenarios relacionados con comunicaciÃ³n dentro del proyecto. |

---

## 11. ConclusiÃ³n del Estado Actual

Las pruebas de integraciÃ³n existentes proporcionan una base sÃ³lida para el mÃ³dulo **GestiÃ³n de Proyectos**. La ejecuciÃ³n fue exitosa, con **179 pruebas pasadas de 179 ejecutadas**, lo que evidencia estabilidad en los flujos ya cubiertos.

La cobertura total obtenida fue de **73%** sobre 21 archivos propios del mÃ³dulo. Este resultado demuestra que gran parte del flujo principal estÃ¡ validado, especialmente en creaciÃ³n y administraciÃ³n de proyectos, campaÃ±as, favoritos, estadÃ­sticas, bÃºsqueda y DTOs.

Sin embargo, el mÃ³dulo todavÃ­a presenta oportunidades de mejora. Las principales brechas se encuentran en `project_partnership_service.py`, `api/projects/teams.py`, `api/projects/partnerships.py`, `project_partner.py` y `project_chat.py`. Estas Ã¡reas deberÃ­an priorizarse si se busca aumentar la cobertura del mÃ³dulo hacia una meta superior, como 80% u 85%.

**ConclusiÃ³n final:**  
El mÃ³dulo de GestiÃ³n de Proyectos cuenta con una cobertura de integraciÃ³n aceptable y una ejecuciÃ³n estable de pruebas, pero requiere reforzar los escenarios de partnerships, equipos asociados y comunicaciÃ³n de proyecto para alcanzar una cobertura mÃ¡s alta y equilibrada.



