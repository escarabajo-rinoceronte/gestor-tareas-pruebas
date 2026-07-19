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
  <b>Proyecto:</b> HOT Tasking Manager — Especificación de Pruebas Unitarias: Suite de Servicios Core y Lógica de Negocio <br>
  <b>Fecha de Elaboración:</b> 29/05/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Especificación de Pruebas Unitarias: Suite de Servicios Core y Lógica de Negocio

**Responsable:** Test Analyst (Integrante 2)  
**Dominio Funcional:** Lógica de Negocio Backend (FastAPI)  
**Estándar de Referencia:** ISO/IEC/IEEE 29119-4 (Especificación de Diseño de Pruebas)  

## 1. Base de Pruebas (Test Basis)

El presente documento establece los fundamentos analíticos y técnicos para el aseguramiento de calidad del módulo de servicios del backend de Tasking Manager. Este módulo representa el núcleo operativo de la arquitectura funcional, siendo el responsable de orquestar la creación de proyectos, la gestión de organizaciones, la administración del ciclo de vida de las tareas cartográficas y la validación de roles. 

Para cumplir con el estándar ISO 29119, esta base de pruebas delimita el alcance estructural del código fuente a evaluar, define la estrategia técnica de aislamiento utilizada en las pruebas existentes y expone los riesgos de negocio que justifican el esfuerzo de validación. El objetivo actual consiste en mapear el comportamiento técnico de estos componentes para habilitar el futuro diseño detallado de casos límite.

### 1.1. Arquitectura Técnica y Estrategia de Aislamiento

Las pruebas unitarias implementadas para el módulo de servicios operan bajo un paradigma de aislamiento estricto. El framework de testing adoptado por el proyecto es `pytest`, el cual interactúa profundamente con el motor asíncrono de FastAPI. Para garantizar que las pruebas del núcleo de negocio evalúen únicamente la lógica algorítmica y no la infraestructura subyacente, el equipo de desarrollo ha estructurado un ecosistema avanzado de *fixtures* y generadores de estado.

El siguiente diagrama ilustra cómo se estructura la ejecución de una prueba unitaria típica dentro de esta suite, garantizando que el servicio evaluado no genere mutaciones persistentes indeseadas ni dependa de latencias de red.

![Estrategia de aislamiento](/tests-docs/02-diseno-de-pruebas/unitarias/img/estrategia-aislamiento.png) 

*(Propósito del diagrama: Demostrar el modelo de aislamiento de dependencias. Se evidencia cómo las "Canned Factories" y los "Mocks" envuelven al Servicio Core para asegurar la determinidad de la prueba, mitigando el riesgo de falsos positivos en el pipeline de CI/CD).*

### 1.2. Análisis Detallado de Componentes Críticos

El repositorio revela que la lógica de negocio se encuentra fragmentada en servicios altamente especializados ubicados en el directorio `backend/services/`. Entre los componentes más críticos que exigen cobertura estructural se encuentran el servicio de proyectos (`project_service.py`), los servicios de tareas (`mapping_service.py` y `validator_service.py`), el motor de división geométrica (`grid/split_service.py`), además de los servicios auxiliares (`project_admin_service.py`, `team_service.py`, `campaign_service.py` y `project_search_service.py`). 

La criticidad del servicio de tareas radica en el manejo de la concurrencia. Cuando múltiples mapeadores intentan bloquear un mismo polígono espacial simultáneamente, el servicio debe prevenir condiciones de carrera (Race Conditions) mediante bloqueos transaccionales seguros. Cualquier brecha funcional en este componente resultaría en la corrupción de los datos de contribución. Por su parte, los servicios de proyectos y organizaciones actúan como guardianes del control de acceso, requiriendo un análisis profundo sobre la segregación de roles.

### 1.3. Comportamiento y Cobertura Actual: Servicio de Organizaciones

Como prueba de concepto del nivel de análisis requerido para esta suite, se ha auditado exhaustivamente el archivo `tests/backend/base/services/test_organisation_service.py`. Este archivo concentra las validaciones orientadas al comportamiento del servicio principal de organizaciones (`OrganisationService`), garantizando que la recuperación y manipulación de entidades respeten las reglas de autorización del sistema.

Dentro de la lógica de negocio, estas pruebas aseguran una correcta segregación de roles. El comportamiento esperado y automatizado dictamina que un usuario regular (mapeador) únicamente puede visualizar e interactuar con las organizaciones en las que ha sido designado explícitamente como administrador local (*manager*). En contraposición, la lógica técnica debe asegurar que un perfil con privilegios globales (`UserRole.ADMIN`) obtenga acceso absoluto a la colección completa de organizaciones, eludiendo las restricciones de asignación directa.

A nivel de implementación, las pruebas existentes dependen fuertemente de la inyección de fábricas de datos conocidas como *canned factories* (específicamente `create_canned_organisation` y `create_canned_user`). Estas herramientas permiten inicializar el estado de la base de datos temporal con entidades precisas antes de ejecutar las aserciones, tal como se observa en la configuración fundamental (fixture) de la clase de pruebas:

```python
    @pytest.fixture(autouse=True)
    async def setup_test_data(self, db_connection_fixture, request):
        assert db_connection_fixture is not None, "Database connection is not available"

        request.cls.test_org = await create_canned_organisation(db_connection_fixture)
        request.cls.test_user = await create_canned_user(db_connection_fixture)
        request.cls.db = db_connection_fixture

        assert self.test_org is not None, "Failed to create test organisation"
        assert self.test_user is not None, "Failed to create test user"
```

A través de esta suite automatizada, el proyecto actualmente previene y mitiga el riesgo de escalada de privilegios. Adicionalmente, las pruebas existentes garantizan que las consultas sobre identificadores inexistentes no desencadenen fallos catastróficos a nivel de framework (HTTP 500), forzando al servicio a capturar la anomalía y emitir una excepción controlada de tipo `NotFound`.

### 1.4. Identificación de Vacíos y Estrategia de Expansión

El análisis holístico derivado de la ejecución (que reveló una cobertura global del 52% en la capa Core) expone deficiencias críticas en la evaluación de escenarios límite, el manejo de excepciones de base de datos y la seguridad a nivel funcional.

La estrategia de expansión adoptada consistirá en inyectar fallos transaccionales (simulando excepciones como `IntegrityError` mediante Mocks) y aserciones de control de roles (captura de errores `403 Forbidden` / `AuthorizationError`). Se aplicarán técnicas de partición de equivalencia y tablas de decisiones para garantizar que componentes como `project_search_service.py` (filtros dinámicos) y `team_service.py` (jerarquías) validen las reglas de negocio en su totalidad, mitigando vulnerabilidades críticas como el *Broken Access Control*.

## 2. Condiciones de Prueba (TD2) y Cobertura (TD3)

A partir del análisis funcional y la revisión de cobertura, se establecen las siguientes condiciones lógicas transversales que deberán ser garantizadas por los scripts de prueba.

| ID Condición | Funcionalidad Core a Evaluar | Técnica ISO 29119-4 Aplicable |
| :--- | :--- | :--- |
| COND-CORE-01 | Visualización de organizaciones limitada al rol de *Manager* frente a rol *Admin*. | Tabla de Decisiones |
| COND-CORE-02 | Captura controlada de excepciones al consultar entidades inexistentes. | Partición de Equivalencia |
| COND-CORE-03 | Prevención de bloqueos simultáneos sobre una misma tarea cartográfica (Concurrencia). | Casos de Uso / Diagrama de Transición de Estados |
| COND-CORE-04 | Validación combinada de filtros dinámicos en búsquedas de proyectos. | Partición de Equivalencia |
| COND-CORE-05 | Aislamiento y denegación de privilegios no autorizados en jerarquías y modificaciones. | Tabla de Decisiones |
| COND-CORE-06 | Rollback seguro ante fallos transaccionales en base de datos. | Transición de Estados / Partición |
| COND-CORE-07 | Integridad referencial ante intento de eliminación de entidades acopladas (borrado físico). | Análisis de Valores Límite |

## 3. Casos de Prueba (TD4 y TD6)

La siguiente sección registra la trazabilidad de los casos de prueba implementados y por implementar, asegurando que las nuevas especificaciones impacten directamente en la robustez y cobertura de los componentes del módulo.

### 3.1. Pruebas Implementadas Existentes (Test Scripts)

El siguiente registro asegura que los esfuerzos de desarrollo actuales (línea base) posean un respaldo funcional documentado.

| ID Caso | ID Condición | Comportamiento Esperado y Validado | Componente Automatizado | Estado |
| :--- | :--- | :--- | :--- | :--- |
| TC-ORG-001 | COND-CORE-02 | Retorna la entidad exacta cuando la consulta se realiza con un ID numérico válido. | `test_organisation_service.py` | Automatizado |
| TC-ORG-002 | COND-CORE-02 | Lanza excepción `NotFound` (HTTP 404) cuando el ID de la organización no existe en base de datos. | `test_organisation_service.py` | Automatizado |
| TC-ORG-003 | COND-CORE-01 | Retorna lista filtrada de organizaciones cuando el usuario posee rol *Manager*, excluyendo las no asignadas. | `test_organisation_service.py` | Automatizado |

### 3.2. Brechas Funcionales (Nuevas Pruebas a Implementar)

A continuación, se documentan los nuevos escenarios diseñados para subsanar los vacíos de cobertura identificados (incremento esperado del 52% al >85%). Estas pruebas guiarán las futuras iteraciones de TDD y priorizan las nuevas suites identificadas.

| ID Caso | ID Condición | Componente Evaluado | Comportamiento y Justificación (Propósito) | Resultado Esperado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-TSK-001 | COND-CORE-03 | `mapping_service.py` | **Concurrencia:** Mapeador intenta bloquear una tarea bloqueada hace menos de 1 segundo. Justificación: Prevención de Race Conditions en el mapeo activo. | Excepción `TaskAlreadyLocked` | Pendiente TDD |
| TC-PRJ-001 | N/A | `project_service.py` | **Geometría:** Crear proyecto de mapeo sin polígono GeoJSON válido. Justificación: Salvaguardar integridad de datos PostGIS. | Error 400 (Invalid GeoJSON) | Pendiente TDD |
| TC-SRC-001 | COND-CORE-04 | `project_search_service.py` | **Filtros Múltiples:** Construcción dinámica de consulta usando combinaciones de nivel, rol y texto. Justificación: Cubrir las ramas `if` de los queries dinámicos. | Lista filtrada de DTOs | Pendiente TDD |
| TC-SRC-002 | COND-CORE-04 | `project_search_service.py` | **Filtros Inválidos:** Inyección de parámetros de búsqueda corruptos o inexistentes. Justificación: Validación de entradas y prevención de caídas HTTP 500. | Colección vacía controlada | Pendiente TDD |
| TC-TEA-001 | COND-CORE-05 | `team_service.py` | **Broken Access Control:** Usuario sin rol intenta añadir miembros a un equipo ajeno. Justificación: Forzar el control de roles RBAC en jerarquías críticas. | Excepción `403 Forbidden` | Pendiente TDD |
| TC-TEA-002 | COND-CORE-07 | `team_service.py` | **Integridad Relacional:** Borrado físico de un equipo vinculado a proyectos en ejecución. Justificación: Asegurar desconexión de relaciones Many-to-Many. | Retorno seguro / Modificación | Pendiente TDD |
| TC-VAL-001 | COND-CORE-06 | `validator_service.py` | **Rollback Seguro:** Inyección de `IntegrityError` (Mock) durante la validación masiva. Justificación: Confirmar propiedad ACID de las transacciones (ejecución del bloque except). | Excepción controlada (Rollback) | Pendiente TDD |
| TC-ADM-001 | COND-CORE-07 | `project_admin_service.py` | **Borrado Temerario:** Intento de eliminación (`delete`) de un proyecto con tareas ya mapeadas. Justificación: Probar protección de dependencias foráneas. | Excepción de Restricción | Pendiente TDD |
| TC-PRJ-002 | COND-CORE-05 | `project_service.py` | **Mutación No Autorizada:** Modificación de metadatos de un proyecto de mapeo sin privilegios de Manager. Justificación: Seguridad a nivel de controlador. | Excepción `403 Forbidden` | Pendiente TDD |
| TC-SRC-003 | COND-CORE-04 | `project_search_service.py` | **Filtro Texto y Localización:** Búsqueda combinando text_search y preferred_locale. Justificación: Cobertura de la generación de subqueries to_tsquery y param. | DTOs filtrados | Implementado |
| TC-SRC-004 | COND-CORE-04 | `project_search_service.py` | **Intereses de Usuario:** Búsqueda filtrando por intereses (based_on_user_interests=True). Justificación: Cobertura de la subconsulta a project_interests. | DTOs filtrados | Implementado |
| TC-SRC-005 | COND-CORE-04 | `project_search_service.py` | **Mapeado y Favoritos:** Búsqueda combinando mapped_by y favorited_by. Justificación: Cobertura de ramas condicionales de actividad de usuario. | DTOs filtrados | Implementado |
| TC-SRC-006 | COND-CORE-04 | `project_search_service.py` | **Filtros de Acción:** Búsqueda con action="map" y action="validate". Justificación: Alcanzar la verificación interna de permisos de mapeo/validación. | DTOs filtrados | Implementado |
| TC-SRC-007 | COND-CORE-04 | `project_search_service.py` | **Organizaciones y Metadatos:** Filtro por organisation_id, team_id, sandbox, mapping_types. Justificación: Cobertura de múltiples IFs simultáneos en _filter_projects. | DTOs filtrados | Implementado |
| TC-SRC-008 | COND-CORE-04 | `project_search_service.py` | **Ordenamiento de Porcentajes:** Uso de order_by='percent_mapped' (DESC). Justificación: Validación de SQL CASE generada dinámicamente. | DTOs ordenados | Implementado |
| TC-SRC-009 | N/A | `project_search_service.py` | **GeoJSON Válido:** Generación de FeatureCollection desde un BBox SRID 4326. Justificación: Cobertura de cálculo de intersección y conversión geométrica. | geojson.FeatureCollection | Implementado |
| TC-SRC-010 | N/A | `project_search_service.py` | **BBox Excedido:** Solicitud geoespacial con BBox mayor al MAX_AREA. Justificación: Prevención de denegación de servicio (DoS) por mapas gigantes. | Excepción `BBoxTooBigError` | Implementado |
| TC-SRC-011 | N/A | `project_search_service.py` | **Exportación CSV:** Generación de CSV mediante `search_projects_as_csv` con `as_csv=True`. Justificación: Cobertura completa del flujo de exportación y transformación de datos tabulares. | `str` (CSV) | Implementado |
| TC-SRC-012 | COND-CORE-04 | `project_search_service.py` | **Fechas y Localización:** Filtros combinados de rango de fechas (`created_gte/lte`, `last_updated_gte/lte`), country e imagery `custom`. Justificación: Cobertura de ramas temporales y geográficas. | DTOs filtrados | Implementado |
| TC-SRC-013 | COND-CORE-04 | `project_search_service.py` | **Partnerships y Gestión:** Filtros de partnership (`partner_id`, `partnership_from/to`), `created_by`, `managed_by`, `organisation_name` e `interests`. Justificación: Ramas de filtros complejos. | DTOs filtrados | Implementado |
| TC-SRC-014 | COND-CORE-04 | `project_search_service.py` | **DRAFT sin autenticación:** Estado DRAFT solicitado sin usuario logueado. Justificación: Rama que fuerza `FALSE` en la query al no permitir DRAFT para anónimos. | Excepción `NotFound` | Implementado |
| TC-SRC-015 | COND-CORE-04 | `project_search_service.py` | **DRAFT con usuario:** Estado DRAFT solicitado por usuario no-admin. Justificación: Cobertura de la lógica condicional de `managed_projects` para filtrado DRAFT. | DTOs filtrados o `NotFound` | Implementado |
| TC-SRC-016 | COND-CORE-04 | `project_search_service.py` | **Paginación con COUNT:** Búsqueda con `omit_map_results=True`. Justificación: Rama de paginación con `SELECT COUNT(*)` en vez de `fetch_all` completo. | DTOs paginados | Implementado |
| TC-SRC-017 | COND-CORE-04 | `project_search_service.py` | **Imagery Específico:** Filtro con URL de imagery completa (no `custom`). Justificación: Rama `else` del filtro de imagery con coincidencia exacta. | DTOs filtrados | Implementado |
| TC-SRC-018 | COND-CORE-04 | `project_search_service.py` | **Ordenamiento Genérico:** `order_by="id"` para cubrir la rama `else` del orden dinámico SQL. Justificación: Construcción de cláusula ORDER BY con columna arbitraria. | DTOs ordenados | Implementado |

*(Nota: Las nuevas suites automatizadas como `test_project_search_service.py`, `test_team_service.py` y `test_project_admin_service.py` adoptarán estos escenarios como objetivo central durante su expansión).*


## 4. Métricas Base de Cobertura de Diseño

*Nota: Estas métricas reflejan la línea base identificada más el conjunto de expansiones requeridas.*

*   Total de Elementos de Cobertura Identificados (T): 12 (Casos automatizados + nuevos diseños)
*   Total de Elementos Ejecutados/Automatizados (N): 3 (Casos ORG)
*   Cobertura de Diseño Inicial ($N/T * 100\%$): 25% (Refleja la madurez documentada al término de la fase analítica).
