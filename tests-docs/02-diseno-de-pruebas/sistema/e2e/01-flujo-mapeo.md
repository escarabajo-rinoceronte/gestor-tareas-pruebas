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
  <b>Proyecto:</b> HOT Tasking Manager — DiseÃ±o de Pruebas E2E â€” Flujo de Mapeo (Backend Real) <br>
  <b>Fecha de Elaboración:</b> 17/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# DiseÃ±o de Pruebas E2E â€” Flujo de Mapeo (Backend Real)

**VersiÃ³n del Documento:** 1.0  
**Tipo de Documento:** DiseÃ±o de Pruebas de Sistema (Caja Negra)  
**Caso de Prueba Asociado:** CP-E2E-MAP-001  
**MÃ³dulo Funcional Relacionado:** MOD-03 â€” EjecuciÃ³n de Mapeo (Tasking)  
**Escenario Funcional Relacionado:** ESC-3001 â€” Solicitud de Bloqueo e Inicio de Tarea de Mapeo  
**EstÃ¡ndares de referencia:** IEEE 829, ISO/IEC/IEEE 29119

---

## 1. Contexto

Este documento describe el diseÃ±o de la prueba End-to-End del flujo de mapeo ejecutado contra el backend real de HOT Tasking Manager. El objetivo es validar el "happy path" de un usuario `MAPPER` que inicia sesiÃ³n, explora proyectos publicados, selecciona una tarea en estado `READY` y la abre en el editor iD, verificando la integraciÃ³n completa frontend-backend-base de datos.

Para el detalle de actores, restricciones y reglas de negocio del mÃ³dulo de mapeo, referirse al [DiseÃ±o de Pruebas Funcionales â€” MOD-03](/tests-docs/02-diseno-de-pruebas/funcionales/03-ejecucion-de-mapeo.md).

## 2. Estrategia de DiseÃ±o

### 2.1. Enfoque general

- Prueba E2E automatizada con Playwright.
- NavegaciÃ³n real por la interfaz de usuario.
- Backend real con base de datos PostgreSQL/PostGIS.
- ValidaciÃ³n de estados y navegaciÃ³n, ademÃ¡s de mÃ©tricas de desempeÃ±o.

### 2.2. TÃ©cnicas de caja negra aplicadas

| TÃ©cnica | AplicaciÃ³n |
| :--- | :--- |
| **TransiciÃ³n de estados** | Verificar que la tarea seleccionada pasa de `READY` a `LOCKED_FOR_MAPPING` tras el bloqueo. |
| **ParticiÃ³n de equivalencia** | Editor web (`iD`) como clase vÃ¡lida; el flujo no evalÃºa editores locales ni estados invÃ¡lidos. |
| **AnÃ¡lisis de valores lÃ­mite** | Tiempos de respuesta en cada etapa del flujo, con umbrales generosos para entorno de desarrollo. |

## 3. CaracterÃ­sticas a probar

| CaracterÃ­stica | DescripciÃ³n |
| :--- | :--- |
| AutenticaciÃ³n de sesiÃ³n | Login mediante callback `/authorized/` con token de sesiÃ³n vÃ¡lido. |
| ExploraciÃ³n de proyectos | Renderizado de tarjetas de proyectos publicados desde `/api/v2/projects/`. |
| Detalle de proyecto | NavegaciÃ³n a `/projects/{id}` y carga de resumen. |
| SelecciÃ³n de tarea | BÃºsqueda de tarea por ID en `/projects/{id}/tasks`. |
| Apertura de editor | NavegaciÃ³n a `/projects/{id}/map` y carga del contenedor `#id-container`. |

## 4. Condiciones de prueba

### 4.1. Precondiciones

1. Backend real y base de datos levantados con `docker-compose.e2e.yml`.
2. Script `scripts/e2e-seed.py` ejecutado.
3. Proyecto `E2E Mapping Project` publicado con al menos una tarea en estado `READY`.
4. Usuario `e2e_mapper` con rol mapper, email verificado y sesiÃ³n vÃ¡lida.

### 4.2. Datos de entrada

| Dato | Valor | Origen |
| :--- | :--- | :--- |
| Usuario | `e2e_mapper` | Seed |
| Proyecto | `E2E Mapping Project` | Seed |
| Tarea a mapear | `#2` (READY) | Seed |
| Editor | iD (`#id-container`) | ConfiguraciÃ³n del proyecto |

### 4.3. Factores ambientales

- `E2E_BACKEND=real` debe estar configurado.
- `TM_APP_API_URL=http://127.0.0.1:5000/api` para que el frontend apunte al backend real.
- El overlay de webpack-dev-server se oculta durante la prueba para evitar interferencias.

## 5. Caso de prueba derivado

| ID Caso | Datos de entrada o escenario | Resultado Esperado | TÃ©cnicas Aplicadas |
| :--- | :--- | :--- | :--- |
| **CP-E2E-MAP-001** | Usuario `e2e_mapper`, proyecto `E2E Mapping Project`, tarea `#2` READY, editor iD. | El sistema permite el bloqueo de la tarea (`LOCKED_FOR_MAPPING`) y carga el editor iD. El usuario navega por login â†’ explore â†’ project detail â†’ task selection â†’ map editor. | TransiciÃ³n de estados, ParticiÃ³n de equivalencia |

## 6. Criterios de aceptaciÃ³n

- El usuario inicia sesiÃ³n exitosamente.
- El proyecto de prueba es visible en la pÃ¡gina de exploraciÃ³n.
- La navegaciÃ³n al detalle del proyecto es correcta.
- La tarea `#2` puede seleccionarse y abrirse en el editor iD.
- Los tiempos medidos no superan los umbrales establecidos.

## 7. Criterios de Ã©xito adicionales (desempeÃ±o)

| MÃ©trica | Umbral |
| :--- | :--- |
| `loginToExplore` | < 10 000 ms |
| `exploreToProjectDetail` | < 10 000 ms |
| `projectDetailToTaskSelection` | < 10 000 ms |
| `taskSelectionToEditor` | < 90 000 ms |

## 8. Postcondiciones

- La tarea `#2` queda bloqueada para mapeo por el usuario `e2e_mapper` en la base de datos.
- El entorno puede re-seedearse para ejecutar la prueba nuevamente.

## 9. Trazabilidad

- Requisito funcional: un mapper debe poder seleccionar y abrir una tarea lista para mapear.
- Flujo de usuario automatizado: `frontend/e2e/flows/mapping-flow.spec.js`.
- Datos de prueba: `scripts/e2e-seed.py`.
- DiseÃ±o funcional base: [MOD-03](/tests-docs/02-diseno-de-pruebas/funcionales/03-ejecucion-de-mapeo.md).



