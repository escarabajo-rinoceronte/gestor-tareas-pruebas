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
| **CA-ACP-01** | `RF-1001` | `/login` -> `/authorized` | `CP-1001-01` | Inicio de sesión exitoso mediante OAuth con OpenStreetMap. | El usuario entra a la plataforma y visualiza sesión activa en la interfaz. |
| **CA-ACP-02** | `RF-1001` | `/login` | `CP-1001-02` | Cancelación o denegación del acceso OAuth. | El sistema retorna a estado no autenticado sin crear sesión local. |
| **CA-ACP-03** | `RF-1001` | Barra superior / perfil | `CP-1001-03` | Cierre de sesión desde la opción `Log Out`. | La sesión se destruye y la UI vuelve a la vista pública. |
| **CA-ACP-04** | `RF-1003` | `/projects/:id` | `CP-1003-01` | Acceso a proyecto restrictivo sin haber iniciado sesión. | El sistema bloquea el acceso y redirige a autenticación. |
| **CA-ACP-05** | `RF-1003` | `/projects/:id/tasks` | `CP-1003-03`, `CP-1003-04` | Proyecto con licencia: bloqueo previo y habilitación posterior tras aceptar términos. | Antes de aceptar, la contribución queda bloqueada; tras aceptar, el botón de mapeo se habilita. |
| **CA-ACP-06** | `RF-1004` | `/settings` | `CP-1004-01`, `CP-1004-02`, `CP-1004-03` | Edición de perfil con validación de datos y guardado de cambios. | El sistema bloquea entradas inválidas y guarda correctamente los datos válidos. |

### 3.2. MOD-02 — Exploración de Proyectos

| ID | RF | Ruta principal | Caso funcional base | Descripción | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CA-ACP-07** | `RF-2001` | `/explore` | `CP-2001-01` | Carga inicial del catálogo sin filtros activos. | La pantalla muestra el catálogo base de proyectos. |
| **CA-ACP-08** | `RF-2001` | `/explore` | `CP-2001-02` | Filtrado por estado `Activo`. | Solo se muestran proyectos activos. |
| **CA-ACP-09** | `RF-2001` | `/explore` | `CP-2001-04` | Combinación de filtros por estado, dificultad y campaña. | La UI procesa la intersección correctamente, incluyendo el caso de resultado vacío. |
| **CA-ACP-10** | `RF-2002` | `/explore` | `CP-2002-02`, `CP-2002-04`, `CP-2002-06` | Búsqueda por texto y manejo controlado de entradas o delimitaciones inválidas. | La búsqueda responde a entradas válidas y controla errores sin romper la interfaz. |
| **CA-ACP-11** | `RF-2003` | `/explore`, `/projects/:id` | `CP-2003-01`, `CP-2003-02`, `CP-2003-04` | Protección de proyectos privados para usuario anónimo y acceso permitido a usuario autorizado. | El proyecto privado permanece oculto al no autorizado y visible solo para quien tiene permisos. |

### 3.3. MOD-03 — Ejecución de Mapeo

| ID | RF | Ruta principal | Caso funcional base | Descripción | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CA-ACP-12** | `RF-3001`, `RF-3002` | `/projects/:id/tasks` -> `/projects/:id/map?editor=ID` | `CP-3001-01` | Bloqueo exitoso de tarea `READY` con editor web `iD`. | La tarea pasa a `LOCKED_FOR_MAPPING` y se carga el editor. |
| **CA-ACP-13** | `RF-3003` | `/projects/:id/map?editor=JOSM` | `CP-3001-02` | Selección de `JOSM` cuando el servicio local no está disponible. | El sistema informa el error, pero conserva la integridad del flujo y del bloqueo. |
| **CA-ACP-14** | `RF-1003`, `RF-3001` | `/projects/:id/tasks` -> `/projects/:id/map` | `CP-3001-03` | Restricción de mapeo cuando la licencia no ha sido aceptada. | El sistema no debe permitir iniciar el mapeo hasta aceptar la licencia. |
| **CA-ACP-15** | `RF-3001` | `/projects/:id/tasks` | `CP-3001-04`, `CP-3001-05`, `CP-3001-06` | Restricciones de bloqueo por concurrencia, estado inválido o permisos insuficientes. | El sistema deniega el bloqueo cuando no se cumplen las reglas de negocio. |
| **CA-ACP-16** | `RF-3004` | `/projects/:id/map` | `CP-3002-01` | Finalización de tarea con opción `Yes`. | La tarea pasa a `MAPPED` y se libera el bloqueo. |
| **CA-ACP-17** | `RF-3004` | `/projects/:id/map` | `CP-3002-02` | Liberación de tarea con opción `No`. | La tarea vuelve a `READY`. |
| **CA-ACP-18** | `RF-3004` | `/projects/:id/tasks` | `CP-3002-03`, `CP-3002-04`, `CP-3002-05` | El panel `Submit Task` no debe mostrarse en contextos no válidos. | La UI oculta los controles de envío cuando el usuario no puede finalizar la tarea. |
| **CA-ACP-19** | `RF-3005` | `/projects/:id/tasks`, `/projects/:id/map` | `CP-3003-01`, `CP-3003-03`, `CP-3003-04` | División de tarea solo cuando el usuario posee una tarea válida y bloqueada. | El split solo se habilita en contexto permitido y permanece oculto o denegado en los demás casos. |
| **CA-ACP-20** | `RF-3006` | `/projects/:id/map` | `CP-3004-02`, `CP-3004-03`, `CP-3004-04`, `CP-3004-05` | Gestión del tiempo de sesión: auto-unlock, extensión válida y restricción de `Extend Session` en contextos inválidos. | El sistema libera o extiende la tarea correctamente y protege la acción cuando no corresponde. |

