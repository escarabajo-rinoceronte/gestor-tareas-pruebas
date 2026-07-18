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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — DiseÃ±o de Pruebas E2E â€” Flujo de AdministraciÃ³n / Crear Proyecto (Backend Real)</td></tr>
      <tr><td class="label">Fecha</td><td>17/07/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# DiseÃ±o de Pruebas E2E â€” Flujo de AdministraciÃ³n / Crear Proyecto (Backend Real)

**VersiÃ³n del Documento:** 1.0  
**Tipo de Documento:** DiseÃ±o de Pruebas de Sistema (Caja Negra)  
**Caso de Prueba Asociado:** CP-E2E-ADM-001  
**MÃ³dulo Funcional Relacionado:** MOD-02 â€” GestiÃ³n de Proyectos  
**Escenario Funcional Relacionado:** ESC-2001 â€” CreaciÃ³n de un Nuevo Proyecto  
**EstÃ¡ndares de referencia:** IEEE 829, ISO/IEC/IEEE 29119

---

## 1. Contexto

Este documento describe el diseÃ±o de la prueba End-to-End del flujo de administraciÃ³n para crear un proyecto ejecutado contra el backend real de HOT Tasking Manager. El objetivo es validar que un usuario `ADMIN` puede iniciar sesiÃ³n, acceder al panel de gestiÃ³n, crear un nuevo proyecto importando un AOI GeoJSON, definir la grilla de tareas y guardar el proyecto como borrador.

## 2. Estrategia de DiseÃ±o

### 2.1. Enfoque general

- Prueba E2E automatizada con Playwright.
- NavegaciÃ³n real por el wizard de creaciÃ³n de proyectos.
- Backend real con base de datos PostgreSQL/PostGIS.
- ValidaciÃ³n de pasos del wizard, creaciÃ³n exitosa y redirecciÃ³n al proyecto creado.

### 2.2. TÃ©cnicas de caja negra aplicadas

| TÃ©cnica | AplicaciÃ³n |
| :--- | :--- |
| **Flujo de trabajo** | Recorrer secuencialmente los 4 pasos del wizard (AOI, tamaÃ±o de tareas, recorte y revisiÃ³n). |
| **ParticiÃ³n de equivalencia** | AOI vÃ¡lido en formato GeoJSON; se descartan formatos invÃ¡lidos y AOIs fuera de lÃ­mites. |
| **AnÃ¡lisis de valores lÃ­mite** | AOI pequeÃ±o (â‰ˆ1 kmÂ²) que genera una Ãºnica tarea, acotando el tiempo de procesamiento. |

## 3. CaracterÃ­sticas a probar

| CaracterÃ­stica | DescripciÃ³n |
| :--- | :--- |
| AutenticaciÃ³n de sesiÃ³n | Login mediante callback `/authorized/` con token de sesiÃ³n de administrador. |
| Panel de gestiÃ³n | Renderizado de `/manage` y acceso a "Create new project". |
| Wizard de creaciÃ³n | NavegaciÃ³n por `/manage/projects/new/` y sus 4 pasos. |
| ImportaciÃ³n de AOI | Carga de archivo GeoJSON y cÃ¡lculo de Ã¡rea/grilla. |
| SelecciÃ³n de organizaciÃ³n | SelecciÃ³n de la organizaciÃ³n de prueba en el paso de revisiÃ³n. |
| CreaciÃ³n de borrador | EnvÃ­o del formulario y redirecciÃ³n a `/manage/projects/{id}`. |

## 4. Condiciones de prueba

### 4.1. Precondiciones

1. Backend real y base de datos levantados con `docker-compose.e2e.yml`.
2. Script `scripts/e2e-seed.py` ejecutado.
3. Usuario `e2e_admin` con rol `ADMIN` (`role = 1`), email verificado y sesiÃ³n vÃ¡lida.
4. OrganizaciÃ³n `E2E Organisation` creada y visible para el administrador.
5. Archivo AOI de prueba disponible en `frontend/e2e/fixtures/test-aoi.geojson`.

### 4.2. Datos de entrada

| Dato | Valor | Origen |
| :--- | :--- | :--- |
| Usuario | `e2e_admin` | Seed |
| OrganizaciÃ³n | `E2E Organisation` | Seed |
| Nombre del proyecto | `E2E Admin Project {timestamp}` | Test |
| AOI | `test-aoi.geojson` (polÃ­gono pequeÃ±o) | Fixture |

### 4.3. Factores ambientales

- `E2E_BACKEND=real` debe estar configurado.
- `TM_APP_API_URL=http://127.0.0.1:5000/api` para que el frontend apunte al backend real.
- El overlay de webpack-dev-server se oculta durante la prueba para evitar interferencias.

## 5. Caso de prueba derivado

| ID Caso | Datos de entrada o escenario | Resultado Esperado | TÃ©cnicas Aplicadas |
| :--- | :--- | :--- | :--- |
| **CP-E2E-ADM-001** | Usuario `e2e_admin`, AOI `test-aoi.geojson`, organizaciÃ³n `E2E Organisation`. | El sistema permite completar el wizard, crea el proyecto como borrador y redirige a `/manage/projects/{id}`. | Flujo de trabajo, ParticiÃ³n de equivalencia |

## 6. Criterios de aceptaciÃ³n

- El usuario inicia sesiÃ³n exitosamente y accede al panel de gestiÃ³n.
- El wizard de creaciÃ³n de proyectos se carga correctamente.
- El AOI se importa y se calculan Ã¡rea y nÃºmero de tareas.
- Es posible avanzar por los pasos Set Task Sizes, Trim Task Grid y Review.
- El nombre del proyecto y la organizaciÃ³n son obligatorios y habilitan el botÃ³n **Create**.
- Tras crear, el sistema redirige a la pÃ¡gina de administraciÃ³n del proyecto reciÃ©n creado.

## 7. Criterios de Ã©xito adicionales (desempeÃ±o)

| MÃ©trica | Umbral |
| :--- | :--- |
| `loginToManage` | < 10 000 ms |
| `createProjectWizard` | < 120 000 ms |

## 8. Postcondiciones

- Un nuevo proyecto en estado `DRAFT` queda registrado en la base de datos.
- El proyecto queda asociado a la organizaciÃ³n `E2E Organisation`.

## 9. Trazabilidad

- Requisito funcional: un administrador debe poder crear proyectos en el sistema.
- Flujo de usuario automatizado: `frontend/e2e/flows/admin-create-project-flow.spec.js`.
- Datos de prueba: `scripts/e2e-seed.py` y `frontend/e2e/fixtures/test-aoi.geojson`.

