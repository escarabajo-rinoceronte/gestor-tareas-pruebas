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

## 2. Ejecución de casos de aceptación

### 2.1. CA-ACP-01

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-01` |
| **Módulo** | `MOD-01` |
| **Ruta** | `/login` -> `/authorized` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario accede correctamente a la plataforma y visualiza su sesión activa. | El usuario completó el inicio de sesión y accedió a la vista autenticada de la plataforma. |

| Evidencia |
| :-- |
| Inicio de sesión exitoso<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-01-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-01-01.png" width="800px" alt="CA-ACP-01 - Inicio de sesión exitoso"></a><br>Acceso correcto a la vista autenticada de la plataforma. |

---

### 2.2. CA-ACP-02

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-02` |
| **Módulo** | `MOD-01` |
| **Ruta** | `/login` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario permanece fuera de la plataforma y no se crea una sesión local. | El usuario canceló la autorización y la plataforma mantuvo el estado no autenticado. |

| Evidencia |
| :-- |
| Cancelación de autorización<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-02-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-02-01.png" width="800px" alt="CA-ACP-02 - Cancelación de autorización"></a><br>La plataforma retorna al estado público sin crear sesión local. |

---

### 2.3. CA-ACP-03

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-03` |
| **Módulo** | `MOD-01` |
| **Ruta** | Barra superior / perfil |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario regresa a la vista pública después de cerrar sesión. | El usuario cerró sesión y volvió correctamente a la vista pública de la aplicación. |

| Evidencia |
| :-- |
| Cierre de sesión correcto<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-03-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-03-01.png" width="800px" alt="CA-ACP-03 - Cierre de sesión correcto"></a><br>La aplicación retorna a la interfaz pública después del cierre de sesión. |

---

### 2.4. CA-ACP-04

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-04` |
| **Módulo** | `MOD-01` |
| **Ruta** | `/projects/:id` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario es redirigido a autenticación antes de acceder al proyecto restringido. | El usuario no autenticado fue redirigido a autenticación al intentar ingresar al proyecto restringido. |

| Evidencia |
| :-- |
| Redirección por acceso restringido<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-04-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-04-01.png" width="800px" alt="CA-ACP-04 - Redirección por acceso restringido"></a><br>El acceso al proyecto queda protegido para usuarios no autenticados. |

---

### 2.5. CA-ACP-05

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-05` |
| **Módulo** | `MOD-01` |
| **Ruta** | `/projects/:id/tasks` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Antes de aceptar, el usuario no puede contribuir; después de aceptar, la contribución queda habilitada. | El usuario encontró bloqueada la contribución antes de aceptar la licencia y pudo habilitarla después de aceptar los términos. |

| Evidencia |
| :-- |
| Bloqueo previo por licencia<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-05-01_1.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-05-01_1.jpeg" width="800px" alt="CA-ACP-05 - Bloqueo previo por licencia"></a><br>La contribución permanece bloqueada mientras el usuario no acepta la licencia requerida. |

| Evidencia |
| :-- |
| Habilitación posterior a la aceptación<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-05-01_2.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-05-01_2.jpeg" width="800px" alt="CA-ACP-05 - Habilitación posterior a la aceptación"></a><br>La contribución queda habilitada después de aceptar los términos del proyecto. |

---

### 2.6. CA-ACP-06

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-06` |
| **Módulo** | `MOD-01` |
| **Ruta** | `/settings` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario guarda correctamente los datos válidos y recibe validación ante entradas inválidas. | El usuario pudo guardar cambios válidos en su perfil y recibió validación al ingresar datos inválidos. |

| Evidencia |
| :-- |
| Validación de entradas inválidas<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-06-01_1.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-06-01_1.jpeg" width="800px" alt="CA-ACP-06 - Validación de entradas inválidas"></a><br>El formulario responde con validaciones visibles ante datos inválidos. |

| Evidencia |
| :-- |
| Guardado de datos válidos<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-06-01_2.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-06-01_2.jpeg" width="800px" alt="CA-ACP-06 - Guardado de datos válidos"></a><br>La información válida del perfil se guarda correctamente. |

---

### 2.7. CA-ACP-07

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-07` |
| **Módulo** | `MOD-02` |
| **Ruta** | `/explore` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario visualiza correctamente el catálogo base de proyectos. | El usuario ingresó a exploración y visualizó el catálogo general de proyectos. |

| Evidencia |
| :-- |
| Catálogo inicial de proyectos<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-07-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-07-01.png" width="800px" alt="CA-ACP-07 - Catálogo inicial de proyectos"></a><br>La vista de exploración muestra correctamente el catálogo general. |

---

### 2.8. CA-ACP-08

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-08` |
| **Módulo** | `MOD-02` |
| **Ruta** | `/explore` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario visualiza solo proyectos en estado `Activo`. | El usuario aplicó el filtro y visualizó únicamente proyectos activos. |

| Evidencia |
| :-- |
| Filtro por proyectos activos<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-08-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-08-01.png" width="800px" alt="CA-ACP-08 - Filtro por proyectos activos"></a><br>La interfaz muestra únicamente proyectos en estado activo. |

---

### 2.9. CA-ACP-09

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-09` |
| **Módulo** | `MOD-02` |
| **Ruta** | `/explore` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario obtiene resultados acordes con la combinación aplicada o una vista vacía controlada. | El usuario combinó filtros y obtuvo resultados coherentes con la selección realizada, incluyendo el caso sin coincidencias. |

| Evidencia |
| :-- |
| Combinación de filtros aplicada<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-09-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-09-01.png" width="800px" alt="CA-ACP-09 - Combinación de filtros aplicada"></a><br>La interfaz responde de forma coherente a la combinación de filtros seleccionada. |

---

### 2.10. CA-ACP-10

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-10` |
| **Módulo** | `MOD-02` |
| **Ruta** | `/explore` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario obtiene resultados para búsquedas válidas y mensajes controlados ante entradas inválidas. | El usuario realizó búsquedas válidas e ingresó entradas no válidas sin afectar la estabilidad de la interfaz. |

| Evidencia |
| :-- |
| Búsqueda válida de proyectos<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-10_1.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-10_1.jpeg" width="800px" alt="CA-ACP-10 - Búsqueda válida de proyectos"></a><br>La interfaz devuelve resultados coherentes para una búsqueda válida. |

| Evidencia |
| :-- |
| Manejo controlado de entrada inválida<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-10-01_2.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-10-01_2.jpeg" width="800px" alt="CA-ACP-10 - Manejo controlado de entrada inválida"></a><br>La búsqueda mantiene la estabilidad de la interfaz ante una entrada no válida. |

---

### 2.11. CA-ACP-11

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-11` |
| **Módulo** | `MOD-02` |
| **Ruta** | `/explore`, `/projects/:id` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El proyecto privado permanece oculto para quien no tiene permiso y visible para quien sí lo posee. | El usuario no autorizado no pudo visualizar el proyecto privado y el usuario autorizado sí pudo acceder a él. |

| Evidencia |
| :-- |
| Proyecto privado oculto para usuario no autorizado<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-11-01_1.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-11-01_1.jpeg" width="800px" alt="CA-ACP-11 - Proyecto privado oculto para usuario no autorizado"></a><br>El proyecto privado no es visible para un usuario sin permisos. |

| Evidencia |
| :-- |
| Proyecto privado visible para usuario autorizado<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-11-01_2.jpeg"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-11-01_2.jpeg" width="800px" alt="CA-ACP-11 - Proyecto privado visible para usuario autorizado"></a><br>El proyecto privado se muestra correctamente cuando el usuario sí cuenta con autorización. |

---

### 2.12. CA-ACP-12

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-12` |
| **Módulo** | `MOD-03` |
| **Ruta** | `/projects/:id/tasks` -> `/projects/:id/map?editor=ID` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario puede iniciar el mapeo de una tarea disponible y acceder al editor `iD`. | El usuario seleccionó una tarea disponible e inició correctamente el mapeo en el editor `iD`. |

| Evidencia |
| :-- |
| Inicio de mapeo con editor iD<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-12-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-12-01.png" width="800px" alt="CA-ACP-12 - Inicio de mapeo con editor iD"></a><br>La tarea disponible se abre correctamente en el editor web seleccionado. |

---

### 2.13. CA-ACP-13

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-13` |
| **Módulo** | `MOD-03` |
| **Ruta** | `/projects/:id/map?editor=JOSM` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario recibe una notificación sobre la indisponibilidad de `JOSM` y conserva el flujo iniciado. | El usuario fue informado de la indisponibilidad de `JOSM` sin perder el contexto de la tarea. |

| Evidencia |
| :-- |
| Notificación de indisponibilidad de JOSM<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-13-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-13-01.png" width="800px" alt="CA-ACP-13 - Notificación de indisponibilidad de JOSM"></a><br>La interfaz informa el problema sin perder el contexto de trabajo. |

---

### 2.14. CA-ACP-14

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-14` |
| **Módulo** | `MOD-03` |
| **Ruta** | `/projects/:id/tasks` -> `/projects/:id/map` |
| **Estado** | `Rechazado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario no puede iniciar el mapeo hasta aceptar la licencia correspondiente. | El usuario pudo avanzar en el flujo de mapeo sin que el bloqueo preventivo por licencia se aplicara correctamente. |

| Evidencia |
| :-- |
| Incumplimiento del bloqueo por licencia<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-14-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-14-01.png" width="800px" alt="CA-ACP-14 - Incumplimiento del bloqueo por licencia"></a><br>La evidencia muestra que el flujo avanzó sin aplicar correctamente la restricción previa de licencia. |

---

### 2.15. CA-ACP-15

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-15` |
| **Módulo** | `MOD-03` |
| **Ruta** | `/projects/:id/tasks` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario no puede bloquear la tarea cuando no cumple las reglas de negocio definidas. | El usuario no pudo bloquear tareas en escenarios con concurrencia, estado inválido o permisos insuficientes. |

| Evidencia |
| :-- |
| Restricción de bloqueo inválido<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-15-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-15-01.png" width="800px" alt="CA-ACP-15 - Restricción de bloqueo inválido"></a><br>El sistema deniega el bloqueo cuando no se cumplen las condiciones permitidas. |

---

### 2.16. CA-ACP-16

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-16` |
| **Módulo** | `MOD-03` |
| **Ruta** | `/projects/:id/map` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La tarea queda registrada como completada después de que el usuario la finaliza. | El usuario finalizó la tarea y esta quedó registrada como completada. |

| Evidencia |
| :-- |
| Finalización correcta de tarea<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-16-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-16-01.png" width="800px" alt="CA-ACP-16 - Finalización correcta de tarea"></a><br>La tarea pasa al estado esperado después de la finalización. |

---

### 2.17. CA-ACP-17

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-17` |
| **Módulo** | `MOD-03` |
| **Ruta** | `/projects/:id/map` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La tarea vuelve a estar disponible después de que el usuario la libera sin completarla. | El usuario liberó la tarea sin completarla y esta volvió a quedar disponible. |

| Evidencia |
| :-- |
| Liberación de tarea sin completar<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-17-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-17-01.png" width="800px" alt="CA-ACP-17 - Liberación de tarea sin completar"></a><br>La tarea retorna correctamente al estado disponible. |

---

### 2.18. CA-ACP-18

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-18` |
| **Módulo** | `MOD-03` |
| **Ruta** | `/projects/:id/tasks` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario no visualiza controles de envío cuando no puede finalizar la tarea. | El usuario no visualizó la opción `Submit Task` en contextos no válidos para finalizar la tarea. |

| Evidencia |
| :-- |
| Ocultamiento de controles de envío<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-18-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-18-01.png" width="800px" alt="CA-ACP-18 - Ocultamiento de controles de envío"></a><br>La interfaz oculta correctamente la acción de envío en contextos no válidos. |

---

### 2.19. CA-ACP-19

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-19` |
| **Módulo** | `MOD-03` |
| **Ruta** | `/projects/:id/tasks`, `/projects/:id/map` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La opción de dividir tarea solo está disponible cuando el contexto lo permite. | El usuario solo pudo visualizar y usar la división de tarea en un contexto válido. |

| Evidencia |
| :-- |
| Disponibilidad condicionada de split task<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-19-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-19-01.png" width="800px" alt="CA-ACP-19 - Disponibilidad condicionada de split task"></a><br>La división de tarea solo se habilita cuando el contexto lo permite. |

---

### 2.20. CA-ACP-20

| Campo | Valor |
| :-- | :-- |
| **ID** | `CA-ACP-20` |
| **Módulo** | `MOD-03` |
| **Ruta** | `/projects/:id/map` |
| **Estado** | `Aprobado` |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El usuario puede extender o liberar la sesión solo cuando el contexto correspondiente lo permite. | El usuario pudo extender o liberar la sesión de mapeo únicamente en los contextos permitidos. |

| Evidencia |
| :-- |
| Gestión de sesión de mapeo<br><a href="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-20-01.png"><img src="/tests-docs/03-ejecucion-de-pruebas/aceptacion/img/CA-ACP-20-01.png" width="800px" alt="CA-ACP-20 - Gestión de sesión de mapeo"></a><br>La interfaz permite extender o liberar la sesión solo en los contextos válidos. |

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
