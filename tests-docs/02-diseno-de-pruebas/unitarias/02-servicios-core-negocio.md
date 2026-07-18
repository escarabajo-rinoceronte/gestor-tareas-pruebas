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
  <b>Proyecto:</b> HOT Tasking Manager — EspecificaciÃ³n de Pruebas Unitarias: Suite de Servicios Core y LÃ³gica de Negocio <br>
  <b>Fecha de Elaboración:</b> 29/05/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# EspecificaciÃ³n de Pruebas Unitarias: Suite de Servicios Core y LÃ³gica de Negocio

**Responsable:** Test Analyst (Integrante 2)  
**Dominio Funcional:** LÃ³gica de Negocio Backend (FastAPI)  
**EstÃ¡ndar de Referencia:** ISO/IEC/IEEE 29119-4 (EspecificaciÃ³n de DiseÃ±o de Pruebas)  

## 1. Base de Pruebas (Test Basis)

El presente documento establece los fundamentos analÃ­ticos y tÃ©cnicos para el aseguramiento de calidad del mÃ³dulo de servicios del backend de Tasking Manager. Este mÃ³dulo representa el nÃºcleo operativo de la arquitectura funcional, siendo el responsable de orquestar la creaciÃ³n de proyectos, la gestiÃ³n de organizaciones, la administraciÃ³n del ciclo de vida de las tareas cartogrÃ¡ficas y la validaciÃ³n de roles. 

Para cumplir con el estÃ¡ndar ISO 29119, esta base de pruebas delimita el alcance estructural del cÃ³digo fuente a evaluar, define la estrategia tÃ©cnica de aislamiento utilizada en las pruebas existentes y expone los riesgos de negocio que justifican el esfuerzo de validaciÃ³n. El objetivo actual consiste en mapear el comportamiento tÃ©cnico de estos componentes para habilitar el futuro diseÃ±o detallado de casos lÃ­mite.

### 1.1. Arquitectura TÃ©cnica y Estrategia de Aislamiento

Las pruebas unitarias implementadas para el mÃ³dulo de servicios operan bajo un paradigma de aislamiento estricto. El framework de testing adoptado por el proyecto es `pytest`, el cual interactÃºa profundamente con el motor asÃ­ncrono de FastAPI. Para garantizar que las pruebas del nÃºcleo de negocio evalÃºen Ãºnicamente la lÃ³gica algorÃ­tmica y no la infraestructura subyacente, el equipo de desarrollo ha estructurado un ecosistema avanzado de *fixtures* y generadores de estado.

El siguiente diagrama ilustra cÃ³mo se estructura la ejecuciÃ³n de una prueba unitaria tÃ­pica dentro de esta suite, garantizando que el servicio evaluado no genere mutaciones persistentes indeseadas ni dependa de latencias de red.

![Estrategia de aislamiento](/tests-docs/02-diseno-de-pruebas/unitarias/img/estrategia-aislamiento.png) 

*(PropÃ³sito del diagrama: Demostrar el modelo de aislamiento de dependencias. Se evidencia cÃ³mo las "Canned Factories" y los "Mocks" envuelven al Servicio Core para asegurar la determinidad de la prueba, mitigando el riesgo de falsos positivos en el pipeline de CI/CD).*

### 1.2. AnÃ¡lisis Detallado de Componentes CrÃ­ticos

El repositorio revela que la lÃ³gica de negocio se encuentra fragmentada en servicios altamente especializados ubicados en el directorio `backend/services/`. Entre los componentes mÃ¡s crÃ­ticos que exigen cobertura estructural se encuentran el servicio de proyectos (`project_service.py`), el servicio de tareas (`task_service.py`) y el servicio de organizaciones (`organisation_service.py`). 

La criticidad del servicio de tareas radica en el manejo de la concurrencia. Cuando mÃºltiples mapeadores intentan bloquear un mismo polÃ­gono espacial simultÃ¡neamente, el servicio debe prevenir condiciones de carrera (Race Conditions) mediante bloqueos transaccionales seguros. Cualquier brecha funcional en este componente resultarÃ­a en la corrupciÃ³n de los datos de contribuciÃ³n. Por su parte, los servicios de proyectos y organizaciones actÃºan como guardianes del control de acceso, requiriendo un anÃ¡lisis profundo sobre la segregaciÃ³n de roles.

### 1.3. Comportamiento y Cobertura Actual: Servicio de Organizaciones

Como prueba de concepto del nivel de anÃ¡lisis requerido para esta suite, se ha auditado exhaustivamente el archivo `tests/backend/base/services/test_organisation_service.py`. Este archivo concentra las validaciones orientadas al comportamiento del servicio principal de organizaciones (`OrganisationService`), garantizando que la recuperaciÃ³n y manipulaciÃ³n de entidades respeten las reglas de autorizaciÃ³n del sistema.

Dentro de la lÃ³gica de negocio, estas pruebas aseguran una correcta segregaciÃ³n de roles. El comportamiento esperado y automatizado dictamina que un usuario regular (mapeador) Ãºnicamente puede visualizar e interactuar con las organizaciones en las que ha sido designado explÃ­citamente como administrador local (*manager*). En contraposiciÃ³n, la lÃ³gica tÃ©cnica debe asegurar que un perfil con privilegios globales (`UserRole.ADMIN`) obtenga acceso absoluto a la colecciÃ³n completa de organizaciones, eludiendo las restricciones de asignaciÃ³n directa.

A nivel de implementaciÃ³n, las pruebas existentes dependen fuertemente de la inyecciÃ³n de fÃ¡bricas de datos conocidas como *canned factories* (especÃ­ficamente `create_canned_organisation` y `create_canned_user`). Estas herramientas permiten inicializar el estado de la base de datos temporal con entidades precisas antes de ejecutar las aserciones, tal como se observa en la configuraciÃ³n fundamental (fixture) de la clase de pruebas:

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

A travÃ©s de esta suite automatizada, el proyecto actualmente previene y mitiga el riesgo de escalada de privilegios. Adicionalmente, las pruebas existentes garantizan que las consultas sobre identificadores inexistentes no desencadenen fallos catastrÃ³ficos a nivel de framework (HTTP 500), forzando al servicio a capturar la anomalÃ­a y emitir una excepciÃ³n controlada de tipo `NotFound`.

### 1.4. IdentificaciÃ³n de VacÃ­os y Estrategia de ExpansiÃ³n

A pesar de la solidez tÃ©cnica evidenciada en las pruebas del servicio de organizaciones, el anÃ¡lisis holÃ­stico del mÃ³dulo revela Ã¡reas funcionales con baja cobertura. Actualmente, el repositorio exhibe una sÃ³lida cobertura sobre los "caminos felices" (Happy Paths) y la validaciÃ³n bÃ¡sica de roles. No obstante, existe un vacÃ­o documental y procedimental respecto a escenarios transaccionales lÃ­mite.

La estrategia a implementar por los Test Designers en la prÃ³xima iteraciÃ³n consistirÃ¡ en aplicar tÃ©cnicas de diseÃ±o de caja negra, como el AnÃ¡lisis de Valores LÃ­mite, sobre los algoritmos de divisiÃ³n geomÃ©trica en el `project_service.py` y tÃ©cnicas de Tabla de Decisiones para los estados de transiciÃ³n en el `task_service.py`. Estas pruebas serÃ¡n especificadas funcionalmente en esta Wiki para que los desarrolladores las implementen posteriormente utilizando TDD.

## 2. Condiciones de Prueba (TD2) y Cobertura (TD3)

A partir del anÃ¡lisis funcional, se establecen las siguientes condiciones lÃ³gicas transversales que deberÃ¡n ser garantizadas por los scripts de prueba a lo largo del ciclo de vida del mÃ³dulo.

| ID CondiciÃ³n | Funcionalidad Core a Evaluar | TÃ©cnica ISO 29119-4 Aplicable |
| :--- | :--- | :--- |
| COND-CORE-01 | VisualizaciÃ³n de organizaciones limitada al rol de *Manager* frente a rol *Admin*. | Tabla de Decisiones |
| COND-CORE-02 | Captura controlada de excepciones al consultar entidades inexistentes. | ParticiÃ³n de Equivalencia |
| COND-CORE-03 | PrevenciÃ³n de bloqueos simultÃ¡neos sobre una misma tarea cartogrÃ¡fica (Concurrencia). | Casos de Uso / Diagrama de TransiciÃ³n de Estados |

## 3. Casos de Prueba (TD4 y TD6)

La siguiente secciÃ³n registra la trazabilidad de los casos de prueba que ya han sido desarrollados en el cÃ³digo fuente, validando las condiciones analizadas previamente. El diseÃ±o exhaustivo de los casos lÃ­mite faltantes se ejecutarÃ¡ en las siguientes semanas del cronograma funcional.

### 3.1. Pruebas Implementadas Existentes (Test Scripts)

El siguiente registro asegura que los esfuerzos de desarrollo actuales posean un respaldo funcional documentado, permitiendo conectar el requisito de negocio con el comportamiento automatizado.

| ID Caso | ID CondiciÃ³n | Comportamiento Esperado y Validado | Componente Automatizado | Estado |
| :--- | :--- | :--- | :--- | :--- |
| TC-ORG-001 | COND-CORE-02 | Retorna la entidad exacta cuando la consulta se realiza con un ID numÃ©rico vÃ¡lido. | `test_organisation_service.py` | Automatizado |
| TC-ORG-002 | COND-CORE-02 | Lanza excepciÃ³n `NotFound` (HTTP 404) cuando el ID de la organizaciÃ³n no existe en base de datos. | `test_organisation_service.py` | Automatizado |
| TC-ORG-003 | COND-CORE-01 | Retorna lista filtrada de organizaciones cuando el usuario posee rol *Manager*, excluyendo las no asignadas. | `test_organisation_service.py` | Automatizado |

### 3.2. Brechas Funcionales (Nuevas Pruebas a Implementar)

A continuaciÃ³n, se documentan las brechas identificadas que requieren ser priorizadas en las prÃ³ximas asignaciones de TDD.

| ID Caso | ID CondiciÃ³n | DescripciÃ³n de la RestricciÃ³n LÃ³gica | Resultado Esperado | Estado QA |
| :--- | :--- | :--- | :--- | :--- |
| TC-TSK-001 | COND-CORE-03 | Mapeador intenta bloquear una tarea que fue bloqueada hace menos de 1 segundo por otro usuario. | ExcepciÃ³n `TaskAlreadyLocked` | Pendiente TDD |
| TC-PRJ-001 | N/A | Administrador intenta crear un proyecto de mapeo sin definir un polÃ­gono GeoJSON vÃ¡lido. | Error de validaciÃ³n de entidad (400) | Pendiente TDD |

## 4. MÃ©tricas Base de Cobertura de DiseÃ±o

*Nota: Estas mÃ©tricas reflejan Ãºnicamente la porciÃ³n auditada del servicio de organizaciones y evolucionarÃ¡n a medida que los Test Analysts completen el mapeo del servicio de tareas y proyectos.*

*   Total de Elementos de Cobertura Identificados (T): 5 (Casos TC-ORG-001 al TC-PRJ-001)
*   Total de Elementos Ejecutados/Automatizados (N): 3 (Casos ORG)
*   Cobertura de DiseÃ±o Inicial ($N/T * 100\%$): 60%



