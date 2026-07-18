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
  <b>Proyecto:</b> HOT Tasking Manager — Plan de Pruebas Unitarias (Fase 1) <br>
  <b>Fecha de Elaboración:</b> 11/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Plan de Pruebas Unitarias (Fase 1)

**Proyecto:** HOT OSM Tasking Manager  
**Fase de EjecuciÃ³n:** Fase 1 - Pruebas Unitarias Backend  
**EstÃ¡ndar de Referencia:** ISO/IEC/IEEE 29119-3 (Sub-process Test Plan)  

## 1. PropÃ³sito y Enfoque del Documento
El presente documento define la estrategia, organizaciÃ³n y planificaciÃ³n logÃ­stica exclusiva para la fase de Pruebas Unitarias del proyecto Tasking Manager. A diferencia de las fases posteriores que evaluarÃ¡n flujos de usuario, esta etapa inicial se concentra estrictamente en la validaciÃ³n estructural y funcional de los componentes aislados del backend, desarrollado sobre el framework FastAPI. 

En alineaciÃ³n con los lineamientos del Plan General de Pruebas, el esfuerzo primario consiste en delimitar exhaustivamente el alcance de los mÃ³dulos, identificar las funcionalidades crÃ­ticas que requieren cobertura y establecer un marco de trabajo coordinado que permita la posterior implementaciÃ³n bajo enfoques de desarrollo guiado por pruebas (TDD) y desarrollo guiado por comportamiento (BDD).

## 2. Alcance Funcional de la Fase Unitaria
El anÃ¡lisis estructural del cÃ³digo fuente ha permitido sectorizar el esfuerzo de aseguramiento de calidad en tres grandes dominios funcionales:

- Seguridad, Usuarios y Servicios de ComunicaciÃ³n, el cual abarca la lÃ³gica de autenticaciÃ³n OAuth, el control de acceso basado en roles (RBAC) y los mecanismos de notificaciÃ³n interna. El aseguramiento de este bloque es crÃ­tico debido a la sensibilidad de los datos de los mapeadores.

- Servicios Core y la LÃ³gica de Negocio. Este sector representa el nÃºcleo operativo de la plataforma, responsabilizÃ¡ndose por la creaciÃ³n de Ã¡reas de interÃ©s, la concurrencia en el bloqueo de tareas y la orquestaciÃ³n del ciclo de vida cartogrÃ¡fico.

- Modelos, Objetos de Transferencia de Datos (DTOs) y Validaciones Base, garantizando que las estructuras de datos que interactÃºan con la base espacial PostGIS posean integridad antes de cualquier transacciÃ³n de persistencia. La documentaciÃ³n actual se centrarÃ¡ en la delimitaciÃ³n de estas Ã¡reas, preparando el terreno para el diseÃ±o detallado en iteraciones venideras.

## 3. OrganizaciÃ³n del Equipo y AsignaciÃ³n de Roles
La gestiÃ³n de esta fase requiere una distribuciÃ³n tÃ©cnica precisa de los seis integrantes proyectados para el equipo de Aseguramiento de Calidad. La asignaciÃ³n obedece a las responsabilidades formales definidas en el Plan General, garantizando que el diseÃ±o estratÃ©gico, el anÃ¡lisis de mÃ³dulos y la ejecuciÃ³n tÃ©cnica posean responsables directos.

Actualmente, el **Test Lead** (un integrante) asume la direcciÃ³n de la fase, gestionando el cronograma general, validando la consistencia documental y supervisando el dominio de Seguridad y Comunicaciones. En paralelo, el rol de **Test Analyst** ha sido asignado a dos integrantes, quienes actualmente se encuentran realizando el anÃ¡lisis estÃ¡tico de los Servicios Core y los DTOs. Su responsabilidad radica en mapear el cÃ³digo existente e identificar las funcionalidades a probar, sin descender al diseÃ±o de casos. 

La arquitectura del entorno de pruebas, incluyendo la configuraciÃ³n de *pytest*, la orquestaciÃ³n de *mocks* y la integraciÃ³n de mÃ©tricas en GitHub Actions, recae sobre un Ãºnico **Test Architect**. Finalmente, los dos miembros restantes asumirÃ¡n el rol de **Test Designer** en la siguiente iteraciÃ³n, tomando el anÃ¡lisis previo para redactar las especificaciones formales de entradas, salidas y tÃ©cnicas de caja negra aplicables.

*(PropÃ³sito del diagrama: Visualizar la jerarquÃ­a operativa y la dependencia entre los roles tÃ©cnicos del equipo de QA durante la fase de pruebas unitarias).*

![Flujo de trabajo en equipo](/tests-docs/01-plan-de-pruebas/02-plan-pruebas-unitarias/img/flujo-trabajo-equipo.png) 

## 4. GestiÃ³n del Cronograma y OperaciÃ³n mediante GitHub Projects
Para garantizar el cumplimiento de los hitos documentales y de ejecuciÃ³n, se ha determinado que GitHub Projects posee la capacidad tÃ©cnica necesaria para gobernar el cronograma QA, siempre y cuando abandone su estructura bÃ¡sica y evolucione hacia una herramienta de gestiÃ³n de ciclo de vida de pruebas. 

### 4.1. Uso de GitHub Projects
El tablero dejarÃ¡ de ser un simple repositorio de tareas aisladas para convertirse en el nÃºcleo de trazabilidad operativa. Para lograrlo, la vista Kanban tradicional se complementarÃ¡ obligatoriamente con una vista de Cronograma (Timeline/Roadmap). Cada tarjeta generada en el tablero representarÃ¡ un mÃ³dulo o Ã©pica de prueba y deberÃ¡ contar obligatoriamente con los campos personalizados de *Esfuerzo Estimado* (en puntos o dÃ­as), *Prioridad de Negocio*, *Rol Asignado* y *Milestone* (IteraciÃ³n).

El flujo de los estados en GitHub Projects reflejarÃ¡ el proceso metodolÃ³gico estipulado por ISO 29119. Las tareas iniciarÃ¡n en el *Backlog QA*, transitando hacia la fase de *AnÃ¡lisis Estructural*, donde los Test Analysts delimitarÃ¡n el alcance del mÃ³dulo. Posteriormente, las tarjetas avanzarÃ¡n al estado de *DiseÃ±o de Pruebas*, habilitando a los Test Designers para estructurar las condiciones lÃ³gicas. Una vez finalizado el diseÃ±o, la tarea pasarÃ¡ a *RevisiÃ³n Documental*, estado en el cual el Test Lead auditarÃ¡ la propuesta mediante Pull Requests. Ãšnicamente tras la aprobaciÃ³n, la tarea alcanzarÃ¡ el estado de *ImplementaciÃ³n*, donde el cÃ³digo serÃ¡ desarrollado e integrado.

*(PropÃ³sito del diagrama: Estandarizar el flujo de estados de las tarjetas en GitHub Projects, asegurando que el avance del cronograma estÃ© atado a hitos formales de validaciÃ³n documental).*

![Flujo de trabajo en GitHub Projects](/tests-docs/01-plan-de-pruebas/02-plan-pruebas-unitarias/img/flujo-en-github-projects.png) 

## 5. Estrategia de CoordinaciÃ³n y Seguimiento
La coordinaciÃ³n entre los analistas funcionales y la arquitectura tÃ©cnica se gestionarÃ¡ mediante ciclos de sincronizaciÃ³n semanales. Durante estas iteraciones, el objetivo principal serÃ¡ poblar la matriz de trazabilidad con los hallazgos estructurales. La comunicaciÃ³n y el seguimiento del cronograma dependerÃ¡n enteramente de las fechas de vencimiento configuradas en los *Milestones* de GitHub.

Cualquier desviaciÃ³n en el esfuerzo estimado por parte de los Test Analysts deberÃ¡ ser documentada en los comentarios del *Issue* correspondiente, permitiendo al Test Lead ajustar la vista de cronograma de manera dinÃ¡mica sin afectar la ruta crÃ­tica del proyecto. La transiciÃ³n formal hacia la fase de diseÃ±o de pruebas detalladas solo ocurrirÃ¡ cuando los tres dominios funcionales hayan sido completamente delimitados y mapeados contra el cÃ³digo fuente existente en el repositorio.


