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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — DiseÃ±o de Pruebas Funcionales: MOD-06 - Gobernanza (Organizaciones y Equipos)</td></tr>
      <tr><td class="label">Fecha</td><td>12/06/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# DiseÃ±o de Pruebas Funcionales: MOD-06 - Gobernanza (Organizaciones y Equipos)
**VersiÃ³n del Documento:** 1.0
**Tipo de AnÃ¡lisis:** DiseÃ±o de Pruebas de Sistema (Caja Negra)

---

## 1. Contexto del MÃ³dulo

Este mÃ³dulo gestiona la estructura jerÃ¡rquica de agrupaciones de usuarios y la delegaciÃ³n de permisos dentro de la plataforma. Su responsabilidad principal es la creaciÃ³n y administraciÃ³n de Organizaciones y Equipos, controlando sus polÃ­ticas de visibilidad (`PUBLIC`, `PRIVATE`), mÃ©todos de ingreso (`ANY`, `BY_REQUEST`, `BY_INVITE`) y orquestando el ciclo de vida de las solicitudes de membresÃ­a para segmentar de forma segura el acceso a los proyectos.

*Para consultar el detalle exhaustivo de los actores, restricciones y reglas de negocio, referirse al [CatÃ¡logo de Requerimientos Funcionales](/tests-docs/02-diseno-de-pruebas/funcionales/00-requerimientos-funcionales.md).*

---

## 2. Estrategia de DiseÃ±o de Pruebas

### 2.1. Enfoque general

El enfoque de pruebas para este mÃ³dulo serÃ¡ de extremo a extremo (End-to-End), orientado fuertemente a la validaciÃ³n del Control de Acceso Basado en Roles (RBAC) y la correcta segregaciÃ³n de privilegios. 

La estrategia evaluarÃ¡ dos perspectivas complementarias: la del actor administrativo (**`Project Manager` ACT-0004** o **`SysAdmin` ACT-0005**) encargado de configurar las polÃ­ticas de gobernanza, y la del actor base (**`MAPPER` ACT-0002**) que interactÃºa con estas estructuras para solicitar membresÃ­as. Se priorizarÃ¡ la verificaciÃ³n del comportamiento de la interfaz al exponer u ocultar informaciÃ³n segÃºn la visibilidad del equipo, asÃ­ como la correcta gestiÃ³n transaccional de las solicitudes de ingreso desde que se emiten hasta que son resueltas por un administrador.

### 2.2. TÃ©cnicas de Caja Negra Utilizadas

Para garantizar una cobertura exhaustiva de las polÃ­ticas de acceso y los flujos de membresÃ­a, se aplicarÃ¡n las siguientes metodologÃ­as de diseÃ±o:

*   **ParticiÃ³n de Equivalencia (Equivalence Partitioning):** TÃ©cnica fundamental para este mÃ³dulo, utilizada para reducir el infinito nÃºmero de interacciones de usuarios a clases representativas basadas en sus roles (por ejemplo, Admin, Org Manager, Team Manager, Mapper, AnÃ³nimo). TambiÃ©n se aplicarÃ¡ para agrupar los atributos de configuraciÃ³n de los equipos (Visibilidad PÃºblica vs. Privada).
*   **Tablas de DecisiÃ³n (Decision Table Testing):** Se utilizarÃ¡ para modelar la lÃ³gica de negocio detrÃ¡s de la acciÃ³n de "Unirse a un Equipo". La interfaz debe reaccionar de manera diferente combinando mÃºltiples entradas: el mÃ©todo de ingreso del equipo (`ANY`, `BY_REQUEST`, `BY_INVITE`), el rol del usuario y su estado de membresÃ­a actual.
*   **TransiciÃ³n de Estados (State Transition Testing):** Aplicada especÃ­ficamente para auditar el flujo de trabajo (workflow) de las solicitudes de membresÃ­a de los usuarios. ValidarÃ¡ que los cambios de estado del actor dentro de un equipo (de `None` a `Pending`, y de `Pending` a `Active` o `Rejected`) sigan estrictamente las transiciones permitidas por la plataforma mediante la intervenciÃ³n de un administrador autorizado.

## 3. Especificaciones de Escenarios y Casos de Prueba

Para asegurar una cobertura funcional completa del mÃ³dulo sin generar redundancia en los casos de prueba, se proponen **3 Especificaciones de Escenarios de Prueba (ESC)**.

**JustificaciÃ³n de la cantidad y agrupaciÃ³n:**
El mÃ³dulo 6 se encarga de la gestiÃ³n de acceso jerÃ¡rquico. La administraciÃ³n de equipos y organizaciones puede dividirse lÃ³gicamente en tres flujos transaccionales con diferentes niveles de intervenciÃ³n de actores y reglas de negocio:

1.  **CreaciÃ³n de Estructuras (ESC-6001):** EvalÃºa los permisos fundamentales. Un usuario debe tener un rol elevado (`ADMIN`, `ORG MANAGER`) para instanciar equipos. (Ya desarrollado).
2.  **Solicitudes y Ciclo de Vida de MembresÃ­a (ESC-6002):** Cubre el flujo de interacciÃ³n entre usuarios base (solicitantes) y administradores (aprobadores), dependiendo altamente de las configuraciones de visibilidad y mÃ©todos de ingreso del equipo. Es ideal para analizar mediante TransiciÃ³n de Estados.
3.  **Privilegios y Permisos Heredados en Proyectos (ESC-6003):** Verifica que las membresÃ­as otorgadas en los flujos anteriores efectivamente habiliten o restrinjan el acceso de un usuario a Mapear o Validar en un proyecto especÃ­fico. Requiere evaluar mÃºltiples reglas de negocio (Tabla de DecisiÃ³n).

| ID Escenario | DescripciÃ³n Breve | RF Cubiertos | Alcance Funcional | TÃ©cnica Principal |
| :--- | :--- | :--- | :--- | :--- |
| **ESC-6001** | CreaciÃ³n y ConfiguraciÃ³n Inicial de Equipos | RF-6001 | ValidaciÃ³n de RBAC en la creaciÃ³n y configuraciÃ³n de variables principales (Visibilidad, MÃ©todo de Ingreso). | ParticiÃ³n de Equivalencia |
| **ESC-6002** | Solicitud y AprobaciÃ³n de MembresÃ­as | RF-6002, RF-6003 | Flujo completo de un usuario solicitando unirse a un equipo y el proceso de aprobaciÃ³n/rechazo por parte del Manager. | TransiciÃ³n de Estados |
| **ESC-6003** | ResoluciÃ³n de Permisos en Proyectos | RF-6003 | Impacto de la membresÃ­a: ValidaciÃ³n de que pertenecer a un equipo (o la suma de roles) otorga los permisos correctos sobre un proyecto. | Tabla de DecisiÃ³n |

---

### 3.1. Escenario: [ESC-6001] - CreaciÃ³n y ConfiguraciÃ³n Inicial de Equipos

**A. DefiniciÃ³n del Escenario**

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el sistema permite la creaciÃ³n y configuraciÃ³n inicial de un Equipo (asignando su OrganizaciÃ³n padre, nivel de visibilidad y mÃ©todo de ingreso) exclusivamente a usuarios con privilegios administrativos, restringiendo el acceso y la habilitaciÃ³n de los controles de interfaz a usuarios sin autorizaciÃ³n. |
| **RF Asociados** | RF-6001 |
| **Precondiciones** | OrganizaciÃ³n matriz previamente creada en el sistema. |
| **TÃ©cnicas aplicadas**| ParticiÃ³n de Equivalencia (PE). |
| **Resultado Esperado** | El sistema procesa la creaciÃ³n del equipo, lo asocia a la organizaciÃ³n correspondiente y redirige al usuario a la vista de gestiÃ³n del equipo (`/manage/teams/{id}`). Las solicitudes sin privilegios o con datos incompletos son bloqueadas a nivel de interfaz o rechazadas por la API. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**

**B.1. ParticiÃ³n de Equivalencia (PE)**
La creaciÃ³n de equipos estÃ¡ gobernada por estrictas reglas de Control de Acceso (RBAC) y validaciÃ³n de formularios. Se aplica la ParticiÃ³n de Equivalencia para agrupar los tipos de usuarios que interactÃºan con el sistema y los estados del formulario de creaciÃ³n, reduciendo la cantidad de pruebas necesarias y cubriendo todas las fronteras de validaciÃ³n.

| Cod. | Campo / CondiciÃ³n Analizada | Clase VÃ¡lida | Clases No VÃ¡lidas |
| :--- | :--- | :--- | :--- |
| **MOD06-PE-001** | Privilegios del Usuario (Control de Acceso) | 1. Administrador Global (`ADMIN`).<br>2. Gestor de la OrganizaciÃ³n (`ORG MANAGER`). | 1. Usuario estÃ¡ndar (`MAPPER`).<br>2. Usuario no autenticado (AnÃ³nimo). |
| **MOD06-PE-002** | Entrada: Nombre del Equipo | Cadena de texto alfanumÃ©rica (> 0 caracteres). | Cadena de texto vacÃ­a. |
| **MOD06-PE-003** | ConfiguraciÃ³n: Visibilidad (`visibility`) | `PUBLIC`, `PRIVATE`. | Valores nulos o alterados en la peticiÃ³n (por ejemplo, `HIDDEN`). |
| **MOD06-PE-004** | ConfiguraciÃ³n: MÃ©todo de ingreso (`joinMethod`) | `ANY`, `BY_REQUEST`, `BY_INVITE`. | Valores nulos o no soportados. |

*   *Comportamiento esperado (MOD06-PE-001 - Clase VÃ¡lida):* El botÃ³n de "Nuevo Equipo" es visible en la interfaz de gestiÃ³n y la peticiÃ³n `POST` al endpoint retorna `HTTP 201 Created`.
*   *Comportamiento esperado (MOD06-PE-001 - Clases No VÃ¡lidas):* La interfaz oculta el botÃ³n de creaciÃ³n. Si se fuerza la peticiÃ³n vÃ­a API, el sistema retorna `HTTP 403` indicando `CreateTeamNotPermitted`.
*   *Comportamiento esperado (MOD06-PE-002 - Clases No VÃ¡lidas):* La interfaz mantiene deshabilitado el botÃ³n "Crear Equipo" hasta que el campo contenga un valor.

**C. Casos de Prueba Derivados**

| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada / Contexto | Resultado Esperado | TÃ©cnicas / Etiquetas Aplicadas |
| :--- | :--- | :--- | :--- | :--- |
| **CP-6001-01** | 1. Autenticar y navegar a "Crear Equipo".<br>2. Completar formulario.<br>3. Enviar. | **Rol:** `ADMIN`<br>**Nombre:** "Alpha Team"<br>**Visibilidad:** `PUBLIC`<br>**Ingreso:** `ANY` | CreaciÃ³n exitosa (`HTTP 201`). El sistema muestra notificaciÃ³n (Toast) de Ã©xito y redirige a la vista del detalle del equipo. | PE-001 (VÃ¡lido)<br>PE-002 (VÃ¡lido)<br>PE-003 (VÃ¡lido) |
| **CP-6001-02** | 1. Autenticar y navegar a "Crear Equipo".<br>2. Completar formulario.<br>3. Enviar. | **Rol:** `ORG MANAGER`<br>**Nombre:** "Bravo Team"<br>**Visibilidad:** `PRIVATE`<br>**Ingreso:** `BY_REQUEST` | CreaciÃ³n exitosa (`HTTP 201`). El usuario queda automÃ¡ticamente registrado como Manager del equipo creado. | PE-001 (VÃ¡lido)<br>PE-003 (VÃ¡lido)<br>PE-004 (VÃ¡lido) |
| **CP-6001-03** | 1. Autenticar y navegar a "Crear Equipo".<br>2. Dejar el campo nombre vacÃ­o.<br>3. Intentar enviar. | **Rol:** `ADMIN`<br>**Nombre:** `""` (VacÃ­o)<br>**Visibilidad:** `PUBLIC` | El botÃ³n de "Crear Equipo" (`Create Team`) permanece deshabilitado (Disabled). No se envÃ­a peticiÃ³n de red. | PE-002 (No VÃ¡lida) |
| **CP-6001-04** | 1. Autenticar como usuario base.<br>2. Acceder al dashboard de equipos.<br>3. Buscar botÃ³n de creaciÃ³n. | **Rol:** `MAPPER` | La UI no muestra el botÃ³n "New". | PE-001 (No VÃ¡lida) |
| **CP-6001-05** | 1. Cargar la URL de creaciÃ³n de equipos de forma directa. | **Rol:** AnÃ³nimo (Sin token) | El sistema redirige al usuario a la pantalla de inicio de sesiÃ³n (`/login`) o retorna `HTTP 401`. | PE-001 (No VÃ¡lida) |

### 3.2. Escenario: [ESC-6002] - Solicitud y AprobaciÃ³n de MembresÃ­as de Equipo

**A. DefiniciÃ³n del Escenario**

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar el flujo de trabajo (workflow) completo mediante el cual un usuario base solicita unirse a un equipo configurado como `BY_REQUEST`, y el posterior proceso de resoluciÃ³n (aceptaciÃ³n o denegaciÃ³n) por parte de un administrador de dicho equipo, verificando la correcta asignaciÃ³n de roles. |
| **RF Asociados** | RF-6002, RF-6003 |
| **Precondiciones** | Equipo existente configurado con `joinMethod = BY_REQUEST`. Usuario solicitante autenticado. |
| **TÃ©cnicas aplicadas**| TransiciÃ³n de Estados (State Transition Testing). |
| **Resultado Esperado** | El sistema procesa secuencialmente la solicitud, generando notificaciones asÃ­ncronas y cambiando el estado de vinculaciÃ³n del usuario con el equipo hasta reflejar la membresÃ­a activa (`MEMBER`) tras la aprobaciÃ³n. Las transiciones no autorizadas o fuera de secuencia son denegadas. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**

**B.1. TransiciÃ³n de Estados**
La membresÃ­a de un usuario en un equipo sigue un ciclo de vida definido. Se modelan los estados del usuario con respecto a la membresÃ­a del equipo y las acciones que provocan las transiciones.

![Diagrama de transiciones ESC-6002](/tests-docs/02-diseno-de-pruebas/funcionales/img/transicion-estado-ESC-6002.png) 

**Tabla de TransiciÃ³n de Estados**

| Estado Inicial (MembresÃ­a) | AcciÃ³n (Evento en Interfaz / API) | Actor | Estado Final Esperado | TransiciÃ³n | ObservaciÃ³n |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `NONE` | Clic en botÃ³n "Join Team" | `MAPPER` | `PENDING` | VÃ¡lida | Solicitud en espera. Se genera notificaciÃ³n al Manager. |
| `PENDING` | Clic en "Accept" | `TEAM MANAGER` | `ACTIVE_MEMBER` | VÃ¡lida | El usuario obtiene rol de `MEMBER` activo. |
| `PENDING` | Clic en "Deny" | `TEAM MANAGER` | `NONE` | VÃ¡lida | Solicitud rechazada. El usuario no ingresa al equipo. |
| `ACTIVE_MEMBER` | Clic en "Leave Team" | `MEMBER` | `NONE` | VÃ¡lida | Salida voluntaria del equipo. |
| `ACTIVE_MEMBER` | Clic en "Remove" | `TEAM MANAGER` | `NONE` | VÃ¡lida | ExpulsiÃ³n forzada por el administrador. |
| `PENDING` | Clic en "Accept" | `MAPPER` (Solicitante) | - | InvÃ¡lida | Un usuario no puede auto-aprobar su solicitud (Error 403). |
| `ACTIVE_MEMBER`| Clic en "Join Team" | `MEMBER` | - | InvÃ¡lida | Un miembro activo no puede solicitar ingreso nuevamente (Error). |

**C. Casos de Prueba Derivados**

| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada / Contexto | Resultado Esperado | TÃ©cnicas / Etiquetas Aplicadas |
| :--- | :--- | :--- | :--- | :--- |
| **CP-6002-01** | 1. Usuario A visita pÃ¡gina de Equipo (`BY_REQUEST`).<br>2. Clic en "Join Team". | **Estado:** `NONE`<br>**Actor:** `MAPPER` | El sistema muestra mensaje "Join request successful". El estado cambia a `PENDING`. Se envÃ­a notificaciÃ³n interna al Manager del equipo. | TransiciÃ³n de Estados (VÃ¡lida) |
| **CP-6002-02** | 1. Manager revisa lista de solicitudes.<br>2. Selecciona Usuario A y hace clic en "Accept". | **Estado:** `PENDING`<br>**Actor:** `TEAM MANAGER` | El sistema retorna "True/Success". El usuario A pasa a estado `ACTIVE_MEMBER` y se visualiza en la pestaÃ±a "Team Members". | TransiciÃ³n de Estados (VÃ¡lida) |
| **CP-6002-03** | 1. Manager revisa lista de solicitudes.<br>2. Selecciona Usuario B y hace clic en "Deny". | **Estado:** `PENDING`<br>**Actor:** `TEAM MANAGER` | El sistema elimina la solicitud. El estado del Usuario B vuelve a `NONE` (no se agrega a la lista de miembros). | TransiciÃ³n de Estados (VÃ¡lida) |
| **CP-6002-04** | 1. Miembro Activo navega al detalle del equipo.<br>2. Clic en "Leave Team" y confirmaciÃ³n. | **Estado:** `ACTIVE_MEMBER`<br>**Actor:** `MEMBER` | El sistema retorna "User removed from the team". El estado vuelve a `NONE`. | TransiciÃ³n de Estados (VÃ¡lida) |
| **CP-6002-05** | 1. Usuario C solicita unirse (`PENDING`).<br>2. Usuario C manipula peticiÃ³n API intentando forzar "Accept". | **Estado:** `PENDING`<br>**Actor:** `MAPPER` (Solicitante) | TransiciÃ³n denegada. El sistema retorna `HTTP 403: You don't have permissions to approve this join team request`. | TransiciÃ³n de Estados (InvÃ¡lida) |


### 3.3. Escenario: [ESC-6003] - ResoluciÃ³n de Permisos y Privilegios en Proyectos

**A. DefiniciÃ³n del Escenario**

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el motor de autorizaciÃ³n del sistema evalÃºa correctamente la combinaciÃ³n de las membresÃ­as de equipo del usuario, los roles asignados a dichos equipos dentro del proyecto, y el nivel de experiencia del usuario, para otorgar o denegar permisos de ejecuciÃ³n (Mapeo o ValidaciÃ³n) sobre las tareas de un proyecto restringido. |
| **RF Asociados** | RF-6003 |
| **Precondiciones** | Proyecto en estado `PUBLISHED`. Permisos del proyecto configurados restrictivamente (ej. `mappingPermission = TEAMS_LEVEL`). Equipos asociados al proyecto con roles definidos (`MAPPER`, `VALIDATOR`). Usuario (ACT-0002) autenticado. |
| **TÃ©cnicas aplicadas**| Tablas de DecisiÃ³n (Decision Table Testing). |
| **Resultado Esperado** | El sistema procesa la matriz de condiciones del usuario contra la configuraciÃ³n del proyecto y habilita los controles de "Mapear Tarea" o "Validar Tarea", o muestra el mensaje de error correspondiente a la validaciÃ³n que fallÃ³. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**

**B.1. Tablas de DecisiÃ³n**
Para determinar si un usuario puede accionar sobre una tarea, el sistema evalÃºa simultÃ¡neamente el mÃ©todo de restricciÃ³n del proyecto, la membresÃ­a, el rol del equipo y el nivel del usuario. Se diseÃ±a una tabla para la restricciÃ³n mÃ¡s estricta: `TEAMS_LEVEL` (Requiere pertenecer a un equipo autorizado Y poseer un nivel mÃ­nimo). Se utilizan guiones (`-`) para condiciones que resultan indiferentes tras una falla primaria.

| Condiciones de entrada | | | | | |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Permiso del proyecto configurado como `TEAMS_LEVEL` | V | V | V | V | V |
| El usuario pertenece a un Equipo asignado al proyecto | V | V | V | F | V |
| El rol del equipo asignado permite la acciÃ³n solicitada (ej. `MAPPER`) | V | F | V | - | F |
| El nivel del usuario (`BEGINNER`, `ADVANCED`) cumple el mÃ­nimo exigido | V | V | F | - | F |
| **Condiciones de salida** | | | | | |
| Permitir AcciÃ³n (Habilitar botones de Mapeo/ValidaciÃ³n) | V | F | F | F | F |
| Error: No pertenece a un equipo con el rol necesario (`UserIsNotMappingTeamMember`) | F | V | F | V | V |
| Error: Nivel insuficiente (`UserLevelToMap` / `UserLevelToValidate`) | F | F | V | F | F |
| **Etiqueta** | **A** | **B** | **C** | **D** | **E** |

*(Nota: La Etiqueta A representa el "Happy Path" de autorizaciÃ³n combinada).*

**C. Casos de Prueba Derivados**

| ID Caso | Datos de entrada o escenario | Resultado Esperado | TÃ©cnicas / Etiquetas Aplicadas |
| :--- | :--- | :--- | :--- |
| **CP-6003-01** | Proyecto requiere `TEAMS_LEVEL` (`ADVANCED`).<br>Usuario Nivel: `ADVANCED`.<br>Equipo: Asignado al proyecto con rol `MAPPER`.<br>Usuario: Miembro Activo. | El usuario visualiza y puede utilizar el botÃ³n "Map a Task" o seleccionar una tarea para mapeo. AutorizaciÃ³n exitosa. | Tabla de DecisiÃ³n (A) |
| **CP-6003-02** | Proyecto requiere `TEAMS_LEVEL` (`ADVANCED`).<br>Usuario Nivel: `ADVANCED`.<br>Equipo: Asignado al proyecto con rol `VALIDATOR`.<br>AcciÃ³n solicitada: Mapear. | AcciÃ³n de mapeo denegada. El sistema muestra la advertencia: `User is not a mapping team member`. | Tabla de DecisiÃ³n (B) |
| **CP-6003-03** | Proyecto requiere `TEAMS_LEVEL` (`ADVANCED`).<br>Usuario Nivel: `BEGINNER`.<br>Equipo: Asignado al proyecto con rol `MAPPER`.<br>Usuario: Miembro Activo. | AcciÃ³n denegada. El sistema muestra la advertencia indicando que no se posee el nivel requerido (`userLevelToMap`). | Tabla de DecisiÃ³n (C) |
| **CP-6003-04** | Proyecto requiere `TEAMS_LEVEL` (`ADVANCED`).<br>Usuario Nivel: `ADVANCED`.<br>Usuario: No pertenece a ningÃºn equipo. | AcciÃ³n denegada por no ser miembro de un equipo autorizado, mostrando la advertencia: `User is not a mapping team member`. | Tabla de DecisiÃ³n (D) |

---

## 4. Matriz de Trazabilidad del MÃ³dulo

Esta matriz consolida la relaciÃ³n bidireccional entre los Requerimientos Funcionales (RF) documentados y los artefactos de diseÃ±o generados para el mÃ³dulo **MOD-06: Gobernanza (Organizaciones y Equipos)**.

Garantiza la cobertura total de las reglas de negocio y facilita el anÃ¡lisis de impacto ante futuros cambios en los flujos de membresÃ­a o el Control de Acceso (RBAC).

| Requerimiento Funcional (RF) | EspecificaciÃ³n de Escenario (ESC) | Casos de Prueba (CP) Derivados | TÃ©cnicas de DiseÃ±o Aplicadas |
| :--- | :--- | :--- | :--- |
| **RF-6001** | **ESC-6001:** CreaciÃ³n y ConfiguraciÃ³n Inicial de Equipos | **CP-6001-01**, **CP-6001-02** | ParticiÃ³n de Equivalencia (Clases VÃ¡lidas) |
| **RF-6001** | ESC-6001 | **CP-6001-03**, **CP-6001-04**, **CP-6001-05** | ParticiÃ³n de Equivalencia (Clases No VÃ¡lidas) |
| **RF-6002, RF-6003** | **ESC-6002:** Solicitud y AprobaciÃ³n de MembresÃ­as de Equipo | **CP-6002-01**, **CP-6002-02**, **CP-6002-03**, **CP-6002-04** | TransiciÃ³n de Estados (VÃ¡lidas) |
| **RF-6002** | ESC-6002 | **CP-6002-05** | TransiciÃ³n de Estados (InvÃ¡lidas) |
| **RF-6003** | **ESC-6003:** ResoluciÃ³n de Permisos y Privilegios en Proyectos | **CP-6003-01** | Tabla de DecisiÃ³n (Happy Path / CombinaciÃ³n A) |
| **RF-6003** | ESC-6003 | **CP-6003-02**, **CP-6003-03**, **CP-6003-04** | Tabla de DecisiÃ³n (Restricciones / Combinaciones B, C, D) |

