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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — MOD-0007 - ComunicaciÃ³n y Notificaciones</td></tr>
      <tr><td class="label">Fecha</td><td>23/06/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# MOD-0007 - ComunicaciÃ³n y Notificaciones

### 7.1. Registrar comentario vÃ¡lido en una tarea

**CP-MOD7-001**

| ID              | DescripciÃ³n                                                                                                 | Tipo   | Estado  | Defectos                    |
| :-------------- | :---------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD7-001** | Verificar que el sistema permita registrar un comentario vÃ¡lido asociado a una tarea dentro de un proyecto. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                           | Resultado obtenido                                                                                                                  |
| :------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir ingresar un comentario de texto vÃ¡lido, guardarlo y mostrarlo en el historial o secciÃ³n de comentarios de la tarea. | El sistema permitiÃ³ ingresar el comentario, registrarlo correctamente y mostrarlo dentro de la secciÃ³n correspondiente de la tarea. |

#### Evidencia CP-MOD7-001 â€” Ãrea de comentarios de la tarea

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-001-01-area-comentarios-tarea.png" alt="CP-MOD7-001 - Ãrea de comentarios de la tarea" width="300">
</p>

Se observa la pantalla de la tarea donde el sistema permite registrar comentarios asociados al trabajo realizado sobre dicha tarea.

#### Evidencia CP-MOD7-001 â€” Comentario ingresado

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-001-02-comentario-ingresado.png" alt="CP-MOD7-001 - Comentario ingresado" width="300">
</p>

Se observa que el usuario ingresÃ³ un comentario vÃ¡lido en el campo correspondiente antes de enviarlo.

#### Evidencia CP-MOD7-001 â€” Comentario registrado correctamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-001-03-comentario-registrado.png" alt="CP-MOD7-001 - Comentario registrado correctamente" width="500">
</p>

Se evidencia que el sistema registrÃ³ correctamente el comentario y lo mostrÃ³ dentro del historial o secciÃ³n de comentarios de la tarea.

### 7.2. EnvÃ­o de tarea sin comentario obligatorio

**CP-MOD7-002**

| ID              | DescripciÃ³n                                                                                                                                                | Tipo   | Estado  | Defectos                    |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD7-002** | Verificar el comportamiento del sistema al enviar una tarea sin registrar comentario, validando si el comentario es obligatorio dentro del flujo de envÃ­o. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                                       | Resultado obtenido                                                                                                                                                                       |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir enviar la tarea sin comentario si el comentario no es obligatorio, siempre que se complete la condiciÃ³n requerida sobre si la tarea estÃ¡ completamente mapeada. | El sistema permitiÃ³ enviar la tarea sin comentario despuÃ©s de seleccionar la opciÃ³n obligatoria sobre el estado de mapeo de la tarea, y redirigiÃ³ correctamente a la vista del proyecto. |

#### Evidencia CP-MOD7-002 â€” Comentario vacÃ­o sin opciÃ³n de mapeo seleccionada

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-002-01-comentario-vacio-sin-opcion-mapeo.png" alt="CP-MOD7-002 - Comentario vacÃ­o sin opciÃ³n de mapeo seleccionada" width="300">
</p>

Se observa que el campo de comentario se encuentra vacÃ­o y que el sistema solicita responder si la tarea estÃ¡ completamente mapeada antes de permitir el envÃ­o.

#### Evidencia CP-MOD7-002 â€” Comentario vacÃ­o con opciÃ³n de mapeo seleccionada

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-002-02-comentario-vacio-con-opcion-mapeo.png" alt="CP-MOD7-002 - Comentario vacÃ­o con opciÃ³n de mapeo seleccionada" width="300">
</p>

Se evidencia que, al seleccionar una opciÃ³n para indicar si la tarea estÃ¡ completamente mapeada, el sistema permite continuar con el envÃ­o aun cuando el comentario permanece vacÃ­o.

#### Evidencia CP-MOD7-002 â€” RedirecciÃ³n a la vista del proyecto

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-002-03-redireccion-vista-proyecto.png" alt="CP-MOD7-002 - RedirecciÃ³n a la vista del proyecto" width="650">
</p>

Se evidencia que el sistema procesÃ³ correctamente el envÃ­o de la tarea sin comentario obligatorio y redirigiÃ³ al usuario a la vista del proyecto.

### 7.3. Registrar comentario con formato Markdown bÃ¡sico

**CP-MOD7-003**

| ID              | DescripciÃ³n                                                                                               | Tipo   | Estado  | Defectos                    |
| :-------------- | :-------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD7-003** | Verificar que el sistema permita registrar un comentario con formato Markdown bÃ¡sico dentro de una tarea. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                    | Resultado obtenido                                                                                                                                   |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir ingresar un comentario con formato Markdown bÃ¡sico, mostrar una vista previa comprensible y registrar el comentario sin afectar la interfaz. | El sistema permitiÃ³ ingresar el comentario con formato Markdown, mostrÃ³ correctamente la vista previa y registrÃ³ el comentario sin errores visibles. |

#### Evidencia CP-MOD7-003 â€” Comentario Markdown ingresado

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-003-01-comentario-markdown-ingresado.png" alt="CP-MOD7-003 - Comentario Markdown ingresado" width="350">
</p>

Se observa que el usuario ingresÃ³ un comentario con formato Markdown bÃ¡sico en el campo de comentarios de la tarea.

#### Evidencia CP-MOD7-003 â€” Vista previa del formato Markdown

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-003-02-vista-previa-markdown.png" alt="CP-MOD7-003 - Vista previa Markdown" width="350">
</p>

Se evidencia que el sistema muestra una vista previa del contenido con formato Markdown, permitiendo verificar cÃ³mo se visualizarÃ¡ el comentario antes de enviarlo.

#### Evidencia CP-MOD7-003 â€” Comentario Markdown registrado correctamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-003-03-comentario-markdown-registrado.png" alt="CP-MOD7-003 - Comentario Markdown registrado" width="300">
</p>

Se evidencia que el sistema registrÃ³ correctamente el comentario con formato Markdown y lo mostrÃ³ en la secciÃ³n correspondiente de la tarea sin afectar la interfaz.

### 7.4. Registrar comentario mencionando a un usuario existente

**CP-MOD7-004**

| ID              | DescripciÃ³n                                                                                                                  | Tipo   | Estado                  | Defectos                    |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------- | :----- | :---------------------- | :-------------------------- |
| **CP-MOD7-004** | Verificar que el sistema permita registrar un comentario que incluya una menciÃ³n a un usuario existente mediante `@usuario`. | Manual | Exitoso con observaciÃ³n | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                                                                             | Resultado obtenido                                                                                                                                                                                                       |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir ingresar y registrar un comentario con menciÃ³n a un usuario existente. Si las notificaciones internas se encuentran habilitadas, el sistema debe generar una notificaciÃ³n para el usuario mencionado. | El sistema permitiÃ³ ingresar, previsualizar y registrar correctamente el comentario con menciÃ³n a un usuario existente. Sin embargo, durante la ejecuciÃ³n no se evidenciÃ³ una notificaciÃ³n in-app asociada a la menciÃ³n. |

#### Evidencia CP-MOD7-004 â€” Comentario con menciÃ³n ingresado

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-004-01-comentario-con-mencion-ingresado.png" alt="CP-MOD7-004 - Comentario con menciÃ³n ingresado" width="350">
</p>

Se observa que el usuario ingresÃ³ un comentario que incluye una menciÃ³n a un usuario existente mediante el formato `@usuario`.

#### Evidencia CP-MOD7-004 â€” Vista previa de la menciÃ³n

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-004-02-vista-previa-mencion.png" alt="CP-MOD7-004 - Vista previa de la menciÃ³n" width="300">
</p>

Se evidencia que el sistema permite visualizar el comentario con la menciÃ³n antes de enviarlo, sin afectar la interfaz.

#### Evidencia CP-MOD7-004 â€” Comentario con menciÃ³n registrado correctamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-004-03-comentario-con-mencion-registrado.png" alt="CP-MOD7-004 - Comentario con menciÃ³n registrado" width="300">
</p>

Se evidencia que el sistema registrÃ³ correctamente el comentario con menciÃ³n dentro de la tarea.

### 7.5. Registrar comentario con menciÃ³n inexistente

**CP-MOD7-005**

| ID              | DescripciÃ³n                                                                                                           | Tipo   | Estado  | Defectos                    |
| :-------------- | :-------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD7-005** | Verificar el comportamiento del sistema al registrar un comentario que contiene una menciÃ³n a un usuario inexistente. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                 | Resultado obtenido                                                                                                                                         |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir registrar el comentario sin romper la interfaz. La menciÃ³n inexistente no debe resolverse como enlace ni generar una notificaciÃ³n vÃ¡lida. | El sistema permitiÃ³ registrar el comentario correctamente. La menciÃ³n inexistente se mostrÃ³ como texto plano y no se evidenciÃ³ generaciÃ³n de notificaciÃ³n. |

#### Evidencia CP-MOD7-005 â€” MenciÃ³n inexistente ingresada

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-005-01-mencion-inexistente-ingresada.png" alt="CP-MOD7-005 - MenciÃ³n inexistente ingresada" width="350">
</p>

Se observa que el usuario ingresÃ³ un comentario que incluye una menciÃ³n a un usuario inexistente.

#### Evidencia CP-MOD7-005 â€” Vista previa de menciÃ³n inexistente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-005-02-vista-previa-mencion-inexistente.png" alt="CP-MOD7-005 - Vista previa de menciÃ³n inexistente" width="350">
</p>

Se evidencia que el sistema permite previsualizar el comentario sin romper la interfaz, aun cuando la menciÃ³n no corresponde a un usuario existente.

#### Evidencia CP-MOD7-005 â€” Comentario con menciÃ³n inexistente registrado

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-005-03-comentario-mencion-inexistente-registrado.png" alt="CP-MOD7-005 - Comentario con menciÃ³n inexistente registrado" width="350">
</p>

Se evidencia que el sistema registrÃ³ correctamente el comentario. La menciÃ³n inexistente se mostrÃ³ como texto plano, por lo que no fue resuelta como enlace ni como referencia vÃ¡lida a un usuario del sistema.

### 7.6. VerificaciÃ³n de notificaciÃ³n in-app por menciÃ³n

**CP-MOD7-006**

| ID              | DescripciÃ³n                                                                                                         | Tipo   | Estado                    | Defectos                          |
| :-------------- | :------------------------------------------------------------------------------------------------------------------ | :----- | :------------------------ | :-------------------------------- |
| **CP-MOD7-006** | Verificar si el sistema muestra una notificaciÃ³n interna cuando un usuario es mencionado en un comentario de tarea. | Manual | Ejecutado con observaciÃ³n | No se confirmÃ³ defecto funcional. |

| Resultado esperado                                                                                                                                                                                          | Resultado obtenido                                                                                                                                                      |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe mostrar una notificaciÃ³n in-app para el usuario mencionado cuando se registra un comentario con una menciÃ³n vÃ¡lida, siempre que las notificaciones se encuentren habilitadas en el entorno. | Se revisÃ³ el Ã¡rea de notificaciones despuÃ©s de registrar una menciÃ³n vÃ¡lida, pero no se evidenciÃ³ una notificaciÃ³n visible asociada a la menciÃ³n dentro de la interfaz. |

#### Evidencia CP-MOD7-006 â€” Panel de notificaciones revisado

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-006-01-panel-notificaciones-revisado.png" alt="CP-MOD7-006 - Panel de notificaciones revisado" width="300">
</p>

Se observa el Ã¡rea de notificaciones del sistema revisada despuÃ©s de haber registrado previamente un comentario con menciÃ³n a un usuario existente.

#### Evidencia CP-MOD7-006 â€” MenciÃ³n no visible en notificaciones

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-006-02-mencion-no-visible-en-notificaciones.png" alt="CP-MOD7-006 - MenciÃ³n no visible en notificaciones" width="400">
</p>

Se evidencia que la menciÃ³n registrada en el comentario no aparece como notificaciÃ³n visible en el panel de notificaciones durante la ejecuciÃ³n realizada.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la prueba se verificÃ³ que la menciÃ³n a un usuario existente fue registrada correctamente en el comentario de la tarea; sin embargo, no se evidenciÃ³ una notificaciÃ³n in-app asociada a dicha menciÃ³n. Este comportamiento queda registrado como observaciÃ³n, ya que puede depender de la configuraciÃ³n de notificaciones, preferencias del usuario, sesiÃ³n del destinatario o condiciones propias del entorno local de pruebas.

### 7.7. Verificar acceso al panel de notificaciones

**CP-MOD7-007**

| ID              | DescripciÃ³n                                                                                                    | Tipo   | Estado  | Defectos                    |
| :-------------- | :------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD7-007** | Verificar que el usuario pueda acceder al panel de notificaciones y que este cargue correctamente sin errores. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                 | Resultado obtenido                                                                                                                                       |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir acceder al Ã¡rea de notificaciones y mostrar el panel correspondiente sin errores, independientemente de si existen notificaciones nuevas. | El sistema permitiÃ³ acceder correctamente al panel de notificaciones. El panel cargÃ³ sin errores visibles, aunque no se mostraron notificaciones nuevas. |

#### Evidencia CP-MOD7-007 â€” Acceso al panel de notificaciones

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-007-01-acceso-panel-notificaciones.png" alt="CP-MOD7-007 - Acceso al panel de notificaciones" width="350">
</p>

Se observa que el usuario accede al Ã¡rea o panel de notificaciones desde la interfaz del sistema.

#### Evidencia CP-MOD7-007 â€” Panel de notificaciones cargado correctamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-007-02-panel-notificaciones-cargado.png" alt="CP-MOD7-007 - Panel de notificaciones cargado correctamente" width="350">
</p>

Se evidencia que el panel de notificaciones carga correctamente y no presenta errores tÃ©cnicos visibles durante la consulta.

### 7.8. ReenvÃ­o de correo de validaciÃ³n desde el perfil de usuario

**CP-MOD7-008**

| ID              | DescripciÃ³n                                                                                                                      | Tipo   | Estado                    | Defectos                          |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------- | :----- | :------------------------ | :-------------------------------- |
| **CP-MOD7-008** | Verificar el comportamiento del sistema al solicitar el reenvÃ­o del correo electrÃ³nico de validaciÃ³n desde el perfil de usuario. | Manual | Ejecutado con observaciÃ³n | No se confirmÃ³ defecto funcional. |

| Resultado esperado                                                                                                                                                                                      | Resultado obtenido                                                                                                                                                                                            |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| El sistema debe permitir solicitar el reenvÃ­o del correo de validaciÃ³n. Si el entorno de correo se encuentra correctamente configurado, el usuario deberÃ­a recibir el mensaje en su bandeja de entrada. | El sistema mostrÃ³ el correo electrÃ³nico del usuario e indicÃ³ que se debÃ­a revisar la cuenta para confirmar la direcciÃ³n. Sin embargo, durante la ejecuciÃ³n no se recibiÃ³ el correo en la bandeja del usuario. |

#### Evidencia CP-MOD7-008 â€” Correo electrÃ³nico pendiente de validaciÃ³n

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-008-01-correo-electronico-pendiente-validacion.png" alt="CP-MOD7-008 - Correo electrÃ³nico pendiente de validaciÃ³n" width="400">
</p>

Se observa que el sistema muestra el correo electrÃ³nico asociado al usuario y solicita confirmar la direcciÃ³n mediante un correo de validaciÃ³n.

#### Evidencia CP-MOD7-008 â€” Correo no recibido en bandeja del usuario

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-008-02-correo-no-recibido.png" alt="CP-MOD7-008 - Correo no recibido" width="400">
</p>

Se evidencia que, durante la ejecuciÃ³n de la prueba, no se recibiÃ³ el correo de validaciÃ³n en la bandeja del usuario.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la prueba se verificÃ³ que la interfaz informa al usuario que debe confirmar su correo electrÃ³nico. Sin embargo, no se pudo confirmar la recepciÃ³n del mensaje en la bandeja de entrada. Este resultado queda registrado como observaciÃ³n, debido a que el envÃ­o real de correos puede depender de variables de entorno o servicios externos no habilitados en el entorno local de pruebas.

### 7.9. Registrar comentario usando etiquetas de grupo

**CP-MOD7-009**

| ID              | DescripciÃ³n                                                                                                     | Tipo   | Estado  | Defectos                    |
| :-------------- | :-------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD7-009** | Verificar que el sistema permita registrar un comentario que incluya una etiqueta de grupo dentro de una tarea. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                  | Resultado obtenido                                                                                                                                   |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir ingresar un comentario con una etiqueta de grupo, registrarlo correctamente y mostrarlo en la secciÃ³n de comentarios sin errores visibles. | El sistema permitiÃ³ ingresar y registrar correctamente el comentario con etiqueta de grupo dentro de la tarea, sin presentar errores en la interfaz. |

#### Evidencia CP-MOD7-009 â€” Comentario con etiqueta de grupo ingresado

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-009-01-comentario-con-etiqueta-grupo-ingresado.png" alt="CP-MOD7-009 - Comentario con etiqueta de grupo ingresado" width="400">
</p>

Se observa que el usuario ingresÃ³ un comentario utilizando una etiqueta de grupo disponible en el editor de comentarios.

#### Evidencia CP-MOD7-009 â€” Vista previa de etiqueta de grupo

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-009-02-vista-previa-etiqueta-grupo.png" alt="CP-MOD7-009 - Vista previa de etiqueta de grupo" width="400">
</p>

Se evidencia que el sistema permite previsualizar el comentario con la etiqueta de grupo antes de enviarlo.

#### Evidencia CP-MOD7-009 â€” Comentario con etiqueta de grupo registrado correctamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-009-03-comentario-etiqueta-grupo-registrado.png" alt="CP-MOD7-009 - Comentario con etiqueta de grupo registrado" width="400">
</p>

Se evidencia que el comentario con etiqueta de grupo fue registrado correctamente en la secciÃ³n de comentarios de la tarea, sin errores visibles en la interfaz.

### 7.10. Registrar comentario extenso en una tarea

**CP-MOD7-010**

| ID              | DescripciÃ³n                                                                                                   | Tipo   | Estado  | Defectos                    |
| :-------------- | :------------------------------------------------------------------------------------------------------------ | :----- | :------ | :-------------------------- |
| **CP-MOD7-010** | Verificar que el sistema permita registrar un comentario extenso dentro de una tarea sin afectar la interfaz. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                         | Resultado obtenido                                                                                                                              |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir ingresar, previsualizar y registrar un comentario extenso dentro de una tarea, manteniendo la legibilidad del contenido y sin romper la interfaz. | El sistema permitiÃ³ ingresar y registrar correctamente el comentario extenso dentro de la tarea, sin presentar errores visibles en la interfaz. |

#### Evidencia CP-MOD7-010 â€” Comentario extenso ingresado

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-010-01-comentario-extenso-ingresado.png" alt="CP-MOD7-010 - Comentario extenso ingresado" width="400">
</p>

Se observa que el usuario ingresÃ³ un comentario extenso en el campo de comentarios de la tarea.

#### Evidencia CP-MOD7-010 â€” Vista previa del comentario extenso

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-010-02-vista-previa-comentario-extenso.png" alt="CP-MOD7-010 - Vista previa comentario extenso" width="400">
</p>

Se evidencia que el sistema permite revisar la vista previa del comentario extenso antes de enviarlo, manteniendo una visualizaciÃ³n comprensible del contenido.

#### Evidencia CP-MOD7-010 â€” Comentario extenso registrado correctamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0007-comunicacion-notificaciones/CP-MOD7-010-03-comentario-extenso-registrado.png" alt="CP-MOD7-010 - Comentario extenso registrado" width="400">
</p>

Se evidencia que el sistema registrÃ³ correctamente el comentario extenso dentro de la secciÃ³n de comentarios de la tarea, sin errores visibles ni pÃ©rdida de contenido.

