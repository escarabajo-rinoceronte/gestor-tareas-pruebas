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
  <b>Proyecto:</b> HOT Tasking Manager — Diseño de Pruebas de Aceptación (MOD-01 a MOD-03) <br>
  <b>Fecha de Elaboración:</b> 20/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Diseño de Pruebas de Aceptación

## 1. Contexto

La presente suite de aceptación se construye exclusivamente sobre los tres módulos analizados en el proyecto:

- `MOD-01` Autenticación y Perfil
- `MOD-02` Exploración de Proyectos
- `MOD-03` Ejecución de Mapeo

### 3.1. MOD-01 — Autenticación y Perfil

| ID | RF | Ruta principal | Caso funcional base | Descripción | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CA-ACP-01** | `RF-1001` | `/login` -> `/authorized` | `CP-1001-01` | El usuario puede iniciar sesión mediante OAuth con OpenStreetMap e ingresar a la plataforma. | El usuario accede correctamente a la plataforma y visualiza su sesión activa. |
| **CA-ACP-02** | `RF-1001` | `/login` | `CP-1001-02` | Si el usuario cancela o niega la autorización con OpenStreetMap, el acceso no se completa. | El usuario permanece fuera de la plataforma y no se crea una sesión local. |
| **CA-ACP-03** | `RF-1001` | Barra superior / perfil | `CP-1001-03` | El usuario puede cerrar su sesión desde la opción `Log Out`. | El usuario regresa a la vista pública después de cerrar sesión. |
| **CA-ACP-04** | `RF-1003` | `/projects/:id` | `CP-1003-01` | Un usuario no autenticado no puede acceder a un proyecto restringido sin iniciar sesión. | El usuario es redirigido a autenticación antes de acceder al proyecto restringido. |
| **CA-ACP-05** | `RF-1003` | `/projects/:id/tasks` | `CP-1003-03`, `CP-1003-04` | En un proyecto con licencia obligatoria, el usuario no puede comenzar a mapear hasta aceptar los términos. | Antes de aceptar, el usuario no puede contribuir; después de aceptar, la contribución queda habilitada. |
| **CA-ACP-06** | `RF-1004` | `/settings` | `CP-1004-01`, `CP-1004-02`, `CP-1004-03` | El usuario puede actualizar su perfil cuando los datos son válidos y no puede guardar información inválida. | El usuario guarda correctamente los datos válidos y recibe validación ante entradas inválidas. |

### 3.2. MOD-02 — Exploración de Proyectos

| ID | RF | Ruta principal | Caso funcional base | Descripción | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CA-ACP-07** | `RF-2001` | `/explore` | `CP-2001-01` | El usuario puede visualizar el catálogo general de proyectos al ingresar a la sección de exploración. | El usuario visualiza correctamente el catálogo base de proyectos. |
| **CA-ACP-08** | `RF-2001` | `/explore` | `CP-2001-02` | El usuario puede filtrar proyectos activos y visualizar únicamente los que cumplen esa condición. | El usuario visualiza solo proyectos en estado `Activo`. |
| **CA-ACP-09** | `RF-2001` | `/explore` | `CP-2001-04` | El usuario puede combinar filtros y obtener resultados coherentes, incluso cuando no existen coincidencias. | El usuario obtiene resultados acordes con la combinación aplicada o una vista vacía controlada. |
| **CA-ACP-10** | `RF-2002` | `/explore` | `CP-2002-02`, `CP-2002-04`, `CP-2002-06` | El usuario puede buscar proyectos y el sistema responde de forma controlada ante entradas no válidas. | El usuario obtiene resultados para búsquedas válidas y mensajes controlados ante entradas inválidas. |
| **CA-ACP-11** | `RF-2003` | `/explore`, `/projects/:id` | `CP-2003-01`, `CP-2003-02`, `CP-2003-04` | Un usuario sin autorización no puede visualizar proyectos privados, mientras que un usuario autorizado sí puede acceder a ellos. | El proyecto privado permanece oculto para quien no tiene permiso y visible para quien sí lo posee. |

### 3.3. MOD-03 — Ejecución de Mapeo

| ID | RF | Ruta principal | Caso funcional base | Descripción | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CA-ACP-12** | `RF-3001`, `RF-3002` | `/projects/:id/tasks` -> `/projects/:id/map?editor=ID` | `CP-3001-01` | El usuario puede seleccionar una tarea disponible e iniciar su edición en el editor web correspondiente. | El usuario puede iniciar el mapeo de una tarea disponible y acceder al editor `iD`. |
| **CA-ACP-13** | `RF-3003` | `/projects/:id/map?editor=JOSM` | `CP-3001-02` | Si el editor local `JOSM` no está disponible, el usuario es informado del problema sin perder el contexto de trabajo. | El usuario recibe una notificación sobre la indisponibilidad de `JOSM` y conserva el flujo iniciado. |
| **CA-ACP-14** | `RF-1003`, `RF-3001` | `/projects/:id/tasks` -> `/projects/:id/map` | `CP-3001-03` | El usuario no puede iniciar el mapeo de una tarea mientras no haya aceptado la licencia requerida por el proyecto. | El usuario no puede iniciar el mapeo hasta aceptar la licencia correspondiente. |
| **CA-ACP-15** | `RF-3001` | `/projects/:id/tasks` | `CP-3001-04`, `CP-3001-05`, `CP-3001-06` | El usuario no puede bloquear tareas cuando no cumple las condiciones necesarias, como permisos, estado válido o ausencia de bloqueos previos. | El usuario no puede bloquear la tarea cuando no cumple las reglas de negocio definidas. |
| **CA-ACP-16** | `RF-3004` | `/projects/:id/map` | `CP-3002-01` | El usuario puede finalizar una tarea de mapeo y dejarla registrada como completada. | La tarea queda registrada como completada después de que el usuario la finaliza. |
| **CA-ACP-17** | `RF-3004` | `/projects/:id/map` | `CP-3002-02` | El usuario puede liberar una tarea sin completarla, dejándola nuevamente disponible para su atención posterior. | La tarea vuelve a estar disponible después de que el usuario la libera sin completarla. |
| **CA-ACP-18** | `RF-3004` | `/projects/:id/tasks` | `CP-3002-03`, `CP-3002-04`, `CP-3002-05` | El usuario no visualiza la opción `Submit Task` cuando no se encuentra en un contexto válido para finalizar una tarea. | El usuario no visualiza controles de envío cuando no puede finalizar la tarea. |
| **CA-ACP-19** | `RF-3005` | `/projects/:id/tasks`, `/projects/:id/map` | `CP-3003-01`, `CP-3003-03`, `CP-3003-04` | El usuario solo puede dividir una tarea cuando se encuentra en una condición válida para hacerlo. | La opción de dividir tarea solo está disponible cuando el contexto lo permite. |
| **CA-ACP-20** | `RF-3006` | `/projects/:id/map` | `CP-3004-02`, `CP-3004-03`, `CP-3004-04`, `CP-3004-05` | El usuario puede extender o liberar su sesión de mapeo según las condiciones permitidas por el sistema. | El usuario puede extender o liberar la sesión solo cuando el contexto correspondiente lo permite. |
