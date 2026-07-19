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
  <b>Proyecto:</b> HOT Tasking Manager — DocumentaciÃ³n del Modelo de Roles y AutorizaciÃ³n <br>
  <b>Fecha de Elaboración:</b> 15/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# DocumentaciÃ³n del Modelo de Roles y AutorizaciÃ³n

## 1. IntroducciÃ³n
El sistema de permisos de Tasking Manager estÃ¡ diseÃ±ado para permitir la colaboraciÃ³n masiva (Crowdsourcing) mientras se mantiene un control estricto sobre la calidad de los datos y la gestiÃ³n de las organizaciones. La autorizaciÃ³n no es lineal; un usuario puede ser un `MAPPER` a nivel global, pero actuar como `MANAGER` dentro de una organizaciÃ³n especÃ­fica.

---

## 2. Roles Globales
Estos roles se definen directamente en la entidad `User` (columna `role`) y establecen el comportamiento base en todo el sistema.

### A. ADMIN (Administrador Global)
*   **PropÃ³sito:** Control total y mantenimiento del sistema. Es el "Superusuario".
*   **Permisos:**
    *   GestiÃ³n total de todas las Organizaciones, Proyectos y Equipos.
    *   Cambiar roles y niveles de mapeo de cualquier usuario.
    *   Modificar configuraciones globales (Banners, licencias, categorÃ­as de problemas).
    *   Acceso a todas las estadÃ­sticas del sistema.
*   **Restricciones:** Ninguna.
*   **Cambios en Interfaz:** Aparece la pestaÃ±a **Manage** con todas las sub-opciones disponibles (Projects, Organisations, Teams, Users, Campaigns).
*   **Tipo de Usuario:** Personal tÃ©cnico de IT o directores de la plataforma.

### B. MAPPER (Usuario EstÃ¡ndar)
*   **PropÃ³sito:** Rol por defecto para todos los usuarios autenticados. Participar en la contribuciÃ³n de datos.
*   **Permisos:**
    *   Mapear tareas en proyectos pÃºblicos.
    *   Validar tareas (si su nivel de experiencia es suficiente).
    *   Crear y gestionar sus propios equipos (si la configuraciÃ³n lo permite).
*   **Restricciones:** No puede crear proyectos ni organizaciones por sÃ­ mismo (a menos que se le asigne un rol de gestiÃ³n). No ve la pestaÃ±a de administraciÃ³n global.
*   **Cambios en Interfaz:** Vista estÃ¡ndar enfocada en **Explore** y **Learn**. Solo ve la pestaÃ±a **Manage** si es autor de un proyecto o manager de un equipo/organizaciÃ³n.
*   **Tipo de Usuario:** Voluntarios y mapeadores de la comunidad.

### C. READ_ONLY (Usuario Bloqueado)
*   **PropÃ³sito:** Restringir el acceso a usuarios que han violado normas de la comunidad.
*   **Permisos:** Solo lectura. Puede ver proyectos y mapas.
*   **Restricciones:** No puede bloquear tareas, comentar, validar ni realizar ninguna acciÃ³n que modifique la base de datos.
*   **Cambios en Interfaz:** Desaparecen los botones de acciÃ³n ("Map Task", "Post Comment").
*   **Tipo de Usuario:** Cuentas suspendidas.

---

## 3. Roles de GestiÃ³n (Scoped Roles)
Estos roles no dependen del valor global `role`, sino de las relaciones en la base de datos.

### A. Organisation Manager
*   **PropÃ³sito:** Gestionar el portafolio de proyectos de una entidad especÃ­fica (por ejemplo, Cruz Roja, MÃ©dicos Sin Fronteras).
*   **Permisos:**
    *   Crear, editar y borrar proyectos vinculados a **su** organizaciÃ³n.
    *   Gestionar los equipos vinculados a su organizaciÃ³n.
    *   Ver estadÃ­sticas detalladas de su organizaciÃ³n.
*   **Restricciones:** No puede gestionar otras organizaciones ni cambiar configuraciones globales del sistema.
*   **Cambios en Interfaz:** En la pestaÃ±a **Manage**, solo ve los recursos pertenecientes a su organizaciÃ³n.
*   **RelaciÃ³n:** Puede supervisar a los Project Managers de su organizaciÃ³n.

### B. Project Manager / Author
*   **PropÃ³sito:** Responsable de la ejecuciÃ³n de un proyecto de mapeo especÃ­fico.
*   **Permisos:**
    *   Editar la descripciÃ³n, instrucciones y prioridades del proyecto.
    *   Gestionar la lista de usuarios permitidos (si el proyecto es privado).
    *   Invalidar o validar tareas de forma masiva en su proyecto.
*   **Restricciones:** Solo tiene poder sobre los proyectos donde es autor o ha sido asignado.
*   **Cambios en Interfaz:** Aparece la opciÃ³n de "Edit Project" en la vista de detalle del proyecto.

### C. Team Manager
*   **PropÃ³sito:** Administrar la membresÃ­a de un grupo de usuarios.
*   **Permisos:**
    *   Aceptar o rechazar solicitudes de uniÃ³n al equipo.
    *   Invitar nuevos miembros.
    *   Asignar el equipo a proyectos especÃ­ficos (si se le permite).
*   **Restricciones:** No tiene permisos administrativos sobre proyectos u organizaciones a menos que el equipo sea asignado explÃ­citamente a ellos.

---

## 4. Niveles de Experiencia (Mapping Levels)
Aunque no son "roles" de gestiÃ³n, actÃºan como un sistema de **AutorizaciÃ³n Basada en Atributos (ABAC)**.

| Nivel | Valor | Capacidades de AutorizaciÃ³n |
| :--- | :---: | :--- |
| **Beginner** | 1 | Solo puede mapear. No puede validar tareas. |
| **Intermediate** | 2 | Puede validar tareas en proyectos que lo permitan. |
| **Advanced** | 3 | Puede validar tareas en cualquier proyecto y suele ser requerido para proyectos desafiantes. |

---

## 5. Mecanismo de AsignaciÃ³n y Control

### Â¿QuiÃ©n puede asignar roles?
1.  **ADMIN:** Puede asignar cualquier rol global, nivel de mapeo o manager de organizaciÃ³n.
2.  **Organisation Manager:** Puede asignar a otros usuarios como managers de **su** organizaciÃ³n o managers de equipos bajo su mando.
3.  **Team Manager:** Puede aÃ±adir miembros a su equipo.

### Flujo de AsignaciÃ³n
*   **Interfaz vs Interno:** 
    *   El **Rol Global** (`role`) solo puede ser cambiado por un `ADMIN` desde `Manage -> Users`.
    *   El **Nivel de Mapeo** se actualiza automÃ¡ticamente por el sistema basado en el nÃºmero de cambios en OSM (vÃ­a `cron_jobs.py`), pero un `ADMIN` puede forzarlo manualmente desde la interfaz.
    *   Los **Managers de OrganizaciÃ³n** se asignan en la vista de creaciÃ³n/ediciÃ³n de la OrganizaciÃ³n.
*   **Validaciones CrÃ­ticas:**
    *   El sistema no permite que un usuario se asigne a sÃ­ mismo como `ADMIN`.
    *   Para que un usuario actÃºe como `Organisation Manager`, debe existir una entrada en la tabla `organisation_managers`.
    *   Para operaciones de API, el backend utiliza el servicio `ProjectAdminService.is_user_action_permitted_on_project`, que verifica secuencialmente: Â¿Es Admin? luego Â¿Es Autor? luego Â¿Es Org Manager? luego Â¿Es Team Manager del proyecto?

---

## 6. Componentes TÃ©cnicos Intervinientes

*   **Base de Datos:**
    *   Tabla `users`: Columnas `role` y `mapping_level`.
    *   Tabla `organisation_managers`: RelaciÃ³n N:N entre usuarios y organizaciones.
    *   Tabla `team_members`: Columna `function` (1=Manager, 2=Member).
    *   Tabla `project_teams`: Determina quÃ© rol tiene un equipo en un proyecto (`MAPPER`, `VALIDATOR`, `PROJECT_MANAGER`).
*   **Backend (Python):**
    *   `models/postgis/statuses.py`: Define los Enums de roles.
    *   `services/users/authentication_service.py`: Contiene los decoradores `@login_required` y `@admin_only`.
    *   `services/project_admin_service.py`: Centraliza la lÃ³gica de permisos para determinar quiÃ©n puede editar quÃ©.
*   **Frontend (React):**
    *   Utiliza el componente `Permissions` y hooks para renderizar condicionalmente elementos de la UI basÃ¡ndose en el objeto `user` obtenido tras el login.


