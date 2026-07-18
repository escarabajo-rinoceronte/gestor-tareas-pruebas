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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — DiseÃ±o de Pruebas E2E â€” Flujo de ValidaciÃ³n (Backend Real)</td></tr>
      <tr><td class="label">Fecha</td><td>17/07/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# DiseÃ±o de Pruebas E2E â€” Flujo de ValidaciÃ³n (Backend Real)

**VersiÃ³n del Documento:** 1.0  
**Tipo de Documento:** DiseÃ±o de Pruebas de Sistema (Caja Negra)  
**Caso de Prueba Asociado:** CP-E2E-VAL-001  
**MÃ³dulo Funcional Relacionado:** MOD-04 â€” ValidaciÃ³n de Tareas  
**Escenario Funcional Relacionado:** ESC-4001 â€” Solicitud de Bloqueo y ValidaciÃ³n de Tarea Mapeada  
**EstÃ¡ndares de referencia:** IEEE 829, ISO/IEC/IEEE 29119

---

## 1. Contexto

Este documento describe el diseÃ±o de la prueba End-to-End del flujo de validaciÃ³n ejecutado contra el backend real de HOT Tasking Manager. El objetivo es validar el "happy path" de un usuario `VALIDATOR` que inicia sesiÃ³n, localiza una tarea en estado `MAPPED`, la bloquea para validaciÃ³n, selecciona el estado `VALIDATED` y envÃ­a el formulario, verificando la integraciÃ³n completa frontend-backend-base de datos.

## 2. Estrategia de DiseÃ±o

### 2.1. Enfoque general

- Prueba E2E automatizada con Playwright.
- NavegaciÃ³n real por la interfaz de usuario.
- Backend real con base de datos PostgreSQL/PostGIS sembrada con datos controlados.
- ValidaciÃ³n de estados, navegaciÃ³n y mÃ©tricas de desempeÃ±o.

### 2.2. TÃ©cnicas de caja negra aplicadas

| TÃ©cnica | AplicaciÃ³n |
| :--- | :--- |
| **TransiciÃ³n de estados** | Verificar que la tarea pasa de `MAPPED` â†’ `LOCKED_FOR_VALIDATION` â†’ `VALIDATED`. |
| **ParticiÃ³n de equivalencia** | ValidaciÃ³n individual de una tarea (`VALIDATED` / `INVALIDATED`); el flujo no evalÃºa validaciÃ³n masiva. |
| **AnÃ¡lisis de valores lÃ­mite** | Tiempos de respuesta en cada etapa, con umbrales generosos para entorno de desarrollo. |

## 3. CaracterÃ­sticas a probar

| CaracterÃ­stica | DescripciÃ³n |
| :--- | :--- |
| AutenticaciÃ³n de sesiÃ³n | Login mediante callback `/authorized/` con token de sesiÃ³n vÃ¡lido del validador. |
| ExploraciÃ³n de proyecto | Renderizado del detalle del proyecto publicado. |
| SelecciÃ³n de tarea mapeada | BÃºsqueda de tarea por ID en `/projects/{id}/tasks`. |
| Bloqueo para validaciÃ³n | Clic en **Validate selected task** (o **Resume validation**) y redirecciÃ³n a `/projects/{id}/validate`. |
| Panel de validaciÃ³n | Cambio a la pestaÃ±a **Completion** y selecciÃ³n de `VALIDATED`. |
| EnvÃ­o de validaciÃ³n | Clic en **Submit task** y redirecciÃ³n a la lista de tareas. |

## 4. Condiciones de prueba

### 4.1. Precondiciones

1. Backend real y base de datos levantados con `docker-compose.e2e.yml`.
2. Script `scripts/e2e-seed.py` ejecutado (limpia y recrea el proyecto de prueba).
3. Proyecto `E2E Mapping Project` publicado con al menos una tarea en estado `MAPPED`.
4. Usuario `e2e_validator` con rol mapper, email verificado y sesiÃ³n vÃ¡lida.
5. Archivo `frontend/e2e/.e2e-seed.json` generado y accesible.

### 4.2. Datos de entrada

| Dato | Valor | Origen |
| :--- | :--- | :--- |
| Usuario | `e2e_validator` | Seed |
| Proyecto | `E2E Mapping Project` | Seed |
| Tarea a validar | `#1` (MAPPED) | Seed |
| Estado objetivo | `VALIDATED` | InteracciÃ³n del usuario |

### 4.3. Factores ambientales

- `E2E_BACKEND=real` debe estar configurado.
- `TM_APP_API_URL=http://127.0.0.1:5000/api` para que el frontend apunte al backend real.
- El overlay de webpack-dev-server se oculta durante la prueba para evitar interferencias.

## 5. Caso de prueba derivado

| ID Caso | Datos de entrada o escenario | Resultado Esperado | TÃ©cnicas Aplicadas |
| :--- | :--- | :--- | :--- |
| **CP-E2E-VAL-001** | Usuario `e2e_validator`, proyecto `E2E Mapping Project`, tarea `#1` MAPPED. | El sistema bloquea la tarea para validaciÃ³n, permite seleccionar `VALIDATED`, envÃ­a el formulario y redirige a la lista de tareas con la tarea en estado `VALIDATED`. | TransiciÃ³n de estados, ParticiÃ³n de equivalencia |

## 6. Criterios de aceptaciÃ³n

- El usuario inicia sesiÃ³n exitosamente.
- El proyecto de prueba es visible.
- La tarea `#1` aparece como mapeada y se puede bloquear para validaciÃ³n.
- La navegaciÃ³n a la vista de validaciÃ³n es correcta.
- El panel de validaciÃ³n se muestra al seleccionar la pestaÃ±a **Completion**.
- Es posible seleccionar `VALIDATED` y enviar la tarea.
- La redirecciÃ³n final es la lista de tareas del proyecto.

## 7. Criterios de Ã©xito adicionales (desempeÃ±o)

| MÃ©trica | Umbral |
| :--- | :--- |
| `loginToExplore` | < 10 000 ms |
| `taskSelectionToValidation` | < 90 000 ms |
| `validationToSubmit` | < 30 000 ms |

## 8. Postcondiciones

- La tarea `#1` queda en estado `VALIDATED` en la base de datos.
- El entorno puede re-seedearse para ejecutar la prueba nuevamente.

## 9. Trazabilidad

- Requisito funcional: un validador debe poder revisar y validar tareas mapeadas.
- Flujo de usuario automatizado: `frontend/e2e/flows/validation-flow.spec.js`.
- Datos de prueba: `scripts/e2e-seed.py`.

