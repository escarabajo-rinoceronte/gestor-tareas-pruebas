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
  <b>Proyecto:</b> HOT Tasking Manager — DiseÃ±o de Pruebas de IntegraciÃ³n: MÃ³dulo de Tareas, Mapeo y ValidaciÃ³n <br>
  <b>Fecha de Elaboración:</b> 03/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# DiseÃ±o de Pruebas de IntegraciÃ³n: MÃ³dulo de Tareas, Mapeo y ValidaciÃ³n

## 1. Criterios de SelecciÃ³n y Alcance del MÃ³dulo

El diseÃ±o de las pruebas de integraciÃ³n correspondientes al mÃ³dulo de **Mapeo y ValidaciÃ³n** se fundamenta en la validaciÃ³n de, al menos, una de las siguientes condiciones lÃ³gicas crÃ­ticas para el negocio:

| CondiciÃ³n LÃ³gica | DescripciÃ³n TÃ©cnica |
| :--- | :--- |
| **ManipulaciÃ³n de Estado** | VerificaciÃ³n de la correcta transiciÃ³n de estados de la entidad `Task` (e.g., de `READY` a `MAPPED`, `VALIDATED` o `BADIMAGERY`). |
| **LÃ³gica Espacial (GIS)** | ComprobaciÃ³n de la precisiÃ³n en la subdivisiÃ³n geomÃ©trica (*splitting*) y el recÃ¡lculo dinÃ¡mico de las Ã¡reas de las tareas. |
| **GestiÃ³n de Bloqueos Concurrentes** | ValidaciÃ³n de los mecanismos de asignaciÃ³n y liberaciÃ³n concurrente de tareas, garantizando la ausencia de condiciones de carrera (*race conditions*). |
| **ExposiciÃ³n CartogrÃ¡fica** | ConfirmaciÃ³n de la correcta integraciÃ³n con metadatos y la exportaciÃ³n fidedigna a formatos GIS estÃ¡ndar (XML/GPX). |
| **AuditorÃ­a y Trazabilidad** | AserciÃ³n sobre la inmutabilidad y correcta generaciÃ³n de los registros histÃ³ricos de acciones sobre las tareas (`TaskHistory`). |
| **Operaciones Masivas y ReversiÃ³n** | ValidaciÃ³n de la integridad transaccional durante la modificaciÃ³n en bloque de mÃºltiples tareas y el retroceso (rollback) controlado de operaciones. |

---

## 2. IntegraciÃ³n de Interfaces y Flujo de Datos

Las pruebas diseÃ±adas para este mÃ³dulo aseguran la integridad en la comunicaciÃ³n a travÃ©s de las mÃºltiples capas arquitectÃ³nicas del sistema. Las interacciones principales sujetas a verificaciÃ³n son:

| Capa de Origen | Capa de Destino | PropÃ³sito de la IntegraciÃ³n |
| :--- | :--- | :--- |
| **API Gateway** (FastAPI) | **Capa de Servicios** (`MappingService`, etc.) | ValidaciÃ³n de la correcta interpretaciÃ³n de los DTOs entrantes y el enrutamiento adecuado hacia la lÃ³gica de dominio. |
| **Capa de Servicios** | **Modelos ORM** (`Task`, `TaskHistory`) | TraducciÃ³n fidedigna de las reglas de negocio en estructuras de datos y relaciones gestionadas por SQLAlchemy. |
| **Modelos ORM** | **Motor Base de Datos** (PostGIS) | EjecuciÃ³n precisa de las consultas SQL y manipulaciÃ³n adecuada de los tipos de datos geomÃ©tricos espaciales. |
| **Capa de Servicios** | **Sistemas Externos** (Parsers JOSM) | GeneraciÃ³n de documentos XML estructurados de acuerdo con los estÃ¡ndares esperados por herramientas de mapeo externas. |

---

## 3. Estrategia de Dependencias y Simulaciones (Mocks)

Para garantizar el aislamiento de las pruebas de integraciÃ³n y prevenir falsos negativos derivados de fallos en la infraestructura externa, se ha definido la siguiente estrategia de simulaciÃ³n:

| Dependencia Estructural | ClasificaciÃ³n | Estrategia de Aislamiento en Pruebas |
| :--- | :--- | :--- |
| **AutenticaciÃ³n OSM** | Externa (Red) | **Simulada (Mocked).** Se inyecta un token vÃ¡lido o un usuario de prueba en el entorno efÃ­mero, omitiendo el flujo OAuth real para evitar latencias de red. |
| **PostGIS (GIS)** | Interna (Persistencia) | **No simulada (Real).** Es estrictamente obligatorio el uso de una instancia real de PostgreSQL con la extensiÃ³n PostGIS para asegurar la validez matemÃ¡tica del *clipping* de polÃ­gonos. |
| **Servicio de Notificaciones** | Interna (Eventos) | **Simulada (Mocked).** Se interceptan los eventos emitidos hacia el *bus* interno, validando la emisiÃ³n de la orden sin incurrir en esperas asÃ­ncronas de red. |

---

## 4. Escenarios y Condiciones de IntegraciÃ³n

Se han modelado los siguientes escenarios lÃ³gicos de integraciÃ³n. Cada escenario somete a estrÃ©s a la cadena de comunicaciÃ³n entre las capas del sistema.

### INT-MAP-01: Bloqueo Transaccional Exitoso
| Atributo | EspecificaciÃ³n TÃ©cnica |
| :--- | :--- |
| **Interfaces Evaluadas** | HTTP Endpoint âž” `MappingService` âž” Base de Datos (ORM + SQL) |
| **Precondiciones** | Proyecto publicado; tarea en estado `READY`; usuario con rol `MAPPER` autenticado. |
| **Entrada Requerida** | PeticiÃ³n `POST` a `/lock-for-mapping/{task_id}` con token de sesiÃ³n vÃ¡lido. |
| **Criterios de AceptaciÃ³n** | **1.** Respuesta HTTP 200 OK.<br>**2.** TransiciÃ³n de estado a `LOCKED_FOR_MAPPING` confirmada en PostGIS.<br>**3.** Registro de auditorÃ­a correctamente insertado en `task_history`. |

### INT-MAP-02: GestiÃ³n de Concurrencia (Race Condition)
| Atributo | EspecificaciÃ³n TÃ©cnica |
| :--- | :--- |
| **Interfaces Evaluadas** | HTTP Endpoint âž” `MappingService` âž” Transaccionalidad de Base de Datos |
| **Precondiciones** | Tarea previamente bloqueada (estado `LOCKED_FOR_MAPPING`) por el Usuario A. |
| **Entrada Requerida** | PeticiÃ³n concurrente `POST` a `/lock-for-mapping/{task_id}` originada por el Usuario B. |
| **Criterios de AceptaciÃ³n** | **1.** Respuesta de rechazo (HTTP 409 Conflict o 403 Forbidden).<br>**2.** PreservaciÃ³n del estado y asignaciÃ³n original en la base de datos.<br>**3.** Ausencia de anomalÃ­as en el historial de transacciones de la tarea. |

### INT-MAP-03: SubdivisiÃ³n de GeometrÃ­as (Split)
| Atributo | EspecificaciÃ³n TÃ©cnica |
| :--- | :--- |
| **Interfaces Evaluadas** | HTTP Endpoint âž” `SplitService` âž” Motor Espacial PostGIS |
| **Precondiciones** | Tarea activa con un polÃ­gono geomÃ©trico que supera el umbral de Ã¡rea definido. |
| **Entrada Requerida** | PeticiÃ³n `POST` a `/split/{task_id}`. |
| **Criterios de AceptaciÃ³n** | **1.** Respuesta HTTP 200 OK.<br>**2.** InhabilitaciÃ³n de la tarea matriz original.<br>**3.** CreaciÃ³n en PostGIS de 4 nuevas tareas derivadas, con geometrÃ­as SRID 4326 cuya sumatoria de Ã¡reas equivale con exactitud al polÃ­gono de la tarea matriz. |

### INT-MAP-04: ExportaciÃ³n de Interfaz Externa JOSM (XML)
| Atributo | EspecificaciÃ³n TÃ©cnica |
| :--- | :--- |
| **Interfaces Evaluadas** | HTTP Endpoint âž” `MappingService` âž” Serializador XML |
| **Precondiciones** | Tarea con delimitaciÃ³n geogrÃ¡fica consolidada en la Base de Datos. |
| **Entrada Requerida** | PeticiÃ³n `GET` solicitando los recursos cartogrÃ¡ficos en formato XML. |
| **Criterios de AceptaciÃ³n** | **1.** Respuesta con cabecera `Content-Type: application/xml`.<br>**2.** Cumplimiento estricto del esquema de validaciÃ³n XML requerido por JOSM.<br>**3.** Concordancia exacta entre el atributo *Bounds* del XML y la geometrÃ­a original de PostGIS. |

### INT-MAP-05: EjecuciÃ³n de Operaciones Masivas (Bulk Actions)
| Atributo | EspecificaciÃ³n TÃ©cnica |
| :--- | :--- |
| **Interfaces Evaluadas** | HTTP Endpoint (`actions.py`) âž” `ValidatorService` / `MappingService` âž” Base de Datos |
| **Precondiciones** | Proyecto publicado con mÃºltiples tareas en estados transicionales. Usuario autenticado con privilegios de AdministraciÃ³n o GestiÃ³n de Proyectos (PM). |
| **Entrada Requerida** | Peticiones HTTP a los endpoints masivos (`map-all`, `validate-all`, `reset-all`). |
| **Criterios de AceptaciÃ³n** | **1.** VerificaciÃ³n estricta de permisos administrativos.<br>**2.** MutaciÃ³n masiva exitosa del estado de todas las tareas elegibles.<br>**3.** SincronizaciÃ³n precisa de los contadores estadÃ­sticos maestros del proyecto. |

### INT-MAP-06: Mecanismos de ReversiÃ³n y Control Temporal
| Atributo | EspecificaciÃ³n TÃ©cnica |
| :--- | :--- |
| **Interfaces Evaluadas** | HTTP Endpoint (`actions.py`) âž” `ValidatorService` / `MappingService` âž” Base de Datos |
| **Precondiciones** | Existencia de tareas en estado de revisiÃ³n, marcadas con imÃ¡genes defectuosas (`BADIMAGERY`), o con bloqueos prÃ³ximos a caducar. |
| **Entrada Requerida** | Peticiones HTTP para la extensiÃ³n de bloqueos (`extend-lock-time`) o solicitudes administrativas de reversiÃ³n de asignaciones de un usuario en particular (`revert-user-tasks`). |
| **Criterios de AceptaciÃ³n** | **1.** Para reversiones por calidad, retorno Ã­ntegro de las tareas al estado `READY`.<br>**2.** Para extensiones de tiempo, ampliaciÃ³n exitosa del margen transaccional garantizando la persistencia del bloqueo original sin interrupciones. |

### INT-MAP-07: Consultas de AuditorÃ­a e Historial Protegido
| Atributo | EspecificaciÃ³n TÃ©cnica |
| :--- | :--- |
| **Interfaces Evaluadas** | HTTP Endpoint (`resources.py`) âž” `ValidatorService` âž” SQLAlchemy |
| **Precondiciones** | Historial poblado de tareas mapeadas por un usuario y consecuentemente invalidadas por validadores. |
| **Entrada Requerida** | PeticiÃ³n HTTP a `/queries/own/invalidated/` con provisiÃ³n de cabecera `Authorization`. |
| **Criterios de AceptaciÃ³n** | **1.** ValidaciÃ³n de identidad del token contra el usuario solicitado, emitiendo HTTP 401/403 en caso de discrepancia (protecciÃ³n de privacidad).<br>**2.** Ensamblaje correcto de la paginaciÃ³n y cruce de datos histÃ³ricos retornando un DTO estructuralmente coherente. |

---

### INT-MAP-08: GestiÃ³n de EliminaciÃ³n de Tareas
| Atributo | EspecificaciÃ³n TÃ©cnica |
| :--- | :--- |
| **Interfaces Evaluadas** | HTTP Endpoint (`resources.py`) âž” `ProjectService` âž” Base de Datos |
| **Precondiciones** | Proyecto con tareas generadas; un usuario autenticado con credenciales de Administrador. |
| **Entrada Requerida** | PeticiÃ³n `DELETE` a `/api/v2/projects/{project_id}/tasks/` incluyendo listado de IDs. |
| **Criterios de AceptaciÃ³n** | **1.** RestricciÃ³n perimetral: rechazo total con cÃ³digo HTTP 403 para usuarios sin privilegios administrativos.<br>**2.** Validaciones estrictas del esquema JSON de entrada (rechazando estructuras ausentes o mal formadas).<br>**3.** ConfirmaciÃ³n exitosa de la eliminaciÃ³n vÃ­a `ProjectService`. |

### INT-MAP-09: IntersecciÃ³n Geoespacial de CuadrÃ­culas
| Atributo | EspecificaciÃ³n TÃ©cnica |
| :--- | :--- |
| **Interfaces Evaluadas** | HTTP Endpoint (`resources.py`) âž” `GridService` |
| **Precondiciones** | Archivo GeoJSON vÃ¡lido especificando un polÃ­gono de Ã¡rea de interÃ©s (AOI). |
| **Entrada Requerida** | PeticiÃ³n `PUT` a `/api/v2/projects/{project_id}/tasks/queries/aoi/` con los esquemas cartogrÃ¡ficos. |
| **Criterios de AceptaciÃ³n** | **1.** Parseo y validaciÃ³n de tipos rigurosos usando los modelos de Pydantic (`GridDTO`).<br>**2.** Recorte (trimming) espacial exitoso retornando `FeatureCollection` vÃ¡lidos.<br>**3.** Aseguramiento de la serializaciÃ³n asÃ­ncrona de la API compatible con Starlette. |

*(Nota: Los escenarios INT-MAP-08 e INT-MAP-09 fueron diseÃ±ados e integrados durante la Fase 3 para elevar los indicadores de cobertura a los umbrales exigidos, permitiendo ademÃ¡s descubrir y subsanar bugs crÃ­ticos de asincronÃ­a y delegaciÃ³n de estado en los decoradores perimetrales `pm_only`).*

---

## 5. DiseÃ±o y Arquitectura de las Suites de IntegraciÃ³n

Con el objetivo de preservar una alta cohesiÃ³n y facilitar el mantenimiento continuo, los escenarios descritos se han segmentado lÃ³gicamente en las siguientes suites de pruebas:

| Suite de Pruebas de IntegraciÃ³n | PropÃ³sito Principal | JustificaciÃ³n TÃ©cnica de su Aislamiento |
| :--- | :--- | :--- |
| **`tests/api/integration/api/tasks/test_bulk_actions.py`** | ComprobaciÃ³n de endpoints administrativos que operan de forma masiva sobre colecciones de tareas. | Previene la contaminaciÃ³n y saturaciÃ³n de los tests transaccionales estÃ¡ndar, garantizando que las modificaciones estructurales masivas mantengan la integridad referencial del sistema (Cubre INT-MAP-05). |
| **`tests/api/integration/api/tasks/test_reversions.py`** | ValidaciÃ³n de los flujos de retroceso, deshacer transacciones y gestiÃ³n del ciclo de vida de los bloqueos temporales. | Los flujos de retroceso exigen la construcciÃ³n de precondiciones de base de datos sumamente complejas. Su aislamiento reduce la fragilidad de las pruebas y simplifica su depuraciÃ³n (Cubre INT-MAP-06). |
| **`tests/api/integration/api/tasks/test_resources.py`** | AserciÃ³n del comportamiento de consultas (Queries), exposiciÃ³n de datos histÃ³ricos y validaciÃ³n de polÃ­ticas de seguridad perimetral. | Asegura la resiliencia del sistema ante vulnerabilidades de exposiciÃ³n de datos (ej. manipulaciÃ³n de tokens), comprobando el comportamiento esperado ante errores de autorizaciÃ³n (Cubre INT-MAP-07). |
| **`tests/api/integration/services/test_mapping_service.py`** | ValidaciÃ³n pura de la lÃ³gica de dominio y transiciones de estado, prescindiendo del ruido inducido por la capa de transporte HTTP. | Permite alcanzar un alto grado de cobertura sobre las reglas de negocio nÃºcleo, validando casos de borde como excepciones de permisos cruzados y retrocesos anÃ³malos de estado. |

---

## 6. MÃ©tricas de Cobertura y Niveles de Riesgo Aceptable

El diseÃ±o de las pruebas para este mÃ³dulo se ha regido por estÃ¡ndares rigurosos de calidad de software. Se establece el siguiente objetivo de cobertura, respaldado por la criticidad de los componentes evaluados:

> **Objetivo de Cobertura de Sentencias:** Mayor o igual al **90%** en la capa de servicios principales y controladores. Esta mÃ©trica se certifica empÃ­ricamente sobre la implementaciÃ³n de `mapping_service.py`, `validator_service.py` y los endpoints del dominio (`actions.py` y `resources.py`).

| OperaciÃ³n / LÃ³gica de Negocio | Nivel de Confianza Exigido | JustificaciÃ³n del Riesgo Asumido |
| :--- | :--- | :--- |
| **Operaciones GeomÃ©tricas (`SplitService`)** | **Extremo (100%)** | Un fallo algorÃ­tmico en la subdivisiÃ³n espacial provocarÃ­a una corrupciÃ³n permanente de la topologÃ­a cartogrÃ¡fica almacenada. |
| **Operaciones Masivas (Bulk Actions)** | **Muy Alto (>90%)** | Dado su impacto sistÃ©mico, una falla inadvertida en este componente posee el potencial de invalidar miles de aportes comunitarios simultÃ¡neamente. |
| **LÃ³gica Transaccional (Locks / Estados)** | **Muy Alto (>90%)** | La precisiÃ³n en los bloqueos es el mecanismo primario para evitar colisiones operativas y superposiciÃ³n de trabajos concurrentes sobre un mismo polÃ­gono territorial. |



