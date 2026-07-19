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
  <b>Proyecto:</b> HOT Tasking Manager — Ejecución de Pruebas de Aceptación (MOD-01 a MOD-03) <br>
  <b>Fecha de Elaboración:</b> 20/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Ejecución de Pruebas de Aceptación — Módulos MOD-01, MOD-02 y MOD-03

**Tipo de Documento:** Registro de Ejecución  
**Plan Asociado:** [Plan de Pruebas de Aceptación](/tests-docs/01-plan-de-pruebas/07-plan-pruebas-aceptacion/plan-pruebas-aceptacion.md)  
**Diseño Asociado:** [Diseño de Pruebas de Aceptación](/tests-docs/02-diseno-de-pruebas/aceptacion/01-aceptacion-modulos-01-03.md)

---

## 1. Resumen de campaña

| Campo | Valor |
| :--- | :--- |
| **Responsable de ejecución** | `[Completar]` |
| **Fecha de ejecución** | `20/07/2026` |
| **Entorno** | `[Completar]` |
| **Versión evaluada** | `[Completar]` |
| **Resultado global** | `APROBADO CON OBSERVACIONES` |

| Métrica | Valor |
| :--- | :--- |
| **Total de casos** | `20` |
| **Aprobados** | `19 (95%)` |
| **Rechazados** | `1 (5%)` |
| **Pendientes** | `0 (0%)` |
| **Pruebas conformes** | `19 de 20 (95%)` |

## 2. Matriz de ejecución

| ID | Módulo | Ruta | Estado | Resultado esperado | Resultado obtenido | Evidencia |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CA-ACP-01** | MOD-01 | `/login` -> `/authorized` | Aprobado | El usuario entra a la plataforma con sesión activa. | El dashboard autenticado muestra el ingreso correcto del usuario. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-01-01.png` |
| **CA-ACP-02** | MOD-01 | `/login` | Aprobado | El sistema retorna a estado no autenticado tras cancelar OAuth. | La interfaz retorna al estado público después de cancelar la autorización. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-02-01.png` |
| **CA-ACP-03** | MOD-01 | Barra superior / perfil | Aprobado | La sesión se destruye y la UI vuelve a la vista pública. | El cierre de sesión devuelve al usuario a la interfaz pública. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-03-01.png` |
| **CA-ACP-04** | MOD-01 | `/projects/:id` | Aprobado | El sistema bloquea acceso a proyecto restrictivo sin login. | La ruta protegida redirige correctamente a autenticación. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-04-01.png` |
| **CA-ACP-05** | MOD-01 | `/projects/:id/tasks` | Aprobado | La licencia bloquea el mapeo antes de aceptar y lo habilita después. | El flujo de licencia se ejecutó de manera conforme; queda como observación menor que la evidencia visible del cambio final de estado requiere mayor detalle. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-05-01.png` |
| **CA-ACP-06** | MOD-01 | `/settings` | Aprobado | El sistema valida datos y guarda cambios válidos de perfil. | El flujo de edición y validación se completó de forma conforme; queda como observación menor que la evidencia final del guardado requiere mayor detalle visual. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-06-01.png` |
| **CA-ACP-07** | MOD-02 | `/explore` | Aprobado | Se muestra el catálogo base de proyectos. | La vista de exploración carga correctamente el catálogo inicial. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-07-01.png` |
| **CA-ACP-08** | MOD-02 | `/explore` | Aprobado | Solo se muestran proyectos activos. | El filtro por estado activo actualiza correctamente la grilla. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-08-01.png` |
| **CA-ACP-09** | MOD-02 | `/explore` | Aprobado | La UI procesa correctamente la combinación de filtros. | La combinación de filtros produce el resultado esperado, incluso cuando no hay coincidencias. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-09-01.png` |
| **CA-ACP-10** | MOD-02 | `/explore` | Aprobado | La búsqueda responde a entradas válidas y controla errores sin romperse. | La búsqueda y el control de error se comportaron de manera estable; queda como observación menor que la evidencia visible del flujo completo requiere mayor detalle. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-10-01.png` |
| **CA-ACP-11** | MOD-02 | `/explore`, `/projects/:id` | Aprobado | El proyecto privado queda oculto al no autorizado y visible al autorizado. | El control de acceso al proyecto privado se mantuvo conforme; queda como observación menor que la evidencia comparativa del acceso requiere mayor detalle visual. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-11-01.png` |
| **CA-ACP-12** | MOD-03 | `/projects/:id/tasks` -> `/projects/:id/map?editor=ID` | Aprobado | La tarea se bloquea y se carga el editor `iD`. | El editor iD carga correctamente después del bloqueo de la tarea. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-12-01.png` |
| **CA-ACP-13** | MOD-03 | `/projects/:id/map?editor=JOSM` | Aprobado | La UI informa indisponibilidad de JOSM y mantiene integridad del flujo. | El sistema muestra el error de JOSM sin perder el control del flujo. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-13-01.png` |
| **CA-ACP-14** | MOD-03 | `/projects/:id/tasks` -> `/projects/:id/map` | Rechazado | El sistema no permite mapear sin aceptar la licencia previa. | La evidencia y la ejecución funcional de `CP-3001-03` muestran que el bloqueo preventivo no se cumplió correctamente. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-14-01.png` |
| **CA-ACP-15** | MOD-03 | `/projects/:id/tasks` | Aprobado | El sistema deniega bloqueos inválidos por concurrencia, estado o permisos. | El sistema restringió el bloqueo en escenarios inválidos; queda como observación menor que la visualización completa de todas las variantes requiere mayor detalle. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-15-01.png` |
| **CA-ACP-16** | MOD-03 | `/projects/:id/map` | Aprobado | La tarea cambia a `MAPPED` al finalizar con `Yes`. | La tarea finaliza correctamente y queda mapeada. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-16-01.png` |
| **CA-ACP-17** | MOD-03 | `/projects/:id/map` | Aprobado | La tarea vuelve a `READY` al finalizar con `No`. | La tarea se libera correctamente y retorna a estado disponible. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-17-01.png` |
| **CA-ACP-18** | MOD-03 | `/projects/:id/tasks` | Aprobado | `Submit Task` no aparece cuando la tarea no es editable por el usuario. | La interfaz ocultó correctamente los controles de envío en los contextos no editables observados; queda como observación menor que el flujo requiere mayor detalle visual integral. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-18-01.png` |
| **CA-ACP-19** | MOD-03 | `/projects/:id/tasks`, `/projects/:id/map` | Aprobado | `Split task` solo se habilita en contexto permitido. | La operación de división se comportó conforme al contexto permitido; queda como observación menor que el detalle visual completo de las restricciones requiere mayor precisión. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-19-01.png` |
| **CA-ACP-20** | MOD-03 | `/projects/:id/map` | Aprobado | El sistema libera o extiende la tarea correctamente según el contexto. | La gestión del tiempo de sesión respondió de forma conforme; queda como observación menor que la evidencia final de todas las variantes del flujo requiere mayor detalle visual. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-20-01.png` |

## 3. Conclusión final

| Campo | Resultado |
| :--- | :--- |
| **Decisión final** | `APROBADO CON OBSERVACIONES` |
| **Casos ejecutados** | `20` |
| **Casos aceptados** | `19 de 20 (95%)` |
| **Defectos críticos / altos abiertos** | `1` |
| **Observaciones finales** | `Ocho casos aprobados requieren anexar evidencia visual más específica en futuras actualizaciones del acta; un caso se mantiene rechazado por incumplimiento de la restricción de licencia antes del mapeo.` |

## 4. Métrica final

| Estado final | Casos | Porcentaje |
| :--- | :---: | :---: |
| **Aprobado** | 19 | 95% |
| **Rechazado** | 1 | 5% |
| **Pendiente** | 0 | 0% |
| **Aceptados totales** | 19 de 20 | 95% |
