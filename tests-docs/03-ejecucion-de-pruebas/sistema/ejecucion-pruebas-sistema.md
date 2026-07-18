# Informe Consolidado de Ejecución — Pruebas de Sistema

**Proyecto:** HOT Tasking Manager — Sistema de Gestión de Tareas Colaborativas de Mapeo
**Curso:** Pruebas de Software
**Versión:** 1.0
**Fecha:** 19 de Julio de 2026
**Responsables:** Jhonatan (E2E) · Alexandra (Desempeño y Seguridad)
**Estándares:** IEEE 829 · ISO/IEC/IEEE 29119 · ISO/IEC 25010

---

## Índice

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Entorno de Ejecución](#2-entorno-de-ejecución)
3. [Flujo de Mapeo — CP-E2E-MAP-001](#3-flujo-de-mapeo--cp-e2e-map-001)
4. [Flujo de Validación — CP-E2E-VAL-001](#4-flujo-de-validación--cp-e2e-val-001)
5. [Flujo de Administración — CP-E2E-ADM-001](#5-flujo-de-administración--cp-e2e-adm-001)
6. [Prueba de Desempeño y Carga — K6](#6-prueba-de-desempeño-y-carga--k6)
7. [Prueba de Seguridad — SonarQube](#7-prueba-de-seguridad--sonarqube)
8. [Resumen de Resultados y Conclusiones](#8-resumen-de-resultados-y-conclusiones)

---

## 1. Resumen Ejecutivo

Las Pruebas de Sistema del HOT Tasking Manager se ejecutaron sobre un entorno completo levantado con Docker, validando los tres flujos críticos del sistema (Mapeo, Validación y Administración) de forma automatizada con Playwright, junto con pruebas no funcionales de **Desempeño** (Grafana K6) y **Seguridad** (SonarCloud + Gitleaks), integradas al pipeline de CI/CD de GitHub Actions.

| Tipo de Prueba | Herramienta | Responsable | Resultado |
| :--- | :--- | :--- | :--- |
| E2E — Flujo de Mapeo | Playwright | Jhonatan | ✅ APROBADO |
| E2E — Flujo de Validación | Playwright | Jhonatan | ✅ APROBADO |
| E2E — Flujo de Administración | Playwright | Jhonatan | ✅ APROBADO |
| Desempeño y Carga (50 VUs, 12 min) | Grafana K6 | Alexandra | ✅ APROBADO |
| Seguridad SAST (76k líneas de código) | SonarCloud + Gitleaks | Alexandra | ✅ EJECUTADO — Hallazgos documentados |

---

## 2. Entorno de Ejecución

| Componente | Versión / Configuración |
| :--- | :--- |
| Sistema operativo | Windows 10 Home Single Language |
| Docker Desktop | v2.0+ |
| Imagen backend | `ghcr.io/hotosm/tasking-manager/backend:main` |
| Base de datos | PostGIS 14-3.3 (`DB_MAX_CONNECTIONS=30`) |
| Proxy inverso | Traefik v3.6.1 (`localhost:3000 → backend:5000`) |
| Node.js | v18.x |
| Yarn | 1.22.22 |
| Playwright | Configurado en `frontend/package.json` |
| K6 | Grafana K6 v0.52+ |
| CI/CD | GitHub Actions (`wiki-sync.yml`, `seguridad-sonarqube.yml`) |

**URLs del entorno:**
- Frontend / API (Traefik): `http://localhost:3000`
- Base de datos: `localhost:5434`

---

## 3. Flujo de Mapeo — CP-E2E-MAP-001

**Responsable:** JhonAQ · **Fecha:** 2026-07-15 · **Herramienta:** Playwright (Chromium)

### 3.1. Datos de Prueba

| Campo | Valor |
| :--- | :--- |
| Usuario | `e2e_mapper` |
| ID de usuario | `9999001` |
| Proyecto | `E2E Mapping Project` |
| Tarea objetivo | `#2` (estado: READY) |

### 3.2. Caso de Prueba Ejecutado

| ID | Descripción | Tipo | Estado | Defectos |
| :--- | :--- | :--- | :--- | :--- |
| **CP-E2E-MAP-001** | Flujo completo de mapeo con backend real: login → explorar proyecto → seleccionar tarea READY → abrir editor iD. | Automatizado | ✅ Exitoso | Ninguno |

### 3.3. Resultado Esperado vs. Obtenido

| Resultado esperado | Resultado obtenido |
| :--- | :--- |
| El usuario `e2e_mapper` inicia sesión, visualiza el proyecto, selecciona la tarea `#2` (READY) y abre el editor iD. El sistema bloquea la tarea (`LOCKED_FOR_MAPPING`) y muestra `#id-container`. | Todas las navegaciones y verificaciones completaron sin errores. El editor iD se cargó correctamente. |

### 3.4. Pasos Ejecutados

1. Navegar a `/authorized/?username=e2e_mapper&session_token=...&redirect_to=/explore`
2. Verificar que la tarjeta del proyecto `E2E Mapping Project` es visible
3. Hacer clic en la tarjeta del proyecto
4. Verificar navegación a `/projects/{projectId}` y título visible
5. Navegar a `/projects/{projectId}/tasks?search=2`
6. Hacer clic en **Map selected task**
7. Verificar navegación a `/projects/{projectId}/map` y visibilidad de `#id-container`

### 3.5. Métricas de Desempeño

| Métrica | Valor obtenido | Umbral | Estado |
| :--- | :--- | :--- | :--- |
| `loginToExplore` | 3,497.27 ms | < 10,000 ms | ✅ Aprobado |
| `exploreToProjectDetail` | 375.18 ms | < 10,000 ms | ✅ Aprobado |
| `projectDetailToTaskSelection` | 516.04 ms | < 10,000 ms | ✅ Aprobado |
| `taskSelectionToEditor` | 6,752.44 ms | < 90,000 ms | ✅ Aprobado |

### 3.6. Salida de Consola

```text
Timings (ms): {
  loginToExplore: 3497.268400000001,
  exploreToProjectDetail: 375.1759999999995,
  projectDetailToTaskSelection: 516.0429999999978,
  taskSelectionToEditor: 6752.4382000000005
}
  ✓  2 [chromium] › e2e\flows\mapping-flow.spec.js:56:3 › Flujo de Mapeo (desempeño) › login -> buscar proyecto -> seleccionar tarea -> abrir editor de mapeo (11.5s)
```

### 3.7. Conclusión

El caso CP-E2E-MAP-001 se ejecutó **exitosamente** contra el backend real. El flujo completo de mapeo funcionó correctamente y todos los criterios de desempeño fueron satisfechos.

---

## 4. Flujo de Validación — CP-E2E-VAL-001

**Responsable:** JhonAQ · **Fecha:** 2026-07-15 · **Herramienta:** Playwright (Chromium)

### 4.1. Datos de Prueba

| Campo | Valor |
| :--- | :--- |
| Usuario | `e2e_validator` |
| ID de usuario | `9999002` |
| Proyecto | `E2E Mapping Project` |
| Tarea objetivo | `#1` (estado: MAPPED) |

### 4.2. Caso de Prueba Ejecutado

| ID | Descripción | Tipo | Estado | Defectos |
| :--- | :--- | :--- | :--- | :--- |
| **CP-E2E-VAL-001** | Flujo completo de validación con backend real: login → seleccionar tarea MAPPED → bloquear para validación → seleccionar VALIDATED → enviar. | Automatizado | ✅ Exitoso | Ninguno |

### 4.3. Resultado Esperado vs. Obtenido

| Resultado esperado | Resultado obtenido |
| :--- | :--- |
| El usuario `e2e_validator` selecciona la tarea `#1` (MAPPED), la bloquea para validación, selecciona `VALIDATED` y envía el formulario. El sistema redirige a la lista de tareas. | Todas las navegaciones y verificaciones completaron sin errores. El estado `VALIDATED` se aplicó correctamente. |

### 4.4. Pasos Ejecutados

1. Navegar a `/authorized/?username=e2e_validator&session_token=...&redirect_to=/explore`
2. Verificar que el proyecto `E2E Mapping Project` es visible
3. Navegar a `/projects/{projectId}/tasks?search=1`
4. Hacer clic en **Validate selected task** (o **Resume validation** si ya estaba bloqueada)
5. Verificar navegación a `/projects/{projectId}/validate`
6. Seleccionar la pestaña **Completion**
7. Seleccionar el radio `VALIDATED`
8. Hacer clic en **Submit task**
9. Verificar redirección a `/projects/{projectId}/tasks`

### 4.5. Métricas de Desempeño

| Métrica | Valor obtenido | Umbral | Estado |
| :--- | :--- | :--- | :--- |
| `loginToExplore` | 16,706.65 ms | < 20,000 ms | ✅ Aprobado |
| `taskSelectionToValidation` | 5,868.77 ms | < 90,000 ms | ✅ Aprobado |
| `validationToSubmit` | 672.01 ms | < 30,000 ms | ✅ Aprobado |

### 4.6. Salida de Consola

```text
Timings (ms): {
  loginToExplore: 16706.652000000002,
  taskSelectionToValidation: 5868.771199999996,
  validationToSubmit: 672.0126999999993
}
  ✓  3 [chromium] › e2e\flows\validation-flow.spec.js:56:3 › Flujo de Validación (funcional / usabilidad) › login como validador -> seleccionar tarea mapeada -> validar tarea (23.7s)
```

### 4.7. Conclusión

El caso CP-E2E-VAL-001 se ejecutó **exitosamente** contra el backend real. El flujo completo de validación funcionó correctamente y todos los criterios de desempeño fueron satisfechos.

---

## 5. Flujo de Administración — CP-E2E-ADM-001

**Responsable:** JhonAQ · **Fecha:** 2026-07-15 · **Herramienta:** Playwright (Chromium)

### 5.1. Datos de Prueba

| Campo | Valor |
| :--- | :--- |
| Usuario | `e2e_admin` |
| ID de usuario | `9999003` |
| Rol | ADMIN (role = 1) |
| Acción | Crear proyecto nuevo importando AOI GeoJSON |

### 5.2. Caso de Prueba Ejecutado

| ID | Descripción | Tipo | Estado | Defectos |
| :--- | :--- | :--- | :--- | :--- |
| **CP-E2E-ADM-001** | Flujo completo de creación de proyecto con backend real: login → panel manage → wizard de creación → guardar borrador. | Automatizado | ✅ Exitoso | Ninguno |

### 5.3. Resultado Esperado vs. Obtenido

| Resultado esperado | Resultado obtenido |
| :--- | :--- |
| El usuario `e2e_admin` crea un nuevo proyecto importando un AOI GeoJSON, avanza por el wizard, completa nombre y organización, y guarda como borrador. El sistema redirige a `/manage/projects/{id}`. | Todas las navegaciones y verificaciones completaron sin errores. El proyecto se creó correctamente en la base de datos. |

### 5.4. Pasos Ejecutados

1. Navegar a `/authorized/?username=e2e_admin&session_token=...&redirect_to=/manage`
2. Verificar que el panel **Manage** muestra el encabezado **Projects**
3. Navegar directamente a `/manage/projects/new/`
4. Subir el archivo `test-aoi.geojson`
5. Avanzar por los pasos **Set Tasks Sizes**, **Trim Task Grid** y **Review**
6. Completar el nombre del proyecto
7. Seleccionar la organización `E2E Organisation` mediante el combobox (teclado)
8. Hacer clic en **Create**
9. Verificar redirección a `/manage/projects/{id}`

### 5.5. Métricas de Desempeño

| Métrica | Valor obtenido | Umbral | Estado |
| :--- | :--- | :--- | :--- |
| `loginToManage` | 5,436.39 ms | < 20,000 ms | ✅ Aprobado |
| `createProjectWizard` | 5,627.15 ms | < 120,000 ms | ✅ Aprobado |

### 5.6. Salida de Consola

```text
Timings (ms): {
  loginToManage: 5436.3946000000005,
  createProjectWizard: 5627.154399999999
}
  ✓  1 [chromium] › e2e\flows\admin-create-project-flow.spec.js:31:3 › Flujo de Administración (funcional / usabilidad) › login como admin -> panel manage -> crear proyecto -> importar AOI -> guardar borrador (13.5s)
```

### 5.7. Conclusión

El caso CP-E2E-ADM-001 se ejecutó **exitosamente** contra el backend real. El flujo completo de creación de proyecto funcionó correctamente y todos los criterios de desempeño fueron satisfechos.

---

## 6. Prueba de Desempeño y Carga — K6

**Responsable:** Alexandra · **Fecha:** 2026-07-19 · **Herramienta:** Grafana K6
**Atributo de calidad (ISO/IEC 25010):** Eficiencia de Desempeño
**Referencia metodológica:** Myers, "The Art of Software Testing" — Pruebas de Estrés y Carga

### 6.1. Configuración del Escenario

| Parámetro | Valor |
| :--- | :--- |
| Usuarios virtuales máximos (VUs) | 50 |
| Duración total | 12 minutos (3 etapas de rampa) |
| Endpoint bajo prueba | `POST /api/v2/projects/1/tasks/actions/lock-for-mapping/{taskId}/` |
| Umbral de latencia | p(95) < 2,000 ms |
| Umbral de errores | rate < 5% |

### 6.2. Resultados Obtenidos

```
█ THRESHOLDS

  http_req_duration
  ✓ 'p(95)<2000' p(95)=1.76s

  http_req_failed
  ✓ 'rate<0.05' rate=0.04%

█ TOTAL RESULTS

  checks_total.......: 9330    12.845491/s
  checks_succeeded...: 100.00% 9330 out of 9330
  checks_failed......: 0.00%   0 out of 9330

  ✓ GET tasks status is 200
  ✓ POST lock: respuesta valida del sistema

  CUSTOM
  lock_200_ok....................: 1033   1.422229/s
  lock_403_conflict_or_state.....: 3632   5.000517/s

  HTTP
  http_req_duration..............: avg=272.94ms min=1.37ms med=14.64ms max=19.48s p(90)=1.14s p(95)=1.76s
  http_req_failed................: 0.04%  5 out of 10363
  http_reqs......................: 10363  14.267719/s

  EXECUTION
  iterations.....................: 4665   6.422745/s
  vus_max........................: 50
```

### 6.3. Evidencia Visual

![Resultados K6 en consola — 100% checks OK, p(95)=1.76s](/tests-docs/03-ejecucion-de-pruebas/sistema/k6-results.jpg)

### 6.4. Análisis de Contención Transaccional

El desglose de respuestas HTTP demuestra que el backend maneja la concurrencia extrema con integridad:

| Código | Conteo | Interpretación |
| :--- | :--- | :--- |
| `lock_200_ok` — 1,033 | 1,033 bloqueos exitosos | Un usuario adquirió la tarea correctamente |
| `lock_403_conflict_or_state` — 3,632 | Rechazos controlados | El sistema rechazó correctamente a usuarios tardíos: **Race Condition prevenida** |
| Errores reales | 5 de 10,363 peticiones (0.04%) | Dentro del umbral aceptable |

> El alto número de respuestas 403 **no es un error**: demuestra que el sistema protege correctamente la integridad de los datos — dos usuarios nunca pueden apropiarse de la misma tarea simultáneamente.

### 6.5. Hallazgo de Optimización Documentado

Durante las rondas de prueba se identificó un cuello de botella crítico:

| ID | Descripción | Causa Raíz | Resolución |
| :--- | :--- | :--- | :--- |
| **DEF-SYS-PERF-001** | El sistema colapsaba con 50 VUs cuando `DB_MAX_CONNECTIONS=8` | La operación `unlock` dispara un recálculo síncrono de medallas de usuario, abriendo una segunda conexión de DB simultáneamente | `DB_MAX_CONNECTIONS` elevado a 30 en entorno de pruebas |

### 6.6. Conclusión

**APROBADO.** El sistema soporta 50 usuarios concurrentes intentando bloquear tareas simultáneamente, con una tasa de error del 0.04% y respondiendo el 95% de las peticiones en menos de 1.76 segundos — dentro del umbral de aceptación de 2 segundos definido en el Plan de Pruebas.

---

## 7. Prueba de Seguridad — SonarQube

**Responsable:** Alexandra · **Fecha:** 2026-07-19
**Herramientas:** SonarCloud (SAST/SCA) + Gitleaks (Secret Scanning)
**Atributo de calidad (ISO/IEC 25010):** Seguridad
**Integración:** GitHub Actions CI/CD (`seguridad-sonarqube.yml`) — se ejecuta automáticamente en cada push a `develop`

### 7.1. Estrategia de Prueba

| Capa | Herramienta | Tipo | Objetivo |
| :--- | :--- | :--- | :--- |
| 1 | **Gitleaks** | Secret Scanning | Detectar tokens, contraseñas o claves API expuestas |
| 2 | **SonarCloud** | SAST + SCA | Detectar vulnerabilidades, bugs críticos y deuda técnica |

### 7.2. Vista General — Organización en SonarCloud

El pipeline de CI/CD procesó exitosamente las **76,000 líneas de código** del repositorio real.

![Vista general de la organización en SonarCloud mostrando el proyecto analizado](/tests-docs/03-ejecucion-de-pruebas/sistema/sonar-01-projects-overview.jpeg)

### 7.3. Dashboard del Proyecto — Estado de Calidad

![Dashboard de estado del proyecto: Quality Gate Failed con 1,595 issues totales](/tests-docs/03-ejecucion-de-pruebas/sistema/sonar-02-project-dashboard.jpeg)

**Interpretación del Quality Gate:**
> El Quality Gate indica **Failed**. Esto es el resultado **esperado y buscado** de una prueba de seguridad efectiva: la herramienta identificó deuda de seguridad real en el código. Una prueba que no encuentra nada en 76k líneas de código real habría sido inefectiva.

| Métrica Dashboard | Valor |
| :--- | :--- |
| Quality Gate | ❌ Failed (1 condición) |
| Open Issues totales | 1,595 |
| Duplicaciones | 1.2% |
| Coverage | 0.0% (no se envió reporte de cobertura — esperado) |

### 7.4. Snapshot de Seguridad

![Panel de seguridad: Rating E, 9 vulnerabilidades por severidad](/tests-docs/03-ejecucion-de-pruebas/sistema/sonar-03-security-snapshot.jpeg)

| Métrica de Seguridad | Valor |
| :--- | :--- |
| **Security Rating** | E (Crítico) |
| **Security Issues detectados** | 9 vulnerabilidades activas |
| Blocker | 11% |
| High | 11% |
| Medium | 56% |
| Low | 22% |
| Security Hotspots Reviewed | 100% ✅ |

### 7.5. Snapshot de Confiabilidad y Mantenibilidad

![Panel de confiabilidad (234 bugs) y mantenibilidad (1,485 code smells, rating A)](/tests-docs/03-ejecucion-de-pruebas/sistema/sonar-04-reliability-maintainability.jpeg)

| Métrica | Valor | Interpretación |
| :--- | :--- | :--- |
| **Reliability Rating** | E | 234 bugs potenciales identificados |
| Reliability Issues | 234 | Mayoría Medium (56%) y Low (32%) |
| **Maintainability Rating** | A ✅ | Excelente para un proyecto de 76k líneas |
| Maintainability Issues | 1,485 | Baja densidad de deuda técnica |

### 7.6. Análisis

**¿Por qué el Quality Gate falló?** Porque SonarQube encontró 9 vulnerabilidades de seguridad activas con al menos una de severidad Blocker. Este es exactamente el objetivo de una prueba SAST: exponer la deuda de seguridad existente en el sistema real.

**Punto positivo:** La calificación de **Mantenibilidad A** es notable. Para 76,000 líneas de código real de un sistema open-source de producción, solo 1,485 code smells representan una densidad muy baja de deuda técnica.

**Gitleaks:** No detectó secretos ni credenciales expuestas en el repositorio. ✅

### 7.7. Conclusión

| Aspecto | Resultado |
| :--- | :--- |
| Pipeline CI/CD integrado | ✅ Funciona en cada push a `develop` |
| Secret Scanning (Gitleaks) | ✅ Ningún secreto expuesto |
| Análisis SAST ejecutado | ✅ Exitoso sobre 76k líneas |
| Vulnerabilidades detectadas | 9 issues (requieren plan de remediación) |
| Objetivo de la prueba | ✅ **EJECUTADO** — Hallazgos documentados para backlog |

---

## 8. Resumen de Resultados y Conclusiones

### 8.1. Tabla de Resultados Globales

| ID Caso | Tipo | Responsable | Criterio | Resultado |
| :--- | :--- | :--- | :--- | :--- |
| CP-E2E-MAP-001 | E2E Funcional | Jhonatan | Todos los pasos exitosos + métricas < umbral | ✅ APROBADO |
| CP-E2E-VAL-001 | E2E Funcional | Jhonatan | Todos los pasos exitosos + métricas < umbral | ✅ APROBADO |
| CP-E2E-ADM-001 | E2E Funcional | Jhonatan | Todos los pasos exitosos + métricas < umbral | ✅ APROBADO |
| PERF-K6-001 | Desempeño/Carga | Alexandra | p(95) < 2000ms · rate < 5% | ✅ APROBADO |
| SEC-SONAR-001 | Seguridad SAST | Alexandra | Pipeline ejecutado, hallazgos documentados | ✅ EJECUTADO |

### 8.2. Defectos Encontrados

| ID | Tipo | Descripción | Estado |
| :--- | :--- | :--- | :--- |
| DEF-SYS-PERF-001 | Cuello de botella | `DB_MAX_CONNECTIONS=8` insuficiente para 50 VUs concurrentes | ✅ Resuelto (elevado a 30) |
| DEF-SYS-SEC-001 a 009 | Seguridad | 9 vulnerabilidades SAST detectadas por SonarCloud | 🔴 Pendiente remediación en sprints futuros |

### 8.3. Conclusión Final

El sistema Tasking Manager demuestra un nivel de calidad **suficiente para su estado actual de desarrollo**:
- Los tres flujos críticos de negocio (Mapeo, Validación, Administración) funcionan correctamente de extremo a extremo.
- El sistema soporta carga real de 50 usuarios concurrentes con latencias aceptables.
- Se identificaron 9 vulnerabilidades de seguridad que deben priorizarse en el backlog.

Se aprueba la ejecución de las Pruebas de Sistema para los módulos evaluados.
