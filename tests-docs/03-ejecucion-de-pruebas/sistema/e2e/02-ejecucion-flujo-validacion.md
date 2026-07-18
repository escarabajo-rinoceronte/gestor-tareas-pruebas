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
  <b>Proyecto:</b> HOT Tasking Manager — EjecuciÃ³n de Casos de Prueba E2E â€” Flujo de ValidaciÃ³n (Backend Real) <br>
  <b>Fecha de Elaboración:</b> 17/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# EjecuciÃ³n de Casos de Prueba E2E â€” Flujo de ValidaciÃ³n (Backend Real)

**VersiÃ³n del Documento:** 1.0  
**Tipo de Documento:** Reporte de EjecuciÃ³n de Pruebas  
**Escenario de Prueba:** ESC-4001 â€” Solicitud de Bloqueo y ValidaciÃ³n de Tarea Mapeada  
**Caso de Prueba:** CP-E2E-VAL-001  
**DiseÃ±o Asociado:** [DiseÃ±o E2E â€” Flujo de ValidaciÃ³n](/tests-docs/02-diseno-de-pruebas/e2e-backend-real/02-flujo-validacion.md)  
**Plan Asociado:** [Plan de Pruebas E2E contra Backend Real](/tests-docs/01-plan-de-pruebas/05-plan-pruebas-e2e-backend-real/plan-pruebas-e2e-backend-real.md)  
**Fecha de EjecuciÃ³n:** 2026-07-15  
**Responsable:** JhonAQ  
**EstÃ¡ndares de referencia:** IEEE 829, ISO/IEC/IEEE 29119

---

## 1. InformaciÃ³n General

| Atributo | Valor |
| :--- | :--- |
| **Sistema bajo prueba** | HOT Tasking Manager â€” Flujo de validaciÃ³n End-to-End |
| **Tipo de ejecuciÃ³n** | Automatizada |
| **Herramienta** | Playwright Test |
| **Navegador** | Chromium |
| **Ambiente** | Local / desarrollo |

## 2. Entorno de EjecuciÃ³n

| Componente | VersiÃ³n / ConfiguraciÃ³n |
| :--- | :--- |
| Sistema operativo | Windows 10 Home Single Language |
| Docker Desktop | (incluido en el entorno) |
| Imagen backend | `ghcr.io/hotosm/tasking-manager/backend:main` (target debug) |
| Base de datos | PostGIS 14-3.3 |
| Node.js | v18.x |
| Yarn | 1.22.22 |
| Playwright | (versiÃ³n definida en `frontend/package.json`) |

### URLs del entorno

- Frontend: `http://127.0.0.1:3000`
- Backend: `http://127.0.0.1:5000`
- Base de datos: `127.0.0.1:5434`

## 3. Datos de Prueba Utilizados

| Campo | Valor |
| :--- | :--- |
| Usuario | `e2e_validator` |
| ID de usuario | `9999002` |
| Proyecto | `E2E Mapping Project` |
| ID de proyecto | `36` (variable segÃºn seed) |
| Tarea mapeada | `#1` (MAPPED) |

> El ID del proyecto puede variar entre ejecuciones porque el seed limpia y recrea el proyecto.

## 4. PreparaciÃ³n del Ambiente

### 4.1. Levantar backend y base de datos

```bash
docker compose --env-file tasking-manager.env \
  -f docker-compose.yml -f docker-compose.e2e.yml \
  up -d tm-db tm-migration tm-backend
```

### 4.2. Sembrar datos de prueba (automÃ¡tico)

Cuando se ejecuta la suite con `E2E_BACKEND=real`, Playwright corre `frontend/e2e/global-setup.js` antes de los tests, el cual ejecuta `scripts/e2e-seed.py` dentro del contenedor `tm-backend`.

Si prefieres correr el seed manualmente:

```bash
docker compose --env-file tasking-manager.env \
  -f docker-compose.yml -f docker-compose.e2e.yml \
  exec tm-backend python scripts/e2e-seed.py
```

### 4.3. Ejecutar el caso de prueba

```bash
cd frontend
E2E_BACKEND=real yarn test:e2e --grep "Flujo de ValidaciÃ³n"
```

## 5. EjecuciÃ³n de CP-E2E-VAL-001

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :--- | :--- | :--- | :--- | :--- |
| **CP-E2E-VAL-001** | Validar el flujo completo de validaciÃ³n con backend real: login â†’ seleccionar tarea MAPPED â†’ bloquear para validaciÃ³n â†’ seleccionar VALIDATED â†’ enviar. | Automatizado | Exitoso | Ninguno |

### 5.1. Resultado esperado vs. obtenido

| Resultado esperado | Resultado obtenido |
| :--- | :--- |
| El usuario `e2e_validator` inicia sesiÃ³n, accede al proyecto `E2E Mapping Project`, selecciona la tarea `#1` en estado MAPPED, la bloquea para validaciÃ³n, selecciona `VALIDATED` y envÃ­a el formulario. El sistema redirige a la lista de tareas con la tarea validada. | Todas las navegaciones y verificaciones completaron sin errores. El estado `VALIDATED` se aplicÃ³ correctamente. |

### 5.2. Pasos ejecutados

1. Navegar a `/authorized/?username=e2e_validator&session_token=...&redirect_to=/explore`.
2. Verificar que el proyecto `E2E Mapping Project` es visible.
3. Navegar a `/projects/{projectId}/tasks?search=1`.
4. Hacer clic en **Validate selected task** (o **Resume validation** si la tarea ya estaba bloqueada).
5. Verificar navegaciÃ³n a `/projects/{projectId}/validate`.
6. Seleccionar la pestaÃ±a **Completion**.
7. Seleccionar el radio `VALIDATED`.
8. Hacer clic en **Submit task**.
9. Verificar redirecciÃ³n a `/projects/{projectId}/tasks`.

## 6. MÃ©tricas de DesempeÃ±o

| MÃ©trica | Valor obtenido | Umbral | Estado |
| :--- | :--- | :--- | :--- |
| `loginToExplore` | 16 706.65 ms | < 20 000 ms | âœ… Aprobado |
| `taskSelectionToValidation` | 5 868.77 ms | < 90 000 ms | âœ… Aprobado |
| `validationToSubmit` | 672.01 ms | < 30 000 ms | âœ… Aprobado |

## 7. Salida de la EjecuciÃ³n

La siguiente salida corresponde a la ejecuciÃ³n conjunta de la suite completa (`E2E_BACKEND=real yarn test:e2e`):

```text
Timings (ms): {
  loginToExplore: 16706.652000000002,
  taskSelectionToValidation: 5868.771199999996,
  validationToSubmit: 672.0126999999993
}
  âœ“  3 [chromium] â€º e2e\flows\validation-flow.spec.js:56:3 â€º Flujo de ValidaciÃ³n (funcional / usabilidad) â€º login como validador -> seleccionar tarea mapeada -> validar tarea (23.7s)
```

## 8. Evidencias

- **Salida de consola:** incluida en la secciÃ³n 7.
- **Video de ejecuciÃ³n:** generado por Playwright en `frontend/test-results/flows-validation-flow-.../video.webm`.
- **Trazas de Playwright:** generadas en `frontend/test-results/`.

## 9. ConclusiÃ³n

El caso de prueba CP-E2E-VAL-001 se ejecutÃ³ exitosamente contra el backend real. El flujo completo de validaciÃ³n (login, selecciÃ³n de tarea MAPPED, bloqueo para validaciÃ³n, selecciÃ³n de `VALIDATED` y envÃ­o) funcionÃ³ correctamente y todos los criterios de desempeÃ±o definidos fueron satisfechos.

## 10. Observaciones

- La prueba maneja tanto el botÃ³n **Validate selected task** como **Resume validation**, ya que una ejecuciÃ³n previa puede haber dejado la tarea bloqueada.
- En la vista de validaciÃ³n, el panel de acciÃ³n se encuentra en la pestaÃ±a **Completion**; el test la activa antes de interactuar con los radios.
- El seed ahora limpia tambiÃ©n la tabla `messages` para evitar errores de clave forÃ¡nea al recrear el proyecto.
- La autenticaciÃ³n se realiza con tokens de sesiÃ³n firmados localmente para usuarios sembrados en la base de datos.

## 11. PrÃ³ximos Pasos

- Mantener el seed idempotente para que las ejecuciones repetidas de la suite completa partan del mismo estado.
- Considerar un `globalSetup` o `test.beforeAll` que ejecute el seed cuando se corra la suite completa.



