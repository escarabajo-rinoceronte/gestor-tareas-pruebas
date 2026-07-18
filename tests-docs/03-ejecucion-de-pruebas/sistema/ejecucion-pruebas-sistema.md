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
  <b>Proyecto:</b> HOT Tasking Manager — Informe Consolidado de EjecuciÃ³n â€” Pruebas de Sistema <br>
  <b>Fecha de Elaboración:</b> 19/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Informe Consolidado de EjecuciÃ³n â€” Pruebas de Sistema

**Proyecto:** HOT Tasking Manager â€” Sistema de GestiÃ³n de Tareas Colaborativas de Mapeo
**Curso:** Pruebas de Software
**VersiÃ³n:** 1.0
**Fecha:** 19 de Julio de 2026
**Responsables:** Jhonatan (E2E) Â· Alexandra (DesempeÃ±o y Seguridad)
**EstÃ¡ndares:** IEEE 829 Â· ISO/IEC/IEEE 29119 Â· ISO/IEC 25010

---

## Ãndice

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Entorno de EjecuciÃ³n](#2-entorno-de-ejecuciÃ³n)
3. [Flujo de Mapeo â€” CP-E2E-MAP-001](#3-flujo-de-mapeo--cp-e2e-map-001)
4. [Flujo de ValidaciÃ³n â€” CP-E2E-VAL-001](#4-flujo-de-validaciÃ³n--cp-e2e-val-001)
5. [Flujo de AdministraciÃ³n â€” CP-E2E-ADM-001](#5-flujo-de-administraciÃ³n--cp-e2e-adm-001)
6. [Prueba de DesempeÃ±o y Carga â€” K6](#6-prueba-de-desempeÃ±o-y-carga--k6)
7. [Prueba de Seguridad â€” SonarQube](#7-prueba-de-seguridad--sonarqube)
8. [Resumen de Resultados y Conclusiones](#8-resumen-de-resultados-y-conclusiones)

---

## 1. Resumen Ejecutivo

Las Pruebas de Sistema del HOT Tasking Manager se ejecutaron sobre un entorno completo levantado con Docker, validando los tres flujos crÃ­ticos del sistema (Mapeo, ValidaciÃ³n y AdministraciÃ³n) de forma automatizada con Playwright, junto con pruebas no funcionales de **DesempeÃ±o** (Grafana K6) y **Seguridad** (SonarCloud + Gitleaks), integradas al pipeline de CI/CD de GitHub Actions.

| Tipo de Prueba | Herramienta | Responsable | Resultado |
| :--- | :--- | :--- | :--- |
| E2E â€” Flujo de Mapeo | Playwright | Jhonatan | âœ… APROBADO |
| E2E â€” Flujo de ValidaciÃ³n | Playwright | Jhonatan | âœ… APROBADO |
| E2E â€” Flujo de AdministraciÃ³n | Playwright | Jhonatan | âœ… APROBADO |
| DesempeÃ±o y Carga (50 VUs, 12 min) | Grafana K6 | Alexandra | âœ… APROBADO |
| Seguridad SAST (76k lÃ­neas de cÃ³digo) | SonarCloud + Gitleaks | Alexandra | âœ… EJECUTADO â€” Hallazgos documentados |

### 1.1. Alcance: Casos de Prueba por Atributo de Calidad (ISO/IEC 25010)

Se seleccionaron **3 atributos de calidad** y se diseÃ±aron y ejecutaron **8 casos de prueba de sistema** en total. Todos son **automatizados y reproducibles** en el pipeline CI/CD.

**Atributo 1 â€” Funcionalidad (E2E con Playwright)**

| # | ID | Escenario | Estado |
| :--- | :--- | :--- | :--- |
| 1 | CP-E2E-MAP-001 | Flujo completo de Mapeo: login â†’ explorar â†’ seleccionar tarea READY â†’ abrir editor iD | âœ… Ejecutado |
| 2 | CP-E2E-VAL-001 | Flujo completo de ValidaciÃ³n: login â†’ seleccionar tarea MAPPED â†’ validar â†’ enviar | âœ… Ejecutado |
| 3 | CP-E2E-ADM-001 | Flujo completo de AdministraciÃ³n: login â†’ panel manage â†’ crear proyecto â†’ guardar borrador | âœ… Ejecutado |

**Atributo 2 â€” Eficiencia de DesempeÃ±o (Grafana K6)**

| # | ID | Escenario | Estado |
| :--- | :--- | :--- | :--- |
| 4 | PERF-K6-001 | Carga sostenida: 50 usuarios virtuales durante 12 minutos â€” p(95) < 2,000 ms, tasa de error < 5% | âœ… Ejecutado |
| 5 | PERF-K6-002 | ContenciÃ³n transaccional: 50 VUs compitiendo por la misma tarea â€” verificaciÃ³n de Race Condition prevention (HTTP 403) | âœ… Ejecutado |

**Atributo 3 â€” Seguridad (SonarCloud + Gitleaks en GitHub Actions)**

| # | ID | Escenario | Estado |
| :--- | :--- | :--- | :--- |
| 6 | SEC-SAST-001 | AnÃ¡lisis estÃ¡tico de vulnerabilidades (SAST) sobre 76,000 lÃ­neas de cÃ³digo con SonarCloud | âœ… Ejecutado |
| 7 | SEC-SECRET-001 | Escaneo de secretos y credenciales expuestas en el repositorio con Gitleaks | âœ… Ejecutado |
| 8 | SEC-CICD-001 | IntegraciÃ³n continua de seguridad: pipeline automÃ¡tico en cada push a `develop` | âœ… Ejecutado |

---

## 2. Entorno de EjecuciÃ³n

| Componente | VersiÃ³n / ConfiguraciÃ³n |
| :--- | :--- |
| Sistema operativo | Windows 10 Home Single Language |
| Docker Desktop | v2.0+ |
| Imagen backend | `ghcr.io/hotosm/tasking-manager/backend:main` |
| Base de datos | PostGIS 14-3.3 (`DB_MAX_CONNECTIONS=30`) |
| Proxy inverso | Traefik v3.6.1 (`localhost:3000 â†’ backend:5000`) |
| Node.js | v18.x |
| Yarn | 1.22.22 |
| Playwright | Configurado en `frontend/package.json` |
| K6 | Grafana K6 v0.52+ |
| CI/CD | GitHub Actions (`wiki-sync.yml`, `seguridad-sonarqube.yml`) |

**URLs del entorno:**
- Frontend / API (Traefik): `http://localhost:3000`
- Base de datos: `localhost:5434`

---

## 3. Flujo de Mapeo â€” CP-E2E-MAP-001

**Responsable:** JhonAQ Â· **Fecha:** 2026-07-15 Â· **Herramienta:** Playwright (Chromium)

### 3.1. Datos de Prueba

| Campo | Valor |
| :--- | :--- |
| Usuario | `e2e_mapper` |
| ID de usuario | `9999001` |
| Proyecto | `E2E Mapping Project` |
| Tarea objetivo | `#2` (estado: READY) |

### 3.2. Caso de Prueba Ejecutado

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :--- | :--- | :--- | :--- | :--- |
| **CP-E2E-MAP-001** | Flujo completo de mapeo con backend real: login â†’ explorar proyecto â†’ seleccionar tarea READY â†’ abrir editor iD. | Automatizado | âœ… Exitoso | Ninguno |

### 3.3. Resultado Esperado vs. Obtenido

| Resultado esperado | Resultado obtenido |
| :--- | :--- |
| El usuario `e2e_mapper` inicia sesiÃ³n, visualiza el proyecto, selecciona la tarea `#2` (READY) y abre el editor iD. El sistema bloquea la tarea (`LOCKED_FOR_MAPPING`) y muestra `#id-container`. | Todas las navegaciones y verificaciones completaron sin errores. El editor iD se cargÃ³ correctamente. |

### 3.4. Pasos Ejecutados

1. Navegar a `/authorized/?username=e2e_mapper&session_token=...&redirect_to=/explore`
2. Verificar que la tarjeta del proyecto `E2E Mapping Project` es visible
3. Hacer clic en la tarjeta del proyecto
4. Verificar navegaciÃ³n a `/projects/{projectId}` y tÃ­tulo visible
5. Navegar a `/projects/{projectId}/tasks?search=2`
6. Hacer clic en **Map selected task**
7. Verificar navegaciÃ³n a `/projects/{projectId}/map` y visibilidad de `#id-container`

### 3.5. MÃ©tricas de DesempeÃ±o

| MÃ©trica | Valor obtenido | Umbral | Estado |
| :--- | :--- | :--- | :--- |
| `loginToExplore` | 3,497.27 ms | < 10,000 ms | âœ… Aprobado |
| `exploreToProjectDetail` | 375.18 ms | < 10,000 ms | âœ… Aprobado |
| `projectDetailToTaskSelection` | 516.04 ms | < 10,000 ms | âœ… Aprobado |
| `taskSelectionToEditor` | 6,752.44 ms | < 90,000 ms | âœ… Aprobado |

### 3.6. Salida de Consola

```text
Timings (ms): {
  loginToExplore: 3497.268400000001,
  exploreToProjectDetail: 375.1759999999995,
  projectDetailToTaskSelection: 516.0429999999978,
  taskSelectionToEditor: 6752.4382000000005
}
  âœ“  2 [chromium] â€º e2e\flows\mapping-flow.spec.js:56:3 â€º Flujo de Mapeo (desempeÃ±o) â€º login -> buscar proyecto -> seleccionar tarea -> abrir editor de mapeo (11.5s)
```

### 3.7. ConclusiÃ³n

El caso CP-E2E-MAP-001 se ejecutÃ³ **exitosamente** contra el backend real. El flujo completo de mapeo funcionÃ³ correctamente y todos los criterios de desempeÃ±o fueron satisfechos.

---

## 4. Flujo de ValidaciÃ³n â€” CP-E2E-VAL-001

**Responsable:** JhonAQ Â· **Fecha:** 2026-07-15 Â· **Herramienta:** Playwright (Chromium)

### 4.1. Datos de Prueba

| Campo | Valor |
| :--- | :--- |
| Usuario | `e2e_validator` |
| ID de usuario | `9999002` |
| Proyecto | `E2E Mapping Project` |
| Tarea objetivo | `#1` (estado: MAPPED) |

### 4.2. Caso de Prueba Ejecutado

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :--- | :--- | :--- | :--- | :--- |
| **CP-E2E-VAL-001** | Flujo completo de validaciÃ³n con backend real: login â†’ seleccionar tarea MAPPED â†’ bloquear para validaciÃ³n â†’ seleccionar VALIDATED â†’ enviar. | Automatizado | âœ… Exitoso | Ninguno |

### 4.3. Resultado Esperado vs. Obtenido

| Resultado esperado | Resultado obtenido |
| :--- | :--- |
| El usuario `e2e_validator` selecciona la tarea `#1` (MAPPED), la bloquea para validaciÃ³n, selecciona `VALIDATED` y envÃ­a el formulario. El sistema redirige a la lista de tareas. | Todas las navegaciones y verificaciones completaron sin errores. El estado `VALIDATED` se aplicÃ³ correctamente. |

### 4.4. Pasos Ejecutados

1. Navegar a `/authorized/?username=e2e_validator&session_token=...&redirect_to=/explore`
2. Verificar que el proyecto `E2E Mapping Project` es visible
3. Navegar a `/projects/{projectId}/tasks?search=1`
4. Hacer clic en **Validate selected task** (o **Resume validation** si ya estaba bloqueada)
5. Verificar navegaciÃ³n a `/projects/{projectId}/validate`
6. Seleccionar la pestaÃ±a **Completion**
7. Seleccionar el radio `VALIDATED`
8. Hacer clic en **Submit task**
9. Verificar redirecciÃ³n a `/projects/{projectId}/tasks`

### 4.5. MÃ©tricas de DesempeÃ±o

| MÃ©trica | Valor obtenido | Umbral | Estado |
| :--- | :--- | :--- | :--- |
| `loginToExplore` | 16,706.65 ms | < 20,000 ms | âœ… Aprobado |
| `taskSelectionToValidation` | 5,868.77 ms | < 90,000 ms | âœ… Aprobado |
| `validationToSubmit` | 672.01 ms | < 30,000 ms | âœ… Aprobado |

### 4.6. Salida de Consola

```text
Timings (ms): {
  loginToExplore: 16706.652000000002,
  taskSelectionToValidation: 5868.771199999996,
  validationToSubmit: 672.0126999999993
}
  âœ“  3 [chromium] â€º e2e\flows\validation-flow.spec.js:56:3 â€º Flujo de ValidaciÃ³n (funcional / usabilidad) â€º login como validador -> seleccionar tarea mapeada -> validar tarea (23.7s)
```

### 4.7. ConclusiÃ³n

El caso CP-E2E-VAL-001 se ejecutÃ³ **exitosamente** contra el backend real. El flujo completo de validaciÃ³n funcionÃ³ correctamente y todos los criterios de desempeÃ±o fueron satisfechos.

---

## 5. Flujo de AdministraciÃ³n â€” CP-E2E-ADM-001

**Responsable:** JhonAQ Â· **Fecha:** 2026-07-15 Â· **Herramienta:** Playwright (Chromium)

### 5.1. Datos de Prueba

| Campo | Valor |
| :--- | :--- |
| Usuario | `e2e_admin` |
| ID de usuario | `9999003` |
| Rol | ADMIN (role = 1) |
| AcciÃ³n | Crear proyecto nuevo importando AOI GeoJSON |

### 5.2. Caso de Prueba Ejecutado

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :--- | :--- | :--- | :--- | :--- |
| **CP-E2E-ADM-001** | Flujo completo de creaciÃ³n de proyecto con backend real: login â†’ panel manage â†’ wizard de creaciÃ³n â†’ guardar borrador. | Automatizado | âœ… Exitoso | Ninguno |

### 5.3. Resultado Esperado vs. Obtenido

| Resultado esperado | Resultado obtenido |
| :--- | :--- |
| El usuario `e2e_admin` crea un nuevo proyecto importando un AOI GeoJSON, avanza por el wizard, completa nombre y organizaciÃ³n, y guarda como borrador. El sistema redirige a `/manage/projects/{id}`. | Todas las navegaciones y verificaciones completaron sin errores. El proyecto se creÃ³ correctamente en la base de datos. |

### 5.4. Pasos Ejecutados

1. Navegar a `/authorized/?username=e2e_admin&session_token=...&redirect_to=/manage`
2. Verificar que el panel **Manage** muestra el encabezado **Projects**
3. Navegar directamente a `/manage/projects/new/`
4. Subir el archivo `test-aoi.geojson`
5. Avanzar por los pasos **Set Tasks Sizes**, **Trim Task Grid** y **Review**
6. Completar el nombre del proyecto
7. Seleccionar la organizaciÃ³n `E2E Organisation` mediante el combobox (teclado)
8. Hacer clic en **Create**
9. Verificar redirecciÃ³n a `/manage/projects/{id}`

### 5.5. MÃ©tricas de DesempeÃ±o

| MÃ©trica | Valor obtenido | Umbral | Estado |
| :--- | :--- | :--- | :--- |
| `loginToManage` | 5,436.39 ms | < 20,000 ms | âœ… Aprobado |
| `createProjectWizard` | 5,627.15 ms | < 120,000 ms | âœ… Aprobado |

### 5.6. Salida de Consola

```text
Timings (ms): {
  loginToManage: 5436.3946000000005,
  createProjectWizard: 5627.154399999999
}
  âœ“  1 [chromium] â€º e2e\flows\admin-create-project-flow.spec.js:31:3 â€º Flujo de AdministraciÃ³n (funcional / usabilidad) â€º login como admin -> panel manage -> crear proyecto -> importar AOI -> guardar borrador (13.5s)
```

### 5.7. ConclusiÃ³n

El caso CP-E2E-ADM-001 se ejecutÃ³ **exitosamente** contra el backend real. El flujo completo de creaciÃ³n de proyecto funcionÃ³ correctamente y todos los criterios de desempeÃ±o fueron satisfechos.

---

## 6. Prueba de DesempeÃ±o y Carga â€” K6

**Responsable:** Alexandra Â· **Fecha:** 2026-07-19 Â· **Herramienta:** Grafana K6
**Atributo de calidad (ISO/IEC 25010):** Eficiencia de DesempeÃ±o
**Referencia metodolÃ³gica:** Myers, "The Art of Software Testing" â€” Pruebas de EstrÃ©s y Carga

### 6.1. ConfiguraciÃ³n del Escenario

| ParÃ¡metro | Valor |
| :--- | :--- |
| Usuarios virtuales mÃ¡ximos (VUs) | 50 |
| DuraciÃ³n total | 12 minutos (3 etapas de rampa) |
| Endpoint bajo prueba | `POST /api/v2/projects/1/tasks/actions/lock-for-mapping/{taskId}/` |
| Umbral de latencia | p(95) < 2,000 ms |
| Umbral de errores | rate < 5% |

### 6.2. Resultados Obtenidos

```
â–ˆ THRESHOLDS

  http_req_duration
  âœ“ 'p(95)<2000' p(95)=1.76s

  http_req_failed
  âœ“ 'rate<0.05' rate=0.04%

â–ˆ TOTAL RESULTS

  checks_total.......: 9330    12.845491/s
  checks_succeeded...: 100.00% 9330 out of 9330
  checks_failed......: 0.00%   0 out of 9330

  âœ“ GET tasks status is 200
  âœ“ POST lock: respuesta valida del sistema

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

![Resultados K6 en consola â€” 100% checks OK, p(95)=1.76s](/tests-docs/03-ejecucion-de-pruebas/sistema/k6-results.jpg)

### 6.4. AnÃ¡lisis de ContenciÃ³n Transaccional

El desglose de respuestas HTTP demuestra que el backend maneja la concurrencia extrema con integridad:

| CÃ³digo | Conteo | InterpretaciÃ³n |
| :--- | :--- | :--- |
| `lock_200_ok` â€” 1,033 | 1,033 bloqueos exitosos | Un usuario adquiriÃ³ la tarea correctamente |
| `lock_403_conflict_or_state` â€” 3,632 | Rechazos controlados | El sistema rechazÃ³ correctamente a usuarios tardÃ­os: **Race Condition prevenida** |
| Errores reales | 5 de 10,363 peticiones (0.04%) | Dentro del umbral aceptable |

> El alto nÃºmero de respuestas 403 **no es un error**: demuestra que el sistema protege correctamente la integridad de los datos â€” dos usuarios nunca pueden apropiarse de la misma tarea simultÃ¡neamente.

### 6.5. Hallazgo de OptimizaciÃ³n Documentado

Durante las rondas de prueba se identificÃ³ un cuello de botella crÃ­tico:

| ID | DescripciÃ³n | Causa RaÃ­z | ResoluciÃ³n |
| :--- | :--- | :--- | :--- |
| **DEF-SYS-PERF-001** | El sistema colapsaba con 50 VUs cuando `DB_MAX_CONNECTIONS=8` | La operaciÃ³n `unlock` dispara un recÃ¡lculo sÃ­ncrono de medallas de usuario, abriendo una segunda conexiÃ³n de DB simultÃ¡neamente | `DB_MAX_CONNECTIONS` elevado a 30 en entorno de pruebas |

### 6.6. ConclusiÃ³n

**APROBADO.** El sistema soporta 50 usuarios concurrentes intentando bloquear tareas simultÃ¡neamente, con una tasa de error del 0.04% y respondiendo el 95% de las peticiones en menos de 1.76 segundos â€” dentro del umbral de aceptaciÃ³n de 2 segundos definido en el Plan de Pruebas.

---

## 7. Prueba de Seguridad â€” SonarQube

**Responsable:** Alexandra Â· **Fecha:** 2026-07-19
**Herramientas:** SonarCloud (SAST/SCA) + Gitleaks (Secret Scanning)
**Atributo de calidad (ISO/IEC 25010):** Seguridad
**IntegraciÃ³n:** GitHub Actions CI/CD (`seguridad-sonarqube.yml`) â€” se ejecuta automÃ¡ticamente en cada push a `develop`

### 7.1. Estrategia de Prueba

| Capa | Herramienta | Tipo | Objetivo |
| :--- | :--- | :--- | :--- |
| 1 | **Gitleaks** | Secret Scanning | Detectar tokens, contraseÃ±as o claves API expuestas |
| 2 | **SonarCloud** | SAST + SCA | Detectar vulnerabilidades, bugs crÃ­ticos y deuda tÃ©cnica |

### 7.2. Vista General â€” OrganizaciÃ³n en SonarCloud

El pipeline de CI/CD procesÃ³ exitosamente las **76,000 lÃ­neas de cÃ³digo** del repositorio real.

![Vista general de la organizaciÃ³n en SonarCloud mostrando el proyecto analizado](/tests-docs/03-ejecucion-de-pruebas/sistema/sonar-01-projects-overview.jpg)

### 7.3. Dashboard del Proyecto â€” Estado de Calidad

![Dashboard de estado del proyecto: Quality Gate Failed con 1,595 issues totales](/tests-docs/03-ejecucion-de-pruebas/sistema/sonar-02-project-dashboard.jpg)

**InterpretaciÃ³n del Quality Gate:**
> El Quality Gate indica **Failed**. Esto es el resultado **esperado y buscado** de una prueba de seguridad efectiva: la herramienta identificÃ³ deuda de seguridad real en el cÃ³digo. Una prueba que no encuentra nada en 76k lÃ­neas de cÃ³digo real habrÃ­a sido inefectiva.

| MÃ©trica Dashboard | Valor |
| :--- | :--- |
| Quality Gate | âŒ Failed (1 condiciÃ³n) |
| Open Issues totales | 1,595 |
| Duplicaciones | 1.2% |
| Coverage | 0.0% (no se enviÃ³ reporte de cobertura â€” esperado) |

### 7.4. Snapshot de Seguridad

![Panel de seguridad: Rating E, 9 vulnerabilidades por severidad](/tests-docs/03-ejecucion-de-pruebas/sistema/sonar-03-security-snapshot.jpg)

| MÃ©trica de Seguridad | Valor |
| :--- | :--- |
| **Security Rating** | E (CrÃ­tico) |
| **Security Issues detectados** | 9 vulnerabilidades activas |
| Blocker | 11% |
| High | 11% |
| Medium | 56% |
| Low | 22% |
| Security Hotspots Reviewed | 100% âœ… |

### 7.5. Snapshot de Confiabilidad y Mantenibilidad

![Panel de confiabilidad (234 bugs) y mantenibilidad (1,485 code smells, rating A)](/tests-docs/03-ejecucion-de-pruebas/sistema/sonar-04-reliability-maintainability.jpg)

| MÃ©trica | Valor | InterpretaciÃ³n |
| :--- | :--- | :--- |
| **Reliability Rating** | E | 234 bugs potenciales identificados |
| Reliability Issues | 234 | MayorÃ­a Medium (56%) y Low (32%) |
| **Maintainability Rating** | A âœ… | Excelente para un proyecto de 76k lÃ­neas |
| Maintainability Issues | 1,485 | Baja densidad de deuda tÃ©cnica |

### 7.6. AnÃ¡lisis

**Â¿Por quÃ© el Quality Gate fallÃ³?** Porque SonarQube encontrÃ³ 9 vulnerabilidades de seguridad activas con al menos una de severidad Blocker. Este es exactamente el objetivo de una prueba SAST: exponer la deuda de seguridad existente en el sistema real.

**Punto positivo:** La calificaciÃ³n de **Mantenibilidad A** es notable. Para 76,000 lÃ­neas de cÃ³digo real de un sistema open-source de producciÃ³n, solo 1,485 code smells representan una densidad muy baja de deuda tÃ©cnica.

**Gitleaks:** No detectÃ³ secretos ni credenciales expuestas en el repositorio. âœ…

### 7.7. ConclusiÃ³n

| Aspecto | Resultado |
| :--- | :--- |
| Pipeline CI/CD integrado | âœ… Funciona en cada push a `develop` |
| Secret Scanning (Gitleaks) | âœ… NingÃºn secreto expuesto |
| AnÃ¡lisis SAST ejecutado | âœ… Exitoso sobre 76k lÃ­neas |
| Vulnerabilidades detectadas | 9 issues (requieren plan de remediaciÃ³n) |
| Objetivo de la prueba | âœ… **EJECUTADO** â€” Hallazgos documentados para backlog |

---

## 8. Resumen de Resultados y Conclusiones

### 8.1. Tabla de Resultados Globales

| ID Caso | Tipo | Responsable | Criterio | Resultado |
| :--- | :--- | :--- | :--- | :--- |
| CP-E2E-MAP-001 | E2E Funcional | Jhonatan | Todos los pasos exitosos + mÃ©tricas < umbral | âœ… APROBADO |
| CP-E2E-VAL-001 | E2E Funcional | Jhonatan | Todos los pasos exitosos + mÃ©tricas < umbral | âœ… APROBADO |
| CP-E2E-ADM-001 | E2E Funcional | Jhonatan | Todos los pasos exitosos + mÃ©tricas < umbral | âœ… APROBADO |
| PERF-K6-001 | DesempeÃ±o/Carga | Alexandra | p(95) < 2000ms Â· rate < 5% | âœ… APROBADO |
| SEC-SONAR-001 | Seguridad SAST | Alexandra | Pipeline ejecutado, hallazgos documentados | âœ… EJECUTADO |

### 8.2. Defectos Encontrados

| ID | Tipo | DescripciÃ³n | Estado |
| :--- | :--- | :--- | :--- |
| DEF-SYS-PERF-001 | Cuello de botella | `DB_MAX_CONNECTIONS=8` insuficiente para 50 VUs concurrentes | âœ… Resuelto (elevado a 30) |
| DEF-SYS-SEC-001 a 009 | Seguridad | 9 vulnerabilidades SAST detectadas por SonarCloud | ðŸ”´ Pendiente remediaciÃ³n en sprints futuros |

### 8.3. ConclusiÃ³n Final

El sistema Tasking Manager demuestra un nivel de calidad **suficiente para su estado actual de desarrollo**:
- Los tres flujos crÃ­ticos de negocio (Mapeo, ValidaciÃ³n, AdministraciÃ³n) funcionan correctamente de extremo a extremo.
- El sistema soporta carga real de 50 usuarios concurrentes con latencias aceptables.
- Se identificaron 9 vulnerabilidades de seguridad que deben priorizarse en el backlog.

Se aprueba la ejecuciÃ³n de las Pruebas de Sistema para los mÃ³dulos evaluados.


