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
  <b>Proyecto:</b> HOT Tasking Manager — EjecuciÃ³n de casos de pruebas del MOD-03: EjecuciÃ³n de Mapeo (Tasking) <br>
  <b>Fecha de Elaboración:</b> 23/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# EjecuciÃ³n de casos de pruebas del MOD-03: EjecuciÃ³n de Mapeo (Tasking)

## Resumen de EjecuciÃ³n (MÃ©tricas)

| MÃ©trica | Valor |
|---|---|
| **Casos preexistentes** | 0 |
| **Nuevos casos creados** | 25 |
| **Total de casos diseÃ±ados** | 25 |
| **Casos ejecutados con evidencia** | 25 (100%) |
| **Casos exitosos (PASS)** | 24 (96%) |
| **Casos fallidos (FAIL)** | 1 (4%) |
| **Defectos reportados** | 1 (Issue pendiente) |

---

### 1.1. EjecuciÃ³n de CP-3001-01

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3001-01** | Validar el bloqueo de una tarea en estado `READY` por un usuario con nivel adecuado, licencia aceptada y sin bloqueos previos, seleccionando el editor web `iD`. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La tarea cambia a estado `LOCKED_FOR_MAPPING`. La interfaz de usuario carga correctamente el iframe del editor iD embebido en la plataforma. | La tarea cambia a `LOCKED_FOR_MAPPING` y la UI carga correctamente el entorno del editor iD integrado sin errores en consola. |

| Evidencia |
| :-- |
| Tarea bloqueada en la interfaz<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3001-01-tarea-bloqueada.png" width="800px" alt="CP-3001-01 - Tarea marcada como LOCKED_FOR_MAPPING"></a><br>Captura de la tarea bloqueada (candado) y que el usuario actual es el titular del bloqueo de la tarea debido a la opciÃ³n `Reanudar Mapeo` y colo rojo del candado. |
| Editor iD cargado correctamente<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3001-01-editor-id-cargado.png" width="800px" alt="CP-3001-01 - Iframe del editor iD desplegado"></a><br>Captura del mapa satelital renderizado dentro de los lÃ­mites del Bounding Box (BBOX) de la tarea seleccionada. |

---

### 1.2. EjecuciÃ³n de CP-3001-02

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3001-02** | Validar el comportamiento del sistema al intentar mapear seleccionando el editor local `JOSM` cuando el servicio de control remoto (puerto 8111) se encuentra inactivo. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema otorga el bloqueo de la tarea (`LOCKED_FOR_MAPPING`), pero muestra una alerta visible al usuario indicando que "JOSM is not running". | El sistema muestra correctamente el modal de error de conexiÃ³n con JOSM. Al verificar el estado, la tarea aparece bloqueada por el usuario activo, previniendo pÃ©rdida del candado. |

| Evidencia |
| :-- |
| Alerta de conexiÃ³n fallida con JOSM<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3001-02-error-josm.png" width="800px" alt="CP-3001-02 - Modal de error JOSM is not running"></a><br>NotificaciÃ³n de la plataforma alertando al usuario que debe iniciar el software JOSM. |

---

### 1.3. EjecuciÃ³n de CP-3001-03

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3001-03** | Validar que el sistema restringe el inicio de sesiÃ³n de mapeo si el usuario no ha aceptado los tÃ©rminos y condiciones de la licencia asociada al proyecto. | Manual | Fallido | El botÃ³n no se bloques |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El bloqueo es denegado preventivamente (`UserLicenseError`). Aparece un modal de aceptaciÃ³n obligatoria de los tÃ©rminos de uso de las imÃ¡genes satelitales. | Al hacer clic en "Contribuir" y luego "Mapear Tarea", la peticiÃ³n sÃ­ procesa el bloqueo. No se despliega inmediatamente el modal con el texto de la licencia y los botones de aceptaciÃ³n. |

| Evidencia |
| :-- |
| Modal de AceptaciÃ³n de Licencia<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3001-03-modal-licencia.png" width="800px" alt="CP-3001-03 - Modal de requerimiento de licencia"></a><br>VisualizaciÃ³n del texto legal requerido. Pero no se evidencia bloqueo del boton ContribuciÃ³n |

---

### 1.4. EjecuciÃ³n de CP-3001-04

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3001-04** | Validar que el sistema impide a un usuario (Mapper) mantener mÃºltiples tareas bloqueadas simultÃ¡neamente para el mismo propÃ³sito (Mapeo). | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema deniega el bloqueo de la segunda tarea solicitada y muestra una alerta/modal indicando que el usuario ya posee una tarea bloqueada (`UserAlreadyHasTaskLocked`). | La peticiÃ³n de bloqueo sobre la segunda tarea es rechazada con un HTTP 403. La UI muestra un modal informando sobre la restricciÃ³n de concurrencia y provee un enlace hacia la tarea previamente bloqueada. |

| Evidencia |
| :-- |
| Alerta de Tareas Concurrentes<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3001-04-limite-concurrencia.png" width="800px" alt="CP-3001-04 - Modal UserAlreadyHasTaskLocked"></a><br>Mensaje del frontend indicando que se debe finalizar la tarea actual antes de solicitar una nueva. |

---

### 1.5. EjecuciÃ³n de CP-3001-05

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3001-05** | Validar que el sistema impide bloquear para mapeo una tarea que se encuentra en un estado topogrÃ¡fico inconsistente (por ejemplo, `MAPPED`). | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema deniega la acciÃ³n por estado invÃ¡lido (`InvalidTaskState`). La interfaz debe ocultar/deshabilitar el botÃ³n "Mapear Tarea" para tareas en dicho estado. | Al seleccionar una tarea en estado `MAPPED`, la interfaz oculta el botÃ³n "Mapear Tarea" y expone las acciones de validaciÃ³n (sujetas a permisos). |

| Evidencia |
| :-- |
| Estado de botÃ³n segÃºn selecciÃ³n de tarea<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3001-05-boton-deshabilitado.png" width="800px" alt="CP-3001-05 - BotÃ³n de mapeo ausente en tarea Mapped"></a><br>VisualizaciÃ³n de la barra lateral sin opciÃ³n de mapeo para la tarea completada. |

---

### 1.6. EjecuciÃ³n de CP-3001-06

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3001-06** | Validar el rechazo de bloqueo cuando el nivel de experiencia del usuario (`BEGINNER`) es inferior al nivel requerido por la configuraciÃ³n del proyecto (`ADVANCED`). | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El bloqueo es denegado (`UserPermissionError`). Aparece un mensaje explÃ­cito indicando que el usuario no cuenta con el nivel necesario para participar en este proyecto. | El sistema evalÃºa correctamente el nivel del usuario. La interfaz notifica la restricciÃ³n mediante una alerta indicando que el nivel requerido es superior al actual. |

| Evidencia |
| :-- |
| Alerta de restricciÃ³n por Nivel<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3001-06-error-nivel.png" width="800px" alt="CP-3001-06 - Mensaje UserPermissionError"></a><br>NotificaciÃ³n advirtiendo que solo usuarios de nivel Avanzado pueden contribuir. |

---

### 1.7. EjecuciÃ³n de CP-3001-07

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3001-07** | Validar el comportamiento predeterminado cuando se solicita un bloqueo de tarea no seleccionando un tipo especÃ­fico de editor. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La tarea selecciona un editor predeterminado ante la ausencia de un editor seleccinado. El sistema selecciona automÃ¡ticamente el entorno web predeterminado (`iD`). | La tarea se bloqueÃ³ correctamente. La interfaz detectÃ³ la selecciÃ³n predeterminada de editor e inicializÃ³ la vista de mapeo utilizando el iframe del editor iD. |

| Evidencia |
| :-- |
| SelecciÃ³n de Editor web por Defecto<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3001-07-fallback-editor.png" width="800px" alt="CP-3001-07 - InicializaciÃ³n de iD como fallback"></a><br>SelecciÃ³n del entorno web por defecto tras omitir explÃ­citamente la selecciÃ³n de editor en la configuraciÃ³n. |

## 2. ESC-3002 LiberaciÃ³n y EnvÃ­o de Tarea de Mapeo (Submit)

### 2.1. EjecuciÃ³n de CP-3002-01

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3002-01** | Validar que el titular del bloqueo de una tarea (`LOCKED_FOR_MAPPING`) puede finalizar el mapeo seleccionando la opciÃ³n "Yes" (Mapeo completo). | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema cambia el estado topogrÃ¡fico de la tarea a `MAPPED`, elimina la asociaciÃ³n temporal (`lockHolder`) con el usuario y aÃ±ade la acciÃ³n al historial de la tarea. | La solicitud se procesÃ³ correctamente (`HTTP 200`). La interfaz actualizÃ³ el color de la tarea en el mapa, y en la pestaÃ±a "History" se reflejÃ³ el evento `STATE_CHANGE: MAPPED` bajo el nombre del usuario. |

| Evidencia |
| :-- |
| ConfirmaciÃ³n de estado Mapped<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3002-01-tarea-mapped.png" width="800px" alt="CP-3002-01 - Interfaz mostrando estado Mapped y botÃ³n Submit"></a><br>Captura del panel lateral durante la selecciÃ³n de la opciÃ³n "Yes" para finalizar la tarea. |
| ActualizaciÃ³n del historial de la tarea<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3002-01-historial.png" width="800px" alt="CP-3002-01 - Registro de la acciÃ³n en TaskHistory"></a><br>Vista del historial comprobando la transiciÃ³n de estado registrada en la base de datos. |

---

### 2.2. EjecuciÃ³n de CP-3002-02

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3002-02** | Validar que el titular de la tarea puede liberar (abortar o pausar) el mapeo seleccionando la opciÃ³n "No" (Mapeo incompleto). | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La tarea revierte su estado a `READY`, permitiendo que quede disponible nuevamente en el *pool* del proyecto para ser tomada por otro usuario. Se remueve el bloqueo. | Tras seleccionar "No", la interfaz retornÃ³ el color de la tarea a su estado original (transparente/blanco). La API de consulta de tareas la listÃ³ nuevamente con estado `READY` sin asignaciÃ³n de titular. |

| Evidencia |
| :-- |
| LiberaciÃ³n de tarea a estado Ready<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3002-02-tarea-ready.png" width="800px" alt="CP-3002-02 - SelecciÃ³n de la opciÃ³n No"></a><br>Luego de seleccionar NO, la tarea queda disponible para ser mapeada por cualquier colaborador |

---

### 2.3. EjecuciÃ³n de CP-3002-03

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3002-03** | Validar la prevenciÃ³n de transiciones invÃ¡lidas: el panel de liberaciÃ³n ("Submit") no debe estar visible si el usuario selecciona una tarea libre (`READY`) en el mapa. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Al seleccionar una tarea en estado `READY`, la UI expone el botÃ³n de inicio ("Map a task"), ocultando completamente el bloque de opciones (Yes/No) y el botÃ³n "Submit", evitando envÃ­os ilegales. | Se seleccionÃ³ una tarea libre en el explorador. En la parte inferior se muestra solo el botÃ³n para iniciar mapeo. No se renderizaron controles de finalizaciÃ³n (Submit). |

| Evidencia |
| :-- |
| Controles de submit ocultos (Tarea Ready)<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3002-03-no-submit-ready.png" width="800px" alt="CP-3002-03 - Interfaz sin opciones de Submit en READY"></a><br>No se expone opciones de transiciÃ³n de finalizaciÃ³n, solo el boton para iniciar el mapeo |

---

### 2.4. EjecuciÃ³n de CP-3002-04

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3002-04** | Validar la protecciÃ³n de autorÃ­a visual: la interfaz debe ocultar el panel de liberaciÃ³n ("Submit") y controles de ediciÃ³n al seleccionar una tarea bloqueada por un tercero. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Al seleccionar una tarea con indicador de bloqueo (candado), el panel muestra "Locked by [Nombre]". No se muestran botones de ediciÃ³n ni el panel de preguntas de "Submit". | Se hizo clic sobre una tarea bloqueada por otro usuario. El panel renderizÃ³ la alerta "Locked for mapping by [Usuario]" y eliminÃ³ todo control de acciÃ³n (botones), garantizando que no se pueda interferir con el trabajo ajeno desde la UI. |

| Evidencia |
| :-- |
| Bloqueo visual por pertenencia ajena<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3002-04-locked-by-other.png" width="800px" alt="CP-3002-04 - Tarea ajena bloqueada en UI"></a><br>Panel lateral notificando la titularidad del bloqueo y suprimiendo controles de mapeo o envÃ­o. |

---

### 2.5. EjecuciÃ³n de CP-3002-05

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3002-05** | Validar que el panel de liberaciÃ³n ("Submit") permanece oculto al inspeccionar una tarea que ya ha sido finalizada (`MAPPED`) por el usuario u otros. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El panel lateral muestra el estado actual de la tarea (Mapeada, en espera de validaciÃ³n). Los controles de "Submit" de la etapa de mapeo no se renderizan, respetando la secuencia del ciclo de vida. | Al seleccionar una tarea en color azul (`MAPPED`), la UI mostrÃ³ el historial y los botones correspondientes a validaciÃ³n (si los permisos lo permiten), confirmando que las opciones de "Submit" de mapeo desaparecieron del DOM. |

| Evidencia |
| :-- |
| Ocultamiento de controles post-mapeo<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3002-05-mapped-task.png" width="800px" alt="CP-3002-05 - Ausencia de controles Submit en tarea Mapped"></a><br>VisualizaciÃ³n del estado de una tarea lista para validar, evidenciando el respeto de las transiciones de estado en la interfaz. |


## 3. ESC-3003 DivisiÃ³n de Tarea de Mapeo (Split Task)

### 3.1. EjecuciÃ³n de CP-3003-01

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3003-01** | Validar que el sistema permite a un usuario dividir (Split) una tarea bloqueada bajo su titularidad cuando el nivel de zoom cartogrÃ¡fico es vÃ¡lido (LÃ­mite Superior VÃ¡lido = 17). | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema ejecuta la divisiÃ³n exitosamente. El polÃ­gono de la tarea original desaparece del mapa y es reemplazado por 4 nuevas sub-tareas. El contador general de tareas del proyecto se incrementa en 3. | Al presionar el botÃ³n "Split task" en una tarea de nivel de zoom 17, el sistema procesÃ³ la solicitud sin errores. El mapa se refrescÃ³ mostrando la grilla subdividida en 4 sectores mÃ¡s pequeÃ±os dentro del espacio original. |

| Evidencia |
| :-- |
| DivisiÃ³n de tarea completada (Zoom 17)<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3003-01-split-success.png" width="800px" alt="CP-3003-01 - Grilla de tarea dividida en 4"></a><br>VisualizaciÃ³n del mapa donde se aprecia el fraccionamiento de la tarea original en sub-tareas manejables. Al lado derecho se observa las 4 tareas recientes disponibles para mapear |

---

### 3.2. EjecuciÃ³n de CP-3003-02

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3003-02** | Validar que el sistema restringe matemÃ¡ticamente la divisiÃ³n de una tarea si el nivel de zoom cartogrÃ¡fico excede el mÃ¡ximo soportado (LÃ­mite Superior InvÃ¡lido = 18). | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La interfaz muestra una notificaciÃ³n indicando que la tarea es demasiado pequeÃ±a para dividirse (`SmallToSplit`). El polÃ­gono original se mantiene intacto y no se alteran los contadores del proyecto. | Tras intentar dividir una sub-tarea que ya se encontraba en el nivel de zoom 18, la UI arrojÃ³ la alerta de error esperada ("Task is too small to split"). La geometrÃ­a en el mapa no sufriÃ³ alteraciones. |

| Evidencia |
| :-- |
| Alerta de restricciÃ³n por zoom mÃ¡ximo<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3003-02-split-error-zoom.png" width="800px" alt="CP-3003-02 - Toast error de tarea muy pequeÃ±a"></a><br>Captura de pantalla de la notificaciÃ³n del sistema advirtiendo la imposibilidad tÃ©cnica de subdividir a esa escala. |

---

### 3.3. EjecuciÃ³n de CP-3003-03

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3003-03** | Validar que la interfaz de usuario oculta o deshabilita la opciÃ³n de "Split Task" si el usuario selecciona una tarea libre en el mapa (Estado `READY`), previniendo operaciones sobre geometrÃ­as no bloqueadas. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El panel lateral, al renderizar los detalles de una tarea `READY`, no debe exponer el botÃ³n o enlace "Split task", forzando al usuario a iniciar la sesiÃ³n de mapeo (Lock) primero. | Se seleccionÃ³ una tarea libre (blanca/transparente). El panel de control se actualizÃ³ mostrando la descripciÃ³n y el botÃ³n "Map Task", pero omitiÃ³ el botÃ³n de divisiÃ³n, confirmando el correcto control de estado en la UI. |

| Evidencia |
| :-- |
| OpciÃ³n de Split oculta en tarea libre<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3003-03-no-split-ready.png" width="800px" alt="CP-3003-03 - Panel sin botÃ³n de split en estado Ready"></a><br>Panel lateral evidenciando la adaptaciÃ³n de los controles funcionales segÃºn el estado previo de la tarea. |

---

### 3.4. EjecuciÃ³n de CP-3003-04

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3003-04** | Validar que el sistema protege la geometrÃ­a de tareas bloqueadas por terceros, ocultando la opciÃ³n "Split Task" cuando un usuario inspecciona una tarea con titularidad ajena. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Al seleccionar una tarea con el indicador visual de bloqueo (candado), la interfaz indica "Locked by [User]" y retira por completo el botÃ³n "Split task" del DOM. | Se inspeccionÃ³ una tarea actualmente en mapeo por otro voluntario. El panel lateral renderizÃ³ la advertencia de titularidad ("Locked for mapping by...") y no mostrÃ³ ningÃºn control interactivo que permitiera alterar o dividir la geometrÃ­a. |

| Evidencia |
| :-- |
| OpciÃ³n de Split oculta en tarea ajena<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3003-04-no-split-other-user.png" width="800px" alt="CP-3003-04 - Ausencia de controles en tarea bloqueada por tercero"></a><br>Vista de protecciÃ³n de autorÃ­a, confirmando que la divisiÃ³n cartogrÃ¡fica exige propiedad activa del bloqueo. |


## 4. ESC-3004 ExpiraciÃ³n y ExtensiÃ³n de Bloqueo de Tarea (Auto-unlock / Extend)

### 4.1. EjecuciÃ³n de CP-3004-01

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3004-01** | Validar que el sistema (Cron/Timer) respeta el bloqueo exclusivo de la tarea mientras el tiempo transcurrido sea inferior al lÃ­mite mÃ¡ximo configurado (`autoUnlockSeconds`). | AutomÃ¡tico | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Al alcanzar un tiempo transcurrido igual a `T = L - 1 segundo` (donde L es el lÃ­mite mÃ¡ximo), la tarea debe mantener su estado `LOCKED_FOR_MAPPING` y el usuario actual conserva la titularidad del bloqueo. | La tarea fue monitoreada hasta el segundo previo a la expiraciÃ³n. La API de estado confirmÃ³ que la tarea seguÃ­a perteneciendo al usuario (`lockHolder` intacto) y el estado se mantuvo en `LOCKED_FOR_MAPPING`. |

| Evidencia |
| :-- |
| Tarea activa antes del lÃ­mite temporal<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3004-01-bloqueo-activo.png" width="800px" alt="CP-3004-01 - Tarea en mapeo cercana a expirar"></a><br>Registro del temporizador interno (o log de la base de datos) demostrando que el bloqueo se respeta dentro del umbral vÃ¡lido. |

---

### 4.2. EjecuciÃ³n de CP-3004-02

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3004-02** | Validar la liberaciÃ³n forzada de la tarea por el sistema cuando el tiempo de bloqueo iguala o supera el lÃ­mite mÃ¡ximo configurado (`autoUnlockSeconds`). | AutomÃ¡tico | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Al llegar al tiempo `T = L` (o superarlo), el sistema revoca el acceso del usuario, cambia el estado a `READY` y aÃ±ade al historial la acciÃ³n `AUTO_UNLOCKED_FOR_MAPPING`. | El temporizador alcanzÃ³ el lÃ­mite establecido (tÃ­picamente 120 minutos). El cron del backend ejecutÃ³ la revocaciÃ³n, dejando el campo `locked_by` en `NULL`. La tarea volviÃ³ a renderizarse disponible (`READY`) en el mapa. |

| Evidencia |
| :-- |
| LiberaciÃ³n automÃ¡tica por expiraciÃ³n<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3004-02-auto-unlock.png" width="800px" alt="CP-3004-02 - TransiciÃ³n a READY por sistema"></a><br>Historial de la tarea reflejando la acciÃ³n automatizada de liberaciÃ³n por exceso de tiempo de ediciÃ³n. |

---

### 4.3. EjecuciÃ³n de CP-3004-03

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3004-03** | Validar que la interfaz permite al titular actual de una tarea (`LOCKED_FOR_MAPPING`) solicitar una extensiÃ³n manual del tiempo de bloqueo antes de su expiraciÃ³n. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Al hacer clic en el botÃ³n de extensiÃ³n de tiempo (ej. "Extend Session" en el panel lateral o modal), el sistema procesa la peticiÃ³n (`HTTP 200`), reinicia el temporizador de expiraciÃ³n y notifica el Ã©xito en la UI. | A falta de pocos minutos para expirar, se mostrÃ³ un modal preventivo. Al hacer clic en "Extend Session", la API respondiÃ³ favorablemente, el temporizador de la interfaz se reiniciÃ³ a 120 minutos y se registrÃ³ `EXTENDED_FOR_MAPPING` en el historial. |

| Evidencia |
| :-- |
| Reinicio de temporizador post-extensiÃ³n<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3004-03-extend-success.png" width="800px" alt="CP-3004-03 - NotificaciÃ³n de sesiÃ³n extendida"></a><br>Captura del temporizador restablecido en el panel de mapeo tras la interacciÃ³n exitosa con la UI. |

---

### 4.4. EjecuciÃ³n de CP-3004-04

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3004-04** | Validar la protecciÃ³n de la interfaz: el botÃ³n "Extend Session" no debe estar presente o ejecutable si la tarea seleccionada se encuentra en estado libre (`READY`). | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Al inspeccionar una tarea libre (`READY`), la interfaz no debe exponer controles temporales ni botones para extender sesiÃ³n, previniendo peticiones invÃ¡lidas (Error: `TaskStatusNotLocked`). | La tarea libre se visualizÃ³ correctamente. El panel de la barra lateral se renderizÃ³ sin temporizadores ni controles de extensiÃ³n, haciendo imposible detonar el flujo desde el frontend. |

| Evidencia |
| :-- |
| Controles de extensiÃ³n ocultos (Tarea Libre)<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3004-04-no-extend-ready.png" width="800px" alt="CP-3004-04 - UI sin timer en tarea Ready"></a><br>DemostraciÃ³n de que la funcionalidad de extensiÃ³n es dependiente del estado actual de bloqueo en la interfaz. |

---

### 4.5. EjecuciÃ³n de CP-3004-05

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3004-05** | Validar la protecciÃ³n de la interfaz: el botÃ³n "Extend Session" no debe estar presente o ejecutable si se selecciona una tarea bloqueada por un tercero. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Al inspeccionar una tarea ajena (`LOCKED_FOR_MAPPING`), el panel muestra "Locked by [Usuario]". No se visualiza temporizador interactivo ni botones para extender la sesiÃ³n (Error: `LockedByAnotherUser`). | Al seleccionar una tarea en uso por otro Mapper, el panel omitiÃ³ la inclusiÃ³n de controles de extensiÃ³n de tiempo, garantizando la imposibilidad de que un usuario modifique el temporizador de una sesiÃ³n ajena. |

| Evidencia |
| :-- |
| Controles de extensiÃ³n ocultos (Tarea Ajena)<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3004-05-no-extend-other.png" width="800px" alt="CP-3004-05 - Tarea de tercero sin controles de tiempo"></a><br>Panel lateral resguardando la seguridad de las sesiones concurrentes, denegando el acceso a controles de extensiÃ³n a los no titulares. |


## 5. ESC-3005 InteracciÃ³n CartogrÃ¡fica y VisualizaciÃ³n de Trazabilidad (Historial)

### 5.1. EjecuciÃ³n de CP-3005-01

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3005-01** | Validar que el filtro "Actividades" en el panel de historial oculta los comentarios de texto y renderiza exclusivamente los eventos de auditorÃ­a y transiciones de estado del sistema. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Al seleccionar el radio button "Actividades", la lista (DOM) se actualiza dinÃ¡micamente. Solo se muestran registros como "bloqueada para mapeo", "marcada como lista" o "dividiÃ³ una tarea". Todos los mensajes ingresados manualmente por usuarios desaparecen de la vista. | Tras activar el filtro en la UI, la pestaÃ±a "Historial" ocultÃ³ instantÃ¡neamente los comentarios. El registro visual mostrÃ³ una lÃ­nea de tiempo clara con las acciones transaccionales realizadas sobre la tarea por diversos usuarios y por el sistema. |

| Evidencia |
| :-- |
| Filtro de Actividades Aplicado<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3005-01-filtro-actividades.png" width="800px" alt="CP-3005-01 - Renderizado del historial mostrando solo transiciones de estado"></a><br>VisualizaciÃ³n del panel derecho de la plataforma con el radio button "Actividades" seleccionado y el *feed* de eventos correspondiente. |

---

### 5.2. EjecuciÃ³n de CP-3005-02

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3005-02** | Validar que el filtro "Comentarios" aisla la vista de la pestaÃ±a Historial para mostrar Ãºnicamente los mensajes textuales aportados por los voluntarios, excluyendo logs de sistema. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Al seleccionar el radio button "Comentarios", los registros automÃ¡ticos de transiciÃ³n de estados desaparecen. El panel muestra exclusivamente los avatares, nombres de usuario y el texto de los comentarios dejados en el flujo de finalizaciÃ³n de tarea. | La selecciÃ³n del radio button "Comentarios" actualizÃ³ la vista aislando correctamente las notas de los mapeadores previos. Los mensajes de estado ("LOCKED", "MAPPED") fueron suprimidos de la interfaz grÃ¡fica exitosamente. |

| Evidencia |
| :-- |
| Filtro de Comentarios Aplicado<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3005-02-filtro-comentarios.png" width="800px" alt="CP-3005-02 - Renderizado del historial mostrando solo texto de usuarios"></a><br>Panel de historial confirmando la discriminaciÃ³n funcional de datos en la interfaz. |

---

### 5.3. EjecuciÃ³n de CP-3005-03

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3005-03** | Validar la reactividad de la interfaz (Editor iD) al seleccionar una geometrÃ­a vÃ¡lida que se encuentra ubicada dentro de los lÃ­mites delineados para la tarea actual. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Al hacer clic sobre un Ã¡rea o vÃ­a existente (dentro del borde magenta), el panel lateral izquierdo debe cambiar de contexto para exponer los metadatos del elemento, como su Tipo (por ejemplo, Ãrea residencial), Nombre, y Etiquetas (Tags de OSM como `landuse=residential`). | Se hizo clic en un polÃ­gono residencial habilitado dentro del Bounding Box. El panel izquierdo reaccionÃ³ sin latencia mostrando la jerarquÃ­a de etiquetas, confirmando que la integraciÃ³n grÃ¡fica entre iD y TM funciona bidireccionalmente. |

| Evidencia |
| :-- |
| SelecciÃ³n de GeometrÃ­a VÃ¡lida<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3005-03-seleccion-elemento.png" width="800px" alt="CP-3005-03 - Panel izquierdo detallando etiquetas del elemento"></a><br>Captura evidenciando la lectura de metadatos (`type=multipolygon`) al seleccionar un elemento en el lienzo principal. |

---
### 5.4. EjecuciÃ³n de CP-3005-04

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-3005-04** | Validar que el sistema inyecta correctamente las guÃ­as visuales restrictivas (sombreado y texto de advertencia) fuera del BBOX de la tarea, permitiendo funcionalmente la ediciÃ³n para delegar el conflicto al flujo de ValidaciÃ³n. | Manual | Exitoso | Ninguno |


| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Al desplazar el mapa fuera de la zona activa, debe mantenerse visible la mÃ¡scara oscura y el mensaje "Task for project [ID]. Do not edit outside of this area!". Al intentar aÃ±adir un nodo, el editor debe permitir su creaciÃ³n, evidenciando el comportamiento de advertencia visual (no bloqueante). | Al realizar *pan* hacia el exterior de la tarea, el frontend renderizÃ³ correctamente la capa de oscurecimiento y el texto de alerta. Se seleccionÃ³ la herramienta "Punto" y se hizo clic en el Ã¡rea ensombrecida; el nodo fue agregado exitosamente a la capa cartogrÃ¡fica de OSM, validando el comportamiento esperado de la plataforma. |

| Evidencia |
| :-- |
| Renderizado de mÃ¡scara y advertencia visual<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-03-ejecucion-mapeado/CP-3005-04-guia-visual-permitida.png" width="800px" alt="CP-3005-04 - CreaciÃ³n de nodo en zona ensombrecida con advertencia"></a><br>Lienzo del editor mostrando un nodo reciÃ©n creado en el exterior de los lÃ­mites de la tarea, en coexistencia con el sombreado preventivo inyectado por el Tasking Manager. |



