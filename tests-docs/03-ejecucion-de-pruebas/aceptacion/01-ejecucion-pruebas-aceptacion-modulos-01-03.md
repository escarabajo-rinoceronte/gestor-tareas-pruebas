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
| **CA-ACP-01** | MOD-01 | `/login` -> `/authorized` | Aprobado | El usuario accede correctamente a la plataforma y visualiza su sesión activa. | El usuario completó el inicio de sesión y accedió a la vista autenticada de la plataforma. | <a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-01-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-01-01.png" width="320px" alt="CA-ACP-01 evidencia"></a> |
| **CA-ACP-02** | MOD-01 | `/login` | Aprobado | El usuario permanece fuera de la plataforma y no se crea una sesión local. | El usuario canceló la autorización y la plataforma mantuvo el estado no autenticado. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-02-01.png` |
| **CA-ACP-03** | MOD-01 | Barra superior / perfil | Aprobado | El usuario regresa a la vista pública después de cerrar sesión. | El usuario cerró sesión y volvió correctamente a la vista pública de la aplicación. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-03-01.png` |
| **CA-ACP-04** | MOD-01 | `/projects/:id` | Aprobado | El usuario es redirigido a autenticación antes de acceder al proyecto restringido. | El usuario no autenticado fue redirigido a autenticación al intentar ingresar al proyecto restringido. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-04-01.png` |
| **CA-ACP-05** | MOD-01 | `/projects/:id/tasks` | Aprobado | Antes de aceptar, el usuario no puede contribuir; después de aceptar, la contribución queda habilitada. | El usuario encontró bloqueada la contribución antes de aceptar la licencia y pudo habilitarla después de aceptar los términos. | <a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-05-01_1.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-05-01_1.jpeg" width="320px" alt="CA-ACP-05 evidencia 1"></a><br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-05-01_2.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-05-01_2.jpeg" width="320px" alt="CA-ACP-05 evidencia 2"></a> |
| **CA-ACP-06** | MOD-01 | `/settings` | Aprobado | El usuario guarda correctamente los datos válidos y recibe validación ante entradas inválidas. | El usuario pudo guardar cambios válidos en su perfil y recibió validación al ingresar datos inválidos. | <a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-06-01_1.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-06-01_1.jpeg" width="320px" alt="CA-ACP-06 evidencia 1"></a><br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-06-01_2.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-06-01_2.jpeg" width="320px" alt="CA-ACP-06 evidencia 2"></a> |
| **CA-ACP-07** | MOD-02 | `/explore` | Aprobado | El usuario visualiza correctamente el catálogo base de proyectos. | El usuario ingresó a exploración y visualizó el catálogo general de proyectos. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-07-01.png` |
| **CA-ACP-08** | MOD-02 | `/explore` | Aprobado | El usuario visualiza solo proyectos en estado `Activo`. | El usuario aplicó el filtro y visualizó únicamente proyectos activos. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-08-01.png` |
| **CA-ACP-09** | MOD-02 | `/explore` | Aprobado | El usuario obtiene resultados acordes con la combinación aplicada o una vista vacía controlada. | El usuario combinó filtros y obtuvo resultados coherentes con la selección realizada, incluyendo el caso sin coincidencias. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-09-01.png` |
| **CA-ACP-10** | MOD-02 | `/explore` | Aprobado | El usuario obtiene resultados para búsquedas válidas y mensajes controlados ante entradas inválidas. | El usuario realizó búsquedas válidas e ingresó entradas no válidas sin afectar la estabilidad de la interfaz. | <a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-10_1.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-10_1.jpeg" width="320px" alt="CA-ACP-10 evidencia 1"></a><br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-10-01_2.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-10-01_2.jpeg" width="320px" alt="CA-ACP-10 evidencia 2"></a> |
| **CA-ACP-11** | MOD-02 | `/explore`, `/projects/:id` | Aprobado | El proyecto privado permanece oculto para quien no tiene permiso y visible para quien sí lo posee. | El usuario no autorizado no pudo visualizar el proyecto privado y el usuario autorizado sí pudo acceder a él. | <a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-11-01_1.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-11-01_1.jpeg" width="320px" alt="CA-ACP-11 evidencia 1"></a><br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-11-01_2.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-11-01_2.jpeg" width="320px" alt="CA-ACP-11 evidencia 2"></a> |
| **CA-ACP-12** | MOD-03 | `/projects/:id/tasks` -> `/projects/:id/map?editor=ID` | Aprobado | El usuario puede iniciar el mapeo de una tarea disponible y acceder al editor `iD`. | El usuario seleccionó una tarea disponible e inició correctamente el mapeo en el editor `iD`. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-12-01.png` |
| **CA-ACP-13** | MOD-03 | `/projects/:id/map?editor=JOSM` | Aprobado | El usuario recibe una notificación sobre la indisponibilidad de `JOSM` y conserva el flujo iniciado. | El usuario fue informado de la indisponibilidad de `JOSM` sin perder el contexto de la tarea. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-13-01.png` |
| **CA-ACP-14** | MOD-03 | `/projects/:id/tasks` -> `/projects/:id/map` | Rechazado | El usuario no puede iniciar el mapeo hasta aceptar la licencia correspondiente. | El usuario pudo avanzar en el flujo de mapeo sin que el bloqueo preventivo por licencia se aplicara correctamente. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-14-01.png` |
| **CA-ACP-15** | MOD-03 | `/projects/:id/tasks` | Aprobado | El usuario no puede bloquear la tarea cuando no cumple las reglas de negocio definidas. | El usuario no pudo bloquear tareas en escenarios con concurrencia, estado inválido o permisos insuficientes. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-15-01.png` |
| **CA-ACP-16** | MOD-03 | `/projects/:id/map` | Aprobado | La tarea queda registrada como completada después de que el usuario la finaliza. | El usuario finalizó la tarea y esta quedó registrada como completada. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-16-01.png` |
| **CA-ACP-17** | MOD-03 | `/projects/:id/map` | Aprobado | La tarea vuelve a estar disponible después de que el usuario la libera sin completarla. | El usuario liberó la tarea sin completarla y esta volvió a quedar disponible. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-17-01.png` |
| **CA-ACP-18** | MOD-03 | `/projects/:id/tasks` | Aprobado | El usuario no visualiza controles de envío cuando no puede finalizar la tarea. | El usuario no visualizó la opción `Submit Task` en contextos no válidos para finalizar la tarea. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-18-01.png` |
| **CA-ACP-19** | MOD-03 | `/projects/:id/tasks`, `/projects/:id/map` | Aprobado | La opción de dividir tarea solo está disponible cuando el contexto lo permite. | El usuario solo pudo visualizar y usar la división de tarea en un contexto válido. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-19-01.png` |
| **CA-ACP-20** | MOD-03 | `/projects/:id/map` | Aprobado | El usuario puede extender o liberar la sesión solo cuando el contexto correspondiente lo permite. | El usuario pudo extender o liberar la sesión de mapeo únicamente en los contextos permitidos. | `/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-20-01.png` |

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
