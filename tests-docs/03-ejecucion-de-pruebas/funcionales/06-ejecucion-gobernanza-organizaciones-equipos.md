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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — EjecuciÃ³n de casos de pruebas del MOD-06: Gobernanza (Organizaciones y Equipos)</td></tr>
      <tr><td class="label">Fecha</td><td>23/06/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# EjecuciÃ³n de casos de pruebas del MOD-06: Gobernanza (Organizaciones y Equipos)

## 1. ESC-6001 CreaciÃ³n y ConfiguraciÃ³n Inicial de Equipos

### 1.1. EjecuciÃ³n de CP-6001-01

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-6001-01** | Validar la creaciÃ³n exitosa de un equipo con visibilidad `PUBLIC` y mÃ©todo de ingreso `ANY` por parte de un usuario con rol de Administrador Global (`ADMIN`). | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema procesa la solicitud retornando `HTTP 201`. Se muestra una notificaciÃ³n (Toast) de Ã©xito en la interfaz y se redirige automÃ¡ticamente a la vista de detalle del nuevo equipo. | La API respondiÃ³ con cÃ³digo `201 Created`. La UI renderizÃ³ el mensaje "Team created successfully" y navegÃ³ correctamente a la ruta `/manage/teams/{id}` mostrando la informaciÃ³n del equipo "Alpha Team". |

| Evidencia |
| :-- |
| NotificaciÃ³n de Ã©xito y redirecciÃ³n<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-06-gobernanza-organizaciones-equipos/CP-6001-01-toast-success.png" width="800px" alt="CP-6001-01 - Toast de creaciÃ³n exitosa de equipo"></a><br>Captura de la pantalla confirmando la creaciÃ³n y visualizaciÃ³n del detalle del equipo. |

---

### 1.2. EjecuciÃ³n de CP-6001-02

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-6001-02** | Validar la creaciÃ³n de un equipo `PRIVATE` con mÃ©todo de ingreso `BY_REQUEST` por un `ORG MANAGER`, asegurando que el creador herede automÃ¡ticamente el rol de Manager del equipo. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| CreaciÃ³n exitosa (`HTTP 201`). El usuario creador ("Bravo Team") se registra automÃ¡ticamente en la base de datos y en la interfaz como Manager (administrador) del equipo creado. | El equipo privado fue instanciado correctamente en la organizaciÃ³n asignada. Al revisar la pestaÃ±a "Team members", el creador aparece listado con el rol de `MANAGER`. |

| Evidencia |
| :-- |
| AsignaciÃ³n automÃ¡tica de rol Manager<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-06-gobernanza-organizaciones-equipos/CP-6001-02-team-manager-role.png" width="800px" alt="CP-6001-02 - Creador listado como Manager del equipo"></a><br>VisualizaciÃ³n de la tabla de miembros donde el Gestor de OrganizaciÃ³n figura como administrador del equipo. |

---

### 1.3. EjecuciÃ³n de CP-6001-03

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-6001-03** | Validar que la interfaz de usuario restringe la creaciÃ³n de un equipo (deshabilitando el botÃ³n de envÃ­o) si el campo de nombre del equipo se encuentra vacÃ­o. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El botÃ³n de "Crear Equipo" (`Create Team`) permanece en estado deshabilitado (Disabled). El frontend no dispara ninguna peticiÃ³n de red hacia el backend. | Al ingresar al formulario y dejar el campo de nombre vacÃ­o (o al borrar su contenido), el botÃ³n "Create Team" mantiene el atributo `disabled`. No se generaron peticiones en la pestaÃ±a Network del navegador. |

| Evidencia |
| :-- |
| ValidaciÃ³n de formulario en UI<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-06-gobernanza-organizaciones-equipos/CP-6001-03-boton-disabled.png" width="800px" alt="CP-6001-03 - BotÃ³n de creaciÃ³n deshabilitado por campo vacÃ­o"></a><br>Captura del formulario mostrando el campo de nombre vacÃ­o y el botÃ³n de acciÃ³n inactivado. |

---

### 1.4. EjecuciÃ³n de CP-6001-04

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-6001-04** | Validar que un usuario sin privilegios administrativos (rol `MAPPER` base) no puede crear equipos, confirmando la ausencia del botÃ³n en UI. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La interfaz de equipo no renderiza la opciÃ³n de "Gestionar". | Al acceder al dashboard del equipo, el botÃ³n "Gestionar" no existe. |

| Evidencia |
| :-- |
| Ausencia de botÃ³n de creaciÃ³n en UI<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-06-gobernanza-organizaciones-equipos/CP-6001-04-ui-sin-boton.png" width="800px" alt="CP-6001-04 - UI de equipos para usuario Mapper"></a><br>Dashboard de equipos visualizado por usuario base, sin controles administrativos. |

---

### 1.5. EjecuciÃ³n de CP-6001-05

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-6001-05** | Validar el rechazo de acceso al flujo de creaciÃ³n de equipos cuando se fuerza la navegaciÃ³n mediante URL directa por parte de un usuario no autenticado (AnÃ³nimo). | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema intercepta la navegaciÃ³n hacia la vista protegida (`/manage/teams/new`) y redirige al visitante a la pantalla de inicio de sesiÃ³n (`/login`), protegiendo el formulario. | Al ingresar la URL absoluta en una sesiÃ³n de incÃ³gnito, el middleware de enrutamiento del frontend detectÃ³ la falta de token y ejecutÃ³ una redirecciÃ³n limpia hacia `/login`. |

| Evidencia |
| :-- |
| RedirecciÃ³n por falta de sesiÃ³n<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-06-gobernanza-organizaciones-equipos/CP-6001-05-redirect-login.png" width="800px" alt="CP-6001-05 - RedirecciÃ³n a la pantalla de Login"></a><br>Barra de direcciones mostrando la ruta de login tras el intento de acceso a la vista de creaciÃ³n de equipos. |

