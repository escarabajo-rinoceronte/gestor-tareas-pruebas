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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — Proceso de ValidaciÃ³n: EjecuciÃ³n de casos de pruebas del MOD-04</td></tr>
      <tr><td class="label">Fecha</td><td>23/06/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# Proceso de ValidaciÃ³n: EjecuciÃ³n de casos de pruebas del MOD-04

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

## 1. ESC-4001 Bloqueo y PrevenciÃ³n de Auto-validaciÃ³n

### 1.1. EjecuciÃ³n de CP-4001-01

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4001-01** | Validar que el sistema asigna la tarea al Validator, cambiando su estado a LOCKED_FOR_VALIDATION. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema asigna la tarea al Validator, mostrando la interfaz de validaciÃ³n y cambiando el estado a Locked. | El sistema asignÃ³ exitosamente la tarea al usuario logueado como Validator, permitiÃ©ndole interactuar en la vista de control de calidad. |

| Evidencia |
| :-- |
| Tarea bloqueada por Validator<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4001-01-01.jpg" width="800px" alt="CP-4001-01 - Tarea en pantalla de validaciÃ³n"></a><br>Pantalla de control de calidad de la tarea exitosamente bloqueada. |

---

### 1.2. EjecuciÃ³n de CP-4001-02

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4001-02** | Impedir validaciÃ³n sobre una tarea mapeada por el propio usuario validador. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema alerta sobre la restricciÃ³n de auto-validaciÃ³n and declina el requerimiento de bloqueo para evaluaciÃ³n. | Al intentar ingresar a revisar una tarea que mapeÃ³ el mismo usuario en sesiÃ³n, el sistema arrojÃ³ la restricciÃ³n de flujo y denegÃ³ el acceso de validaciÃ³n. |

| Evidencia |
| :-- |
| Bloqueo a la auto-validaciÃ³n<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4001-02-01.jpg" width="800px" alt="CP-4001-02 - Error prevenciÃ³n de auto validaciÃ³n"></a><br>Mensaje del sistema impidiendo el flujo de validaciÃ³n. |

---

### 1.3. EjecuciÃ³n de CP-4001-03

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4001-03** | Intento de bloqueo para validaciÃ³n por parte de un usuario con nivel de experiencia insuficiente (Mapper normal). | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema oculta la opciÃ³n de validaciÃ³n o deniega el acceso con un mensaje de permisos insuficientes debido a la falta de experiencia requerida. | La interfaz detectÃ³ el perfil de Mapper sin los requerimientos mÃ­nimos de experiencia y ocultÃ³ por completo el control de bloqueo para revisiÃ³n. |

| Evidencia |
| :-- |
| Controles de validaciÃ³n ocultos<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4001-03-01.jpg" width="800px" alt="CP-4001-03 - Permisos insuficientes en panel"></a><br>Vista del panel del mapa sin botones de gestiÃ³n de calidad para usuarios no aptos. |

---

### 1.4. EjecuciÃ³n de CP-4001-04

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4001-04** | Bloqueo grupal/masivo de mÃºltiples tareas ajenas en estado MAPPED simultÃ¡neamente. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema asigna todas las tareas seleccionadas al usuario en funciÃ³n de Validator, pasando el conjunto completo al estado LOCKED_FOR_VALIDATION. | Al procesar la selecciÃ³n mÃºltiple, el sistema bloqueÃ³ el lote de celdas ajenas simultÃ¡neamente y activÃ³ la barra de ediciÃ³n masiva de calidad. |

| Evidencia |
| :-- |
| Bloqueo por lote concedido<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4001-04-01.jpg" width="800px" alt="CP-4001-04 - Bloqueo mÃºltiple exitoso"></a><br>Mapa reflejando el conjunto de tareas seleccionadas bajo el color de revisiÃ³n grupal. |

---

### 1.5. EjecuciÃ³n de CP-4001-05

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4001-05** | Intento de bloqueo masivo de tareas en lote con autorÃ­a mixta (ajenas y una propia). | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema bloquea las tareas de terceros and rechaza aisladamente o advierte sobre la tarea propia impidiendo que transicione. | El sistema inhabilitÃ³ el guardado grupal arrojando un modal de alerta que forzÃ³ la exclusiÃ³n de la tarea propia mapeada por el usuario actual. |

| Evidencia |
| :-- |
| Alerta de lote mixto<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4001-05-01.jpg" width="800px" alt="CP-4001-05 - Advertencia de auto-validaciÃ³n masiva"></a><br>Modal del sistema rechazando el procesamiento por lote debido a la presencia de un elemento con autorÃ­a propia. |

---

### 1.6. EjecuciÃ³n de CP-4001-06

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4001-06** | Intento de validaciÃ³n sobre una tarea en estado READY o LOCKED_FOR_MAPPING. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La interfaz de usuario deshabilita el botÃ³n de validaciÃ³n, imposibilitando la acciÃ³n sobre estados no listos. | Al hacer clic en una celda que aÃºn no ha completado la fase de mapeo, los controles del panel impidieron cualquier transiciÃ³n de validaciÃ³n. |

| Evidencia |
| :-- |
| Controles de calidad deshabilitados<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4001-06-01.jpg" width="800px" alt="CP-4001-06 - Celda en estado no listo"></a><br>Panel de visualizaciÃ³n del mapa showing los botones bloqueados para tareas que no estÃ¡n en estado MAPPED. |

---

### 1.7. EjecuciÃ³n de CP-4001-07

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4001-07** | Intentar forzar el bloqueo de validaciÃ³n sobre una tarea que ya estÃ¡ bloqueada por otro validador en concurrencia. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La interfaz deshabilita u oculta los controles de validaciÃ³n para la tarea bloqueada, mostrando visualmente el candado de restricciÃ³n y permitiendo Ãºnicamente la opciÃ³n de validar un elemento distinto. | El sistema bloqueÃ³ preventivamente la acciÃ³n en la UI; al seleccionar la tarea en paralelo, se visualizÃ³ el indicador de candado y los controles individuales de revisiÃ³n quedaron omitidos, dejando activo Ãºnicamente el botÃ³n "Validar otra tarea". |

| Evidencia |
| :-- |
| Control restrictivo por concurrencia y opciÃ³n alternativa activa<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4001-07-01.jpg" width="800px" alt="CP-4001-07 - Tarea bloqueada en concurrencia sin opciones individuales"></a><br>Vista de la cuadrÃ­cula con el estado "Bloqueada" visible &nbsp;y el panel lateral redirigiendo el flujo exclusivamente mediante el botÃ³n "Validar otra tarea". |

---

### 1.8. EjecuciÃ³n de CP-4001-08

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4001-08** | Intentar iniciar un bloqueo de validaciÃ³n sobre una tarea que ya se encuentra en estado VALIDATED. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La interfaz deshabilita u oculta los controles de validaciÃ³n individuales para la tarea en estado Terminada, permitiendo Ãºnicamente la opciÃ³n de validar un elemento distinto. | El sistema limitÃ³ la acciÃ³n en la UI; al seleccionar la tarea con estado "Terminada" (color verde), el panel lateral omitiÃ³ los botones de revisiÃ³n individuales y redirigiÃ³ el flujo exclusivamente mediante el botÃ³n "Validar otra tarea". |

| Evidencia |
| :-- |
| Controles de revisiÃ³n omitidos en tarea terminada y opciÃ³n alternativa activa<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4001-08-01.jpg" width="800px" alt="CP-4001-08 - Tarea validada sin opciÃ³n de re-bloqueo"></a><br>Tarea #2 seleccionada en estado `VALIDATED` , constatando la ausencia de controles individuales y la presencia del botÃ³n "Validar otra tarea". |

---

### 1.9. EjecuciÃ³n de CP-4001-09

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4001-09** | Intentar iniciar un nuevo bloqueo sobre una tarea INVALIDATED antes de que un Mapper realice las correcciones pertinentes. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema restringe el bloqueo de validaciÃ³n, requiriendo que la tarea pase primero por el flujo de correcciÃ³n y habilitando Ãºnicamente la opciÃ³n de mapeo. | El sistema bloqueÃ³ la acciÃ³n de validaciÃ³n en la UI; al seleccionar la Tarea con el estado "Necesita mÃ¡s mapeo" (`INVALIDATED` ), los controles de revisiÃ³n quedaron omitidos y el panel inferior se actualizÃ³ mostrando Ãºnicamente el botÃ³n "Mapear tarea seleccionada". |

| Evidencia |
| :-- |
| RestricciÃ³n de re-validaciÃ³n prematura y botÃ³n de mapeo activo<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4001-09-01.jpg" width="800px" alt="CP-4001-09 - Tarea invalidada en espera de correcciÃ³n"></a><br>Tarea #3 en estado `INVALIDATED` &nbsp;("Necesita mÃ¡s mapeo"), constatando que el sistema redirige el flujo mediante el botÃ³n "Mapear tarea seleccionada". |

---

### 1.10. EjecuciÃ³n de CP-4001-10

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4001-10** | Intentar auto-validar una tarea propia operando bajo un perfil que combines funciones de Validator y Administrador global. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema otorga el bloqueo de la tarea de autorÃ­a propia al validar que el usuario posee permisos superiores de Administrador global del sistema. | La plataforma validÃ³ el rol del Administrador y permitiÃ³ omitir la polÃ­tica restrictiva, asignÃ¡ndole la tarea directamente y permitiendo la interacciÃ³n en la interfaz con el botÃ³n de reanudaciÃ³n. |

| Evidencia |
| :-- |
| Registro de AutorÃ­a del Mapeo Original<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4001-10-01.jpg" width="800px" alt="CP-4001-10 - Registro de mapeo por el mismo usuario"></a><br>CronologÃ­a de eventos del sistema que constata que la tarea fue trabajada y guardada inicialmente en la fase de mapeo por el usuario actual con privilegios de administrador.<br><br>ConfirmaciÃ³n de Bloqueo para ValidaciÃ³n Concedido<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4001-10-02.jpg" width="800px" alt="CP-4001-10 - Estado de la tarea cambiado a LOCKED_FOR_VALIDATION"></a><br>Panel principal donde se verifica que el sistema permitiÃ³ saltar la restricciÃ³n al usuario, asignÃ¡ndole la tarea de su propia autorÃ­a y cambiando su estado a bloqueada para validaciÃ³n con los controles de ediciÃ³n activos. |

---

## 2. ESC-4002 EvaluaciÃ³n de Calidad de Tareas Mapeadas

### 2.1. EjecuciÃ³n de CP-4002-01

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4002-01** | Aprobar tarea marcÃ¡ndola como correctamente mapeada (VALIDATED). | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La tarea se registra en estado VALIDATED finalizando su revisiÃ³n positivamente. | La tarea transicionÃ³ exitosamente a estado VALIDATED despuÃ©s de confirmarse en el panel y ser devuelta en verde. |

| Evidencia |
| :-- |
| ConfirmaciÃ³n y estado Validated<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-01-01.jpg" width="800px" alt="CP-4002-01 - Tarea vÃ¡lida"></a><br>Pantalla del proyecto con la tarea ya figurando como validada exitosamente. |

---

### 2.2. EjecuciÃ³n de CP-4002-02

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4002-02** | Rechazar tarea marcÃ¡ndola como incorrecta (INVALIDATED). | Manual | Exitoso | N/A |

| Resultado esperado | Extatus obtenido |
| :-- | :-- |
| La tarea transiciona a INVALIDATED con comentario agregado para revisiÃ³n. | Se aÃ±adiÃ³ exitosamente el estatus de Invalidada y el bloque de comentario exigiendo la correcciÃ³n, quedando de amarillo en el mapa. |

| Evidencia |
| :-- |
| Interfaz de rechazo y ediciÃ³n de comentario<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-02-01.jpg" width="800px" alt="CP-4002-02 - Formulario de rechazo"></a><br>Vista del panel lateral con la opciÃ³n "More work is required" seleccionada y el texto de correcciÃ³n redactado.<br><br>ConfirmaciÃ³n de InvalidaciÃ³n e Historial<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-02-02.jpg" width="800px" alt="CP-4002-02 - Tarea rechazada en historial"></a><br>Vista del modal central con la Tarea #5 en estado amarillo y la retroalimentaciÃ³n guardada en la cronologÃ­a. |

---

### 2.3. EjecuciÃ³n de CP-4002-03

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4002-03** | Intentar rechazar una tarea (Invalidar) dejando el campo de comentario obligatorio vacÃ­o. | Manual | Fallido | El sistema permite invalidar tareas con comentarios vacÃ­os sin restricciÃ³n ni alertas. |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema previene el envÃ­o, requiriendo que se adjunte obligatoriamente un comentario explicativo mediante un alert o estado de error. | El sistema procesÃ³ y aceptÃ³ el cambio de estado con el comentario vacÃ­o, permitiendo el envÃ­o sin mostrar ninguna alerta, bloqueo o mensaje de error en la interfaz. |

| Evidencia |
| :-- |
| EnvÃ­o de invalidaciÃ³n con campo de texto vacÃ­o<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-03-01.jpg" width="800px" alt="CP-4002-03 - Formulario enviado sin texto"></a><br>Vista del panel lateral con la opciÃ³n "More work is required" seleccionada y el cuadro de ediciÃ³n "Leave a comment..." totalmente vacÃ­o al momento de remitir la acciÃ³n.<br><br>Persistencia de la tarea invalidada sin comentarios<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-03-02.jpg" width="800px" alt="CP-4002-03 - Estado guardado sin historial de texto"></a><br>Vista del modal central de la Tarea #4 en amarillo, confirmando la ausencia de registros con el mensaje informativo "No comments have been made on the task yet". |

---

### 2.4. EjecuciÃ³n de CP-4002-04

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4002-04** | Enviar evaluaciones mixtas (Aprobar unas e Invalidar otras) sobre un lote de tareas bloqueadas simultÃ¡neamente. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema actualiza cada tarea a su estado asignado individualmente (VALIDATED / INVALIDATED), liberando los bloqueos correspondientes. | Al procesar la confirmation del lote, la API discriminÃ³ los estados y asignÃ³ de manera exacta los estados finales liberando el candado de cada celda. |

| Evidencia |
| :-- |
| SelecciÃ³n y asignaciÃ³n de estados en el lote<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-04-01.jpg" width="800px" alt="CP-4002-04 - ConfiguraciÃ³n de lote mixto"></a><br>Vista del panel lateral de ediciÃ³n mÃºltiple con las tareas #6 y #8 marcadas como aprobadas ("Task well mapped") y la tarea #7 marcada para correcciÃ³n ("More work is required").<br><br>ActualizaciÃ³n e impacto en la cuadrÃ­cula general<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-04-02.jpg" width="800px" alt="CP-4002-04 - Resultados en mapa e historial"></a><br>Vista de la lista de tareas y el mapa general reflejando las tareas #6 y #8 con el estado definitivo "Terminada" (color verde) y la tarea #7 con el estado "Necesita mÃ¡s mapeo" (color amarillo). |

---

### 2.5. EjecuciÃ³n de CP-4002-05

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4002-05** | Intentar evaluar una tarea retenida en revisiÃ³n despuÃ©s de superar el tiempo lÃ­mite de asignaciÃ³n (Timeout). | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema informa mediante un error de timeout ("Ya no tienes esta tarea asignada") and la tarea se devuelve a su estado anterior. | Al intentar mandar la evaluaciÃ³n tras expirar la sesiÃ³n de bloqueo, el backend rechazÃ³ la peticiÃ³n por token vencido y limpiÃ³ el panel lateral con la alerta correspondiente. |

| Evidencia |
| :-- |
| Alerta de expiraciÃ³n de asignaciÃ³n por timeout<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-05-01.jpg" width="800px" alt="CP-4002-05 - Error por timeout de validaciÃ³n"></a><br>Vista del cuadro de diÃ¡logo emergente con el mensaje "Your session has expired" sobre la Tarea #9, ofreciendo las alternativas para cerrar la advertencia o volver a bloquear el elemento con "Relock task".<br><br>Retorno de la tarea al estado anterior en el panel general<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-05-02.jpg" width="800px" alt="CP-4002-05 - Retorno de estado"></a><br>Vista de la lista de tareas y la cuadrÃ­cula del mapa general donde la Tarea #9 se ha liberado y figura nuevamente bajo el estado "Lista para validar" con su respectivo color celeste. |

---

### 2.6. EjecuciÃ³n de CP-4002-06

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4002-06** | Enviar una evaluaciÃ³n de aprobaciÃ³n masiva (VALIDATED) sobre un lote completo de tareas asignadas simultÃ¡neamente. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema procesa la transacciÃ³n masiva de forma directa, transicionando todas las celdas del lote al estado `VALITED` simultÃ¡neamente. | El sistema procesÃ³ la validaciÃ³n mÃºltiple con Ã©xito; al confirmar la acciÃ³n en bloque, todas las tareas seleccionadas transicionaron al mismo tiempo y se actualizaron reflejando el fin de su ciclo de calidad. |

| Evidencia |
| :-- |
|SelecciÃ³n de Tareas en Bloque<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-06-01.jpg" width="800px" alt="CP-4002-06 - SelecciÃ³n mÃºltiple de tareas para validar"></a><br>Panel de control del proyecto que muestra mÃºltiples elementos en estado de lista para validar seleccionados en paralelo, habilitando el botÃ³n unificado para procesar el lote completo.<br><br>Resultado de validaciÃ³n mÃºltiple <br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-06-02.jpg" width="800px" alt="CP-4002-06 - Tareas actualizadas a Terminada en lote"></a><br>Vista del listado y el mapa general donde se constata que las tareas del lote cambiaron simultÃ¡neamente al estado definitivo de terminadas (`VALITED`)|

---

### 2.7. EjecuciÃ³n de CP-4002-07

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4002-07** | Enviar una evaluaciÃ³n de rechazo masivo (INVALIDATED) sobre un lote de tareas asignadas sin exigir comentarios por elemento. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema procesa la transacciÃ³n masiva, cambia el estado de todas las celdas a `INVALITED` y las devuelve a la cola general. | El sistema procesÃ³ la invalidaciÃ³n mÃºltiple de forma correcta; al confirmar la acciÃ³n en bloque, todas las tareas seleccionadas transicionaron simultÃ¡neamente al estado que solicita mÃ¡s mapeo. |

| Evidencia |
| :-- |
|SelecciÃ³n de MÃºltiples Elementos en Lista<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-07-01.jpg" width="800px" alt="CP-4002-07 - SelecciÃ³n mÃºltiple para invalidar"></a><br>Interfaz del proyecto que muestra un conjunto de tareas en estado listo para validar seleccionadas al mismo tiempo, activando el botÃ³n en la barra inferior para procesar las tareas en lote.<br><br>Resultado de la InvalidaciÃ³n Masiva<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-07-02.jpg" width="800px" alt="CP-4002-07 - Lote cambiado a Necesita mÃ¡s mapeo"></a><br>Vista del listado lateral y de la cuadrÃ­cula geogrÃ¡fica donde se observa que los elementos seleccionados pasaron en conjunto al estado `INVALITED` correspondiente a la necesidad de mÃ¡s mapeo. |

---

### 2.8. EjecuciÃ³n de CP-4002-08

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4002-08** | Registrar una invalidaciÃ³n (INVALIDATED) insertando caracteres especiales, sÃ­mbolos tÃ©cnicos o formato enriquecido en el comentario. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema procesa la invalidaciÃ³n y guarda el texto en el historial correctamente sin corromper la codificaciÃ³n de los sÃ­mbolos. | El texto con codificaciÃ³n tÃ©cnica y caracteres especiales fue almacenado y renderizado en la lÃ­nea de tiempo sin sufrir alteraciones ni truncamiento de caracteres. |

| Evidencia |
| :-- |
| Persistencia de caracteres especiales en historial<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-08-01.jpg" width="800px" alt="CP-4002-08 - Comentario con sÃ­mbolos guardado"></a><br>Vista de la cronologÃ­a de la tarea mostrando los sÃ­mbolos tÃ©cnicos legibles y procesados de manera Ã­ntegra. |

---

### 2.9. EjecuciÃ³n de CP-4002-09

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4002-09** | Registrar una invalidaciÃ³n (INVALIDATED) ingresando una retroalimentaciÃ³n extensa para verificar que el sistema no posea un lÃ­mite restrictivo de caracteres. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema asimila el texto completo sin truncar la retroalimentaciÃ³n y asocia el bloque Ã­ntegro en su lÃ­nea de tiempo de actividades. | El sistema guardÃ³ y procesÃ³ el comentario de gran extensiÃ³n sin aplicar truncamientos ni generar errores de desbordamiento, mostrando los pÃ¡rrafos completos con su respectivo formato. |

| Evidencia |
| :-- |
|Registro Completo de RetroalimentaciÃ³n Extensa<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-09-01.jpg" width="800px" alt="CP-4002-09 - Comentario extenso asimilado en actividades"></a><br>Ventana emergente con el historial de actividades donde se visualiza el comentario extenso estructurado por puntos, mostrando una barra de desplazamiento activa que permite leer todo el reporte guardado sin cortes en el texto. |

---

### 2.10. EjecuciÃ³n de CP-4002-10

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4002-10** | Enviar una evaluaciÃ³n adjuntando un texto tÃ©cnico e incluyendo una imagen multimedia que evidencie el estado geogrÃ¡fico. | Manual | Fallido|Error del backend/servidor al procesar la carga de archivos adjuntos en el cuadro de comentarios de revisiÃ³n. |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema procesa el cambio de estado con Ã©xito, guarda el comentario y almacena la imagen adjunta permitiendo su visualizaciÃ³n posterior. | El sistema rechaza la carga del archivo multimedia. Aunque permite la redacciÃ³n del texto en el editor, al intentar procesar la imagen se interrumpe la carga y se despliega un mensaje de error explÃ­cito en la parte inferior del formulario, impidiendo finalizar el registro completo con su respectiva evidencia. |

| Evidencia |
| :-- |
|Fallo en la Carga de Archivos Multimedia<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4002-10-01.jpg" width="800px" alt="CP-4002-10 - Error al subir la imagen en el formulario"></a><br>Interfaz del editor de tareas donde se observa el reporte tÃ©cnico y, debajo del formulario, una alerta explÃ­cita en texto rojo con el mensaje "Error al subir la imagen", confirmando el fallo en el mÃ³dulo de carga. |

---

## 3. ESC-4003 Revertir acciones previas (Undo)

### 3.1. EjecuciÃ³n de CP-4003-01

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4003-01** | EjecuciÃ³n de "Undo" para revertir la Ãºltima acciÃ³n de categorizaciÃ³n. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Se revierte la categorizaciÃ³n retornando al estado anterior, deshaciendo la acciÃ³n y mostrando anotaciÃ³n en el timeline. | El sistema aceptÃ³ clicar en 'deshacer', anulÃ³ el flujo final y regresÃ³ la tarea al estatus previo como si la Ãºltima acciÃ³n no se hubiese cerrado. |

| Evidencia |
| :-- |
| Solicitud de reversiÃ³n desde el historial de actividades<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4003-01-01.jpg" width="800px" alt="CP-4003-01 - Solicitud de revalidaciÃ³n"></a><br>Vista del modal de la Tarea #8 con la opciÃ³n para solicitar la revalidaciÃ³n tras haber sido marcada como validada en la cronologÃ­a de eventos.<br><br>ConfirmaciÃ³n del cambio de estado por Undo<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4003-01-02.jpg" width="800px" alt="CP-4003-01 - ConfirmaciÃ³n de reversiÃ³n de estado"></a><br>Vista del mensaje de advertencia flotante que solicita confirmar si se desea cambiar el estado del elemento de vuelta a "Lista para validar". |

---

### 3.2. EjecuciÃ³n de CP-4003-02

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4003-02** | Intentar ejecutar la acciÃ³n "Undo" (Deshacer) inmediatamente despuÃ©s de haber cambiado el estado de una tarea a INVALIDATED. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema no ofrece controles o botones para deshacer la acciÃ³n (Undo) sobre elementos en estado invalidado, manteniendo la tarea de forma definitiva en el flujo de correcciÃ³n. | El sistema bloqueÃ³ la posibilidad de revertir la acciÃ³n; una vez guardada la invalidaciÃ³n, la interfaz omite por completo cualquier botÃ³n o enlace para deshacer el cambio, obligando a que la tarea permanezca en su estado actual. |

| Evidencia |
| :-- |
|RestricciÃ³n de ReversiÃ³n en Tarea Invalidada<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4003-02-01.jpg" width="800px" alt="CP-4003-02 - Inexistencia de botÃ³n Undo en historial"></a><br>Ventana emergente con el historial de actividades donde queda registrado el estado de necesidad de mÃ¡s mapeo, constatando que la interfaz no despliega ningÃºn control para revertir la transiciÃ³n mientras la celda en el mapa se mantiene en color amarillo. |

---

### 3.3. EjecuciÃ³n de CP-4003-03

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4003-03** | Intentar aplicar "Undo" (Solicitar revalidaciÃ³n) sobre una tarea cuya evaluaciÃ³n final fue realizada por otro usuario validador. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema debe permitir que cualquier usuario con funciÃ³n o rol de Validator pueda solicitar la revalidaciÃ³n (Undo) de cualquier tarea terminada, independientemente de si fue validada originalmente por un tercero. | El sistema validÃ³ el perfil de Validator del usuario en sesiÃ³n y habilitÃ³ correctamente el botÃ³n "Solicitar revalidaciÃ³n" en una tarea completada por otro revisor, permitiendo revertir el estado sin restricciones. |

| Evidencia |
| :-- |
| Control de reversiÃ³n habilitado para tareas de terceros<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4003-03-01.jpg" width="800px" alt="CP-4003-03 - ExposiciÃ³n de Undo en actividad ajena"></a><br>Vista del modal de la Tarea #2 donde se muestra activo y disponible el botÃ³n "Solicitar revalidaciÃ³n" en la parte superior derecha, confirmando el acceso correcto del Validator a elementos evaluados por otros usuarios. |

---

### 3.4. EjecuciÃ³n de CP-4003-04

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4003-04** | Intentar accionar el botÃ³n "Undo" de manera consecutiva o recursiva sobre una misma tarea. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema devuelve error o deshabilita la opciÃ³n notificando que no existe otra acciÃ³n reciente atribuible en el historial inmediato para ser deshecha. | Tras consumarse la primera reversiÃ³n con Ã©xito, el sistema deshabilitÃ³ el botÃ³n impidiendo llamadas recursivas hacia atrÃ¡s en la pila de historial. |

| Evidencia |
| :-- |
| Estado inicial previo a la reversiÃ³n consecutiva<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4003-04-01.jpg" width="800px" alt="CP-4003-04 - Estado inicial antes de deshacer"></a><br>Vista del modal de la Tarea #6 mostrando el flujo regular en el historial donde el elemento figura como validado recientemente.<br><br>Bloqueo del control tras el primer uso de deshacer<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4003-04-02.jpg" width="800px" alt="CP-4003-04 - BotÃ³n deshabilitado para segundo intento"></a><br>Vista de la actualizaciÃ³n en el historial de actividades donde el estado regresa a mapeado and se inhabilita cualquier acciÃ³n posterior para revertir consecutivamente. |

---

### 3.5. EjecuciÃ³n de CP-4003-05

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-4003-05** | Intento de ejecuciÃ³n de acciÃ³n Undo para solicitar revalidaciÃ³n por parte de un usuario con rol de Mapper estÃ¡ndar. | Manual | Exitoso | N/A |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema muestra la advertencia de confirmaciÃ³n, pero al aceptar la acciÃ³n, restringe el proceso ignorando el cambio; el estado de la tarea permanece intacto y no se habilita ningÃºn panel adicional. | Al confirmar la acciÃ³n en el mensaje emergente, el sistema bloqueÃ³ el flujo; la tarea no sufriÃ³ ninguna modificaciÃ³n en su color o estado dentro de la lista general y la interfaz omitiÃ³ la apertura del panel de revalidaciÃ³n. |

| Evidencia |
| :-- |
|Cuadro de ConfirmaciÃ³n de ReversiÃ³n Desplegado<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4003-05-01.jpg" width="800px" alt="CP-4003-05 - Mensaje modal para confirmar deshacer estado"></a><br>Ventana emergente que consulta al usuario si desea continuar con la acciÃ³n para cambiar el estado de la tarea seleccionada de vuelta a "Lista para validar".<br><br>Estado Original Sin Cambios<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-04-validacion/cp-4003-05-02.jpg" width="800px" alt="CP-4003-05 - Estado de tarea se mantiene en terminada"></a><br>Vista del listado de tareas y la cuadrÃ­cula del mapa posterior a la interacciÃ³n, donde se constata que la tarea bajo prueba retiene de forma intacta su estado VALITED, confirmando que la acciÃ³n fue ignorada por el sistema y no se abriÃ³ ningÃºn panel de ediciÃ³n o revalidaciÃ³n complementario.|
