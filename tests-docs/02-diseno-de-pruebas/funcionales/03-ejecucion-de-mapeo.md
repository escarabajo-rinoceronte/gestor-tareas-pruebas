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
  <b>Proyecto:</b> HOT Tasking Manager — DiseÃ±o de Pruebas Funcionales: MOD-03 - EjecuciÃ³n de Mapeo (Tasking) <br>
  <b>Fecha de Elaboración:</b> 12/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# DiseÃ±o de Pruebas Funcionales: MOD-03 - EjecuciÃ³n de Mapeo (Tasking)
**VersiÃ³n del Documento:** 1.0
**Tipo de AnÃ¡lisis:** DiseÃ±o de Pruebas de Sistema (Caja Negra)

---

## 1. Contexto del MÃ³dulo

Este mÃ³dulo gestiona el flujo de trabajo central de contribuciÃ³n geogrÃ¡fica de la plataforma. Es responsable de coordinar la selecciÃ³n, el bloqueo exclusivo, la interacciÃ³n con herramientas de ediciÃ³n (tanto basadas en la web como locales) y la liberaciÃ³n o actualizaciÃ³n de estado de las tareas dentro de un proyecto. Su propÃ³sito principal es garantizar la concurrencia segura de mÃºltiples usuarios, previniendo colisiones de ediciÃ³n y asegurando la correcta evoluciÃ³n del progreso de mapeo del proyecto.

*Para consultar el detalle exhaustivo de los actores, restricciones y reglas de negocio, referirse al [CatÃ¡logo de Requerimientos Funcionales](/tests-docs/02-diseno-de-pruebas/funcionales/00-requerimientos-funcionales.md).*

---

## 2. Estrategia de DiseÃ±o de Pruebas

### 2.1. Enfoque general

El enfoque de pruebas para este mÃ³dulo serÃ¡ de extremo a extremo (End-to-End) desde la perspectiva del comportamiento observable en la interfaz de usuario. Las pruebas se centrarÃ¡n en validar el ciclo de vida completo de una tarea geogrÃ¡fica, tomando como protagonista al actor **`MAPPER` (ACT-0002)**, dado que es el rol principal de ejecuciÃ³n de este flujo. 

Se evaluarÃ¡ rigurosamente la reactividad del sistema frente a restricciones de acceso (licencias previas, exclusividad de bloqueos), el comportamiento de la interfaz al invocar editores cartogrÃ¡ficos externos (validaciÃ³n de URLs generadas o detecciÃ³n de servicios locales) y la correcta respuesta visual tras el envÃ­o de resultados. De manera complementaria, se modelarÃ¡ la intervenciÃ³n del actor **`Sistema` (ACT-0006)** para auditar los flujos de liberaciÃ³n automÃ¡tica por expiraciÃ³n de tiempo.

### 2.2. TÃ©cnicas de Caja Negra Utilizadas

Para garantizar una cobertura Ã³ptima y reducir la redundancia en los casos de prueba, se aplicarÃ¡n las siguientes metodologÃ­as de diseÃ±o:

*   **ParticiÃ³n de Equivalencia (Equivalence Partitioning):** Utilizada para evaluar las restricciones de acceso y selecciÃ³n de herramientas. Se agruparÃ¡n en clases representativas las condiciones de los proyectos (por ejemplo, Proyectos que requieren nivel `BEGINNER` vs `ADVANCED`), los tipos de editores configurados (Editores Web como iD/Rapid vs Editores Locales como JOSM), y el estado legal del usuario (Licencia aceptada vs No aceptada).
*   **AnÃ¡lisis de Valores LÃ­mite (Boundary Value Analysis):** Se aplicarÃ¡ especÃ­ficamente para validar las reglas de negocio dependientes de variables numÃ©ricas extremas, como los lÃ­mites de zoom topogrÃ¡fico al intentar dividir (Split) una tarea, y el umbral de tiempo lÃ­mite (`autoUnlockSeconds`) para la liberaciÃ³n automÃ¡tica de una tarea bloqueada.
*   **Tablas de DecisiÃ³n (Decision Table Testing):** Se utilizarÃ¡ para modelar combinaciones de reglas de negocio complejas antes de permitir el bloqueo de una tarea. CombinarÃ¡ mÃºltiples entradas binarias (por ejemplo, *Â¿Tiene el usuario otra tarea bloqueada?*, *Â¿Cumple con el nivel de mapeo?*, *Â¿El proyecto estÃ¡ publicado?*) para determinar la salida correcta esperada en la interfaz (habilitaciÃ³n del botÃ³n de mapeo o visualizaciÃ³n de un error especÃ­fico).
*   **TransiciÃ³n de Estados (State Transition Testing):** Esta es la tÃ©cnica principal del mÃ³dulo, ya que el modelo funcional depende intrÃ­nsecamente del ciclo de vida de una tarea. Se utilizarÃ¡ para validar que los cambios de estado (por ejemplo, de `READY` a `LOCKED_FOR_MAPPING`, y posteriormente a `MAPPED` o `BADIMAGERY`) sigan estrictamente las transiciones permitidas por la interfaz, incluyendo las reversiones (Undo).
## 3. Especificaciones de Escenarios y Casos de Prueba

Para asegurar una cobertura funcional completa del mÃ³dulo **MOD-03: EjecuciÃ³n de Mapeo (Tasking)** sin redundancia, se proponen **5 Especificaciones de Escenarios de Prueba (ESC)**. 

El mÃ³dulo 3 contiene flujos transaccionales altamente acoplados. Dividirlo en 5 escenarios permite aislar las lÃ³gicas de negocio utilizando la tÃ©cnica de caja negra mÃ¡s adecuada para cada una:
1. Permisos y precondiciones de entrada (Tabla de DecisiÃ³n).
2. Salida, restricciones preventivas en la UI y cambio de estado de la tarea (TransiciÃ³n de Estados).
3. GeometrÃ­a y lÃ­mites matemÃ¡ticos de la plataforma (AnÃ¡lisis de Valores LÃ­mite).
4. Acciones automatizadas del sistema y control de tiempo de sesiÃ³n (AnÃ¡lisis de Valores LÃ­mite).
5. InteracciÃ³n grÃ¡fica espacial y filtrado de auditorÃ­a visual (ParticiÃ³n de Equivalencia).

| ID Escenario | DescripciÃ³n Breve | RF Cubiertos | Alcance Funcional | TÃ©cnica Principal |
| :--- | :--- | :--- | :--- | :--- |
| **ESC-3001** | **Bloqueo e inicio de tarea** | RF-3001, RF-3002, RF-3003 | Verifica si el usuario (`MAPPER`) puede tomar una tarea basado en permisos, licencias, exclusividad y selecciona un editor. | Tabla de DecisiÃ³n, ParticiÃ³n de Equivalencia |
| **ESC-3002** | **LiberaciÃ³n y envÃ­o de tarea (Submit)** | RF-3004 | Cubre la finalizaciÃ³n del mapeo y las restricciones preventivas en la interfaz para evitar transiciones de estado no permitidas. | TransiciÃ³n de Estados, ParticiÃ³n de Equivalencia |
| **ESC-3003** | **DivisiÃ³n de tarea (Split)** | RF-3005 | EvalÃºa la capacidad de fraccionar una grilla de mapeo basÃ¡ndose en el lÃ­mite del nivel de zoom cartogrÃ¡fico. | AnÃ¡lisis de Valores LÃ­mite, ParticiÃ³n de Equivalencia |
| **ESC-3004** | **ExpiraciÃ³n y extensiÃ³n de bloqueo** | RF-3006 | Valida la liberaciÃ³n forzada por el Sistema al exceder el lÃ­mite de tiempo y la solicitud de extensiÃ³n manual de la sesiÃ³n por el usuario. | AnÃ¡lisis de Valores LÃ­mite, ParticiÃ³n de Equivalencia |
| **ESC-3005** | **InteracciÃ³n CartogrÃ¡fica y Trazabilidad** | RF-3002, RF-7001 | Valida la respuesta del editor integrado frente a la navegaciÃ³n (dentro y fuera del BBOX) y el filtrado del panel de historial. | ParticiÃ³n de Equivalencia |

### 3.1. Escenario: [ESC-3001] - Solicitud de Bloqueo e Inicio de Tarea de Mapeo

**A. DefiniciÃ³n del Escenario**

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el sistema permite a un usuario `MAPPER` obtener el bloqueo exclusivo de una tarea para su ediciÃ³n, evaluando de forma concurrente las reglas de negocio restrictivas y ejecutando correctamente el editor cartogrÃ¡fico seleccionado. |
| **RF Asociados** | RF-3001, RF-3002, RF-3003 |
| **Precondiciones** | Proyecto en estado `PUBLISHED`. Usuario `MAPPER` (ACT-0002) autenticado en el sistema. |
| **TÃ©cnicas aplicadas**| Tabla de DecisiÃ³n, ParticiÃ³n de Equivalencia. |
| **Resultado Esperado** | El sistema otorga el bloqueo de la tarea (`LOCKED_FOR_MAPPING`) y lanza el editor correspondiente, o en su defecto, deniega la acciÃ³n mostrando el mensaje de error especÃ­fico segÃºn la regla de negocio infringida. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**

**B.1. Tabla de DecisiÃ³n**
Se aplica esta tÃ©cnica para modelar las reglas de negocio combinadas que el sistema evalÃºa antes de otorgar el bloqueo de una tarea. Se ha racionalizado la tabla utilizando guiones (`-`) para denotar condiciones "indiferentes" una vez que una restricciÃ³n principal de mayor jerarquÃ­a ya ha invalidado el flujo.

| Condiciones de entrada | | | | | |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Nivel de mapeo del usuario cumple con el requerido | V | V | V | V | F |
| Estado de la tarea seleccionada es `READY` | V | V | V | F | - |
| Usuario no posee otras tareas bloqueadas actualmente | V | V | F | - | - |
| TÃ©rminos de licencia del proyecto aceptados | V | F | - | - | - |
| **Condiciones de salida** | | | | | |
| Bloqueo exitoso (`LOCKED_FOR_MAPPING`) | V | F | F | F | F |
| Error: Licencia no aceptada (*UserLicenseError*) | F | V | F | F | F |
| Error: LÃ­mite de tareas excedido (*UserAlreadyHasTaskLocked*) | F | F | V | F | F |
| Error: Estado invÃ¡lido de tarea (*InvalidTaskState*) | F | F | F | V | F |
| Error: Nivel insuficiente (*UserPermissionError*) | F | F | F | F | V |
| **Etiqueta** | **A** | **B** | **C** | **D** | **E** |

*(Nota: La Etiqueta A representa el "Happy Path" del proceso de validaciÃ³n de bloqueo).*

**B.2. ParticiÃ³n de Equivalencia**
Una vez superadas las validaciones de bloqueo, el sistema procesa el lanzamiento del editor seleccionado por el usuario. Se aplica esta tÃ©cnica para agrupar los tipos de editores soportados y su comportamiento esperado.

| Cod. | Campo | Clase VÃ¡lida | Clases No VÃ¡lidas |
| :--- | :--- | :--- | :--- |
| MOD03-PE-001 | Tipo de Editor | Editores Web (por ejemplo, `iD`, `RAPID`), Editores Locales (por ejemplo, `JOSM`) | Cadena vacÃ­a, Editor no soportado (por ejemplo, `CustomApp`) |

*   *Comportamiento esperado (Editores Web):* El sistema redirecciona o carga el iframe embebido con los parÃ¡metros BBOX de la tarea.
*   *Comportamiento esperado (Editores Locales):* El sistema emite una peticiÃ³n `GET` a `127.0.0.1:8111`. Si no hay respuesta, se genera error de conexiÃ³n local.
*   *Comportamiento esperado (Clases No VÃ¡lidas):* El sistema aplica un *fallback* y carga el editor web por defecto (`iD`).

**C. Casos de Prueba Derivados**

| ID Caso | Datos de entrada o escenario | Resultado Esperado | TÃ©cnicas / Etiquetas Aplicadas |
| :--- | :--- | :--- | :--- |
| **CP-3001-01** | Nivel OK, Tarea `READY`, Sin bloqueos previos, Licencia OK.<br>Editor: `iD` (Web). | La tarea cambia a `LOCKED_FOR_MAPPING`. Se carga la interfaz del editor iD correctamente. | Tabla de DecisiÃ³n (A)<br>PE (Clase VÃ¡lida Web) |
| **CP-3001-02** | Nivel OK, Tarea `READY`, Sin bloqueos previos, Licencia OK.<br>Editor: `JOSM` (Local, servicio en puerto 8111 apagado). | Alerta de interfaz indicando "JOSM is not running". La tarea mantiene el bloqueo otorgado. | Tabla de DecisiÃ³n (A)<br>PE (Clase VÃ¡lida Local) |
| **CP-3001-03** | Nivel OK, Tarea `READY`, Sin bloqueos previos, Licencia: No aceptada. | Se muestra modal impidiendo el bloqueo y requiriendo aceptaciÃ³n de "Terms of Use" (`UserLicenseError`). | Tabla de DecisiÃ³n (B) |
| **CP-3001-04** | Nivel OK, Tarea `READY`, Tareas previas bloqueadas: 1, Licencia OK. | Se muestra mensaje de error indicando lÃ­mite de concurrencia excedido (`UserAlreadyHasTaskLocked`). | Tabla de DecisiÃ³n (C) |
| **CP-3001-05** | Nivel OK, Tarea `MAPPED`, Sin bloqueos previos, Licencia OK. | Se muestra mensaje de error indicando estado invÃ¡lido para mapeo (`InvalidTaskState`). | Tabla de DecisiÃ³n (D) |
| **CP-3001-06** | Nivel Usuario: `BEGINNER`<br>Nivel Proyecto: `ADVANCED`<br>Resto de parÃ¡metros vÃ¡lidos. | Se muestra mensaje de error de permisos denegados (`UserPermissionError`). | Tabla de DecisiÃ³n (E) |
| **CP-3001-07** | Nivel OK, Tarea `READY`, Sin bloqueos previos, Licencia OK.<br>Editor: `(VacÃ­o)` | La tarea cambia a `LOCKED_FOR_MAPPING`. El sistema carga el editor `iD` por defecto. | Tabla de DecisiÃ³n (A)<br>PE (Clase No VÃ¡lida) |


### 3.2. Escenario: [ESC-3002] - LiberaciÃ³n y EnvÃ­o de Tarea de Mapeo (Submit)

**A. DefiniciÃ³n del Escenario**

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que la interfaz grÃ¡fica permite a un usuario `MAPPER` finalizar su sesiÃ³n de mapeo sobre una tarea que posee bloqueada, reportando el progreso mediante las opciones visibles en el panel de control y liberando el bloqueo exclusivo. Asimismo, validar que la interfaz restringe visualmente estas opciones cuando la tarea no cumple las condiciones para ser liberada. |
| **RF Asociados** | RF-3004 |
| **Precondiciones** | Proyecto en estado `PUBLISHED`. Usuario `MAPPER` (ACT-0002) autenticado en el sistema. |
| **TÃ©cnicas aplicadas**| TransiciÃ³n de Estados (State Transition Testing), ParticiÃ³n de Equivalencia (PE). |
| **Resultado Esperado** | La interfaz muestra los controles de finalizaciÃ³n ("Yes", "No") Ãºnicamente cuando el usuario posee el bloqueo de la tarea. Al confirmar, la tarea actualiza su color/estado topogrÃ¡fico en el mapa (`MAPPED` o `READY`). Para tareas ajenas o sin bloqueo, los controles de envÃ­o se ocultan. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**

**B.1. TransiciÃ³n de Estados**
Se modelan exclusivamente los estados visuales del mapa y los controles de la interfaz que provocan las transiciones disponibles para el usuario al momento de liberar la tarea.

![Diagrama de transiciÃ³n ESC-3002](/tests-docs/02-diseno-de-pruebas/funcionales/img/transicion-estado-ESC-3002.png) 

**Tabla de TransiciÃ³n de Estados (Observable en UI)**

| Estado Inicial UI | AcciÃ³n en Interfaz | Estado Final Esperado (UI) | TransiciÃ³n |
| :--- | :--- | :--- | :---: |
| Tarea `LOCKED_FOR_MAPPING` (Titular) | Seleccionar "Yes" (Mapeo completo) y "Submit" | Tarea cambia a color de `MAPPED`. Panel vuelve a estado inactivo. | VÃ¡lida |
| Tarea `LOCKED_FOR_MAPPING` (Titular) | Seleccionar "No" (Mapeo incompleto) y "Submit" | Tarea cambia a color de `READY` (blanco/transparente). | VÃ¡lida |

**B.2. ParticiÃ³n de Equivalencia (PE)**
La interfaz de usuario debe reaccionar y adaptarse (mostrando u ocultando el panel de "Submit") basÃ¡ndose en el estado previo de la tarea seleccionada y en quiÃ©n ostenta la propiedad del bloqueo.

| Cod. | Variable Analizada en UI | Clase VÃ¡lida (Muestra panel de Submit) | Clases No VÃ¡lidas (Oculta panel de Submit) |
| :--- | :--- | :--- | :--- |
| **MOD03-PE-002** | Estado de la tarea y titularidad del bloqueo visual | Tarea seleccionada estÃ¡ `LOCKED_FOR_MAPPING` y el usuario actual es el titular. | 1. Tarea en estado `READY` (Libre).<br>2. Tarea en `LOCKED_FOR_MAPPING` por otro usuario (Aparece "Locked by [User]").<br>3. Tarea ya finalizada (`MAPPED`, `VALIDATED`). |

*   *Comportamiento esperado (Clase VÃ¡lida):* El panel lateral renderiza la pregunta "Â¿EstÃ¡ la tarea completamente mapeada?" con las opciones de envÃ­o.
*   *Comportamiento esperado (Clases No VÃ¡lidas):* La interfaz actÃºa como barrera preventiva. No renderiza los radio buttons ni el botÃ³n de "Submit Task". En su lugar, muestra botones acordes al estado (por ejemplo, "Map a task" o solo informaciÃ³n).

**C. Casos de Prueba Derivados**

| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada / Contexto | Resultado Esperado | TÃ©cnicas / Etiquetas Aplicadas |
| :--- | :--- | :--- | :--- | :--- |
| **CP-3002-01** | 1. Seleccionar tarea bloqueada propia.<br>2. Marcar "Yes".<br>3. Clic en "Submit Task". | **Estado:** `LOCKED_FOR_MAPPING` (Propia) | El panel de mapeo se cierra. La tarea se pinta con el color correspondiente a `MAPPED`. El bloqueo visual desaparece. | TransiciÃ³n de Estados (VÃ¡lida)<br>PE (Clase VÃ¡lida) |
| **CP-3002-02** | 1. Seleccionar tarea bloqueada propia.<br>2. Marcar "No".<br>3. Clic en "Submit Task". | **Estado:** `LOCKED_FOR_MAPPING` (Propia) | El panel de mapeo se cierra. La tarea se pinta con el color correspondiente a `READY`. Queda disponible en el mapa. | TransiciÃ³n de Estados (VÃ¡lida)<br>PE (Clase VÃ¡lida) |
| **CP-3002-03** | 1. Hacer clic sobre una tarea libre en el mapa de exploraciÃ³n. | **Estado:** `READY` | El panel lateral muestra informaciÃ³n de la tarea y el botÃ³n "Map Task". **No se muestran** las opciones de "Submit", previniendo un envÃ­o sin bloqueo. | PE (Clase No VÃ¡lida) |
| **CP-3002-04** | 1. Hacer clic sobre una tarea bloqueada por un tercero (candado rojo). | **Estado:** `LOCKED_FOR_MAPPING` (Ajena) | El panel lateral indica "Locked by [Usuario]". **No se muestran** las opciones de "Submit" ni de ediciÃ³n, protegiendo la autorÃ­a del mapeo. | PE (Clase No VÃ¡lida) |
| **CP-3002-05** | 1. Hacer clic sobre una tarea que ya ha sido mapeada por el usuario. | **Estado:** `MAPPED` | El panel lateral refleja que la tarea espera validaciÃ³n. **No se muestran** los controles de "Submit" de mapeo. | PE (Clase No VÃ¡lida) |

### 3.3. Escenario: [ESC-3003] - DivisiÃ³n de Tarea de Mapeo (Split Task)

**A. DefiniciÃ³n del Escenario**

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el sistema permite a un usuario `MAPPER` fraccionar una tarea (actualmente bloqueada por Ã©l) en 4 sub-tareas mÃ¡s pequeÃ±as, siempre y cuando la escala del Ã¡rea (zoom cartogrÃ¡fico) no supere el lÃ­mite mÃ¡ximo permitido por la plataforma para evitar micro-tareas inmanejables. |
| **RF Asociados** | RF-3005 |
| **Precondiciones** | Proyecto en estado `PUBLISHED`. Usuario `MAPPER` (ACT-0002) autenticado en el sistema. Tarea seleccionada en estado `LOCKED_FOR_MAPPING`. |
| **TÃ©cnicas aplicadas**| AnÃ¡lisis de Valores LÃ­mite (AVL), ParticiÃ³n de Equivalencia (PE). |
| **Resultado Esperado** | Si se cumplen las reglas geogrÃ¡ficas y de propiedad, el sistema divide la tarea original en 4 nuevas tareas, eliminando la original e incrementando el total de tareas del proyecto en 3. De lo contrario, se rechaza la acciÃ³n con un mensaje de error especÃ­fico. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**

**B.1. AnÃ¡lisis de Valores LÃ­mite (AVL)**
La capacidad de dividir una tarea estÃ¡ restringida matemÃ¡ticamente por el nivel de zoom cartogrÃ¡fico (escala del mapa). Si una tarea ya es demasiado pequeÃ±a, dividirla generarÃ­a polÃ­gonos no funcionales. El lÃ­mite mÃ¡ximo admitido para aplicar un *Split* es un zoom level igual a `17`. Un nivel de zoom `18` o superior se considera demasiado pequeÃ±o.

| Cod. | Variable a Evaluar | LÃ­mite Superior VÃ¡lido | LÃ­mite Superior InvÃ¡lido | ObservaciÃ³n |
| :--- | :--- | :--- | :--- | :--- |
| **MOD03-AVL-001** | Nivel de Zoom de la Tarea | `17` | `18` | EvalÃºa la frontera exacta donde el sistema bloquea la operaciÃ³n matemÃ¡tica de divisiÃ³n cartogrÃ¡fica. |

**B.2. ParticiÃ³n de Equivalencia (PE)**
Al igual que en la liberaciÃ³n de tareas, la divisiÃ³n es una operaciÃ³n destructiva (elimina el polÃ­gono original), por lo que requiere una estricta validaciÃ³n de estado y propiedad del bloqueo actual.

| Cod. | CondiciÃ³n Analizada | Clase VÃ¡lida | Clases No VÃ¡lidas |
| :--- | :--- | :--- | :--- |
| **MOD03-PE-003** | Estado y AutorÃ­a de la Tarea | Tarea en estado `LOCKED_FOR_MAPPING` cuyo `lockHolder` (titular) coincide con el usuario que emite la peticiÃ³n. | 1. Tarea en cualquier otro estado (por ejemplo, `READY`, `MAPPED`).<br>2. Tarea en `LOCKED_FOR_MAPPING` pero con un `lockHolder` diferente al solicitante. |

*   *Comportamiento esperado (Clase VÃ¡lida):* EjecuciÃ³n exitosa de la funciÃ³n `splitTaskGrid`.
*   *Comportamiento esperado (Clases No VÃ¡lidas):* Rechazo de la solicitud indicando `LockToSplit` (para estado incorrecto) o `SplitOtherUserTask` (para titular distinto).

**C. Casos de Prueba Derivados**

| ID Caso | Datos de entrada o escenario | Resultado Esperado | TÃ©cnicas / Etiquetas Aplicadas |
| :--- | :--- | :--- | :--- |
| **CP-3003-01** | **Zoom de Tarea:** `17`<br>**Estado:** `LOCKED_FOR_MAPPING`<br>**Titular:** Solicitante actual | El sistema procesa la divisiÃ³n. La tarea original desaparece. Se generan 4 tareas nuevas. El contador `total_tasks` aumenta en 3. | MOD03-AVL-001 (VÃ¡lido)<br>MOD03-PE-003 (VÃ¡lido) |
| **CP-3003-02** | **Zoom de Tarea:** `18`<br>**Estado:** `LOCKED_FOR_MAPPING`<br>**Titular:** Solicitante actual | El sistema aborta la transacciÃ³n espacial. Se emite el mensaje de error: `SmallToSplit`. La tarea original se mantiene intacta. | MOD03-AVL-001 (InvÃ¡lido)<br>MOD03-PE-003 (VÃ¡lido) |
| **CP-3003-03** | **Zoom de Tarea:** `15`<br>**Estado:** `READY`<br>**Titular:** Ninguno | El sistema rechaza la peticiÃ³n por estado invÃ¡lido, emitiendo el error: `LockToSplit`. | MOD03-AVL-001 (VÃ¡lido)<br>MOD03-PE-003 (No VÃ¡lido) |
| **CP-3003-04** | **Zoom de Tarea:** `16`<br>**Estado:** `LOCKED_FOR_MAPPING`<br>**Titular:** Usuario B (Diferente al solicitante actual) | El sistema rechaza la peticiÃ³n por conflicto de propiedad, emitiendo el error: `SplitOtherUserTask`. | MOD03-AVL-001 (VÃ¡lido)<br>MOD03-PE-003 (No VÃ¡lido) |

### 3.4. Escenario: [ESC-3004] - ExpiraciÃ³n y ExtensiÃ³n de Bloqueo de Tarea (Auto-unlock / Extend)

**A. DefiniciÃ³n del Escenario**

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el sistema libera automÃ¡ticamente una tarea bloqueada al expirar su tiempo lÃ­mite de ediciÃ³n para prevenir el acaparamiento de tareas (operaciÃ³n del Sistema). Adicionalmente, validar que un `MAPPER` pueda solicitar una extensiÃ³n explÃ­cita de su tiempo de bloqueo antes de que este caduque. |
| **RF Asociados** | RF-3006 |
| **Precondiciones** | Proyecto en estado `PUBLISHED`. Tarea en estado `LOCKED_FOR_MAPPING`. Usuario `MAPPER` (ACT-0002) autenticado (para extensiones). Cron de expiraciÃ³n de tareas (ACT-0006) activo. |
| **TÃ©cnicas aplicadas**| AnÃ¡lisis de Valores LÃ­mite (AVL), ParticiÃ³n de Equivalencia (PE). |
| **Resultado Esperado** | Si el tiempo transcurrido supera el umbral configurado, la tarea vuelve a `READY`. Si el usuario solicita una extensiÃ³n bajo condiciones vÃ¡lidas, el temporizador se reinicia; de lo contrario, la extensiÃ³n es denegada con el error correspondiente. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**

**B.1. AnÃ¡lisis de Valores LÃ­mite (AVL)**
La liberaciÃ³n de la tarea depende de un umbral temporal (`autoUnlockSeconds`, tÃ­picamente 2 horas / 7200 segundos). Se evalÃºa el lÃ­mite de expiraciÃ³n, donde `L` es el lÃ­mite de tiempo y `T` es el tiempo transcurrido desde que se bloqueÃ³ la tarea.

| Cod. | Campo / CondiciÃ³n Evaluada | LÃ­mite Inferior (VÃ¡lido) | LÃ­mite Exacto (No VÃ¡lido) | LÃ­mite Superior (No VÃ¡lido) | ObservaciÃ³n |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MOD03-AVL-002** | Tiempo transcurrido `T` vs `L` | `T = L - 1` segundo | `T = L` | `T = L + 1` segundo | EvalÃºa la frontera cronolÃ³gica donde el sistema debe revocar forzosamente el bloqueo del usuario. |

**B.2. ParticiÃ³n de Equivalencia (PE)**
Al solicitar una "ExtensiÃ³n del Bloqueo" (*Extend Session*), el sistema debe verificar el estado topogrÃ¡fico actual y la autorÃ­a del bloqueo para garantizar la seguridad de la operaciÃ³n.

| Cod. | Campo / CondiciÃ³n | Clase VÃ¡lida | Clases No VÃ¡lidas |
| :--- | :--- | :--- | :--- |
| **MOD03-PE-004** | Estado y Propiedad de la Tarea al extender | Tarea en estado `LOCKED_FOR_MAPPING` y el `lockHolder` (titular) coincide con el solicitante. | 1. Tarea no bloqueada (por ejemplo, `READY`, `MAPPED`).<br>2. Tarea en `LOCKED_FOR_MAPPING` pero asignada a otro usuario. |

*   *Comportamiento esperado (Clase VÃ¡lida):* El sistema reinicia el contador de tiempo y registra la acciÃ³n `EXTENDED_FOR_MAPPING` en el historial.
*   *Comportamiento esperado (Clases No VÃ¡lidas):* Rechazo de la solicitud indicando `TaskStatusNotLocked` (para estado incorrecto) o `LockedByAnotherUser` (para titular distinto).

**C. Casos de Prueba Derivados**

| ID Caso | Datos de entrada o escenario | Resultado Esperado | TÃ©cnicas / Etiquetas Aplicadas |
| :--- | :--- | :--- | :--- |
| **CP-3004-01** | EvaluaciÃ³n del sistema.<br>**Tiempo transcurrido:** `L - 1 segundo`. | La tarea conserva su estado `LOCKED_FOR_MAPPING`. No se revoca el acceso del usuario. | MOD03-AVL-002 (VÃ¡lido) |
| **CP-3004-02** | EvaluaciÃ³n del sistema.<br>**Tiempo transcurrido:** Igual a `L` o `L + 1 segundo`. | El sistema revoca el acceso. La tarea cambia a `READY`. El historial registra la acciÃ³n `AUTO_UNLOCKED_FOR_MAPPING`. | MOD03-AVL-002 (No VÃ¡lido) |
| **CP-3004-03** | Solicitud de ExtensiÃ³n.<br>**Estado:** `LOCKED_FOR_MAPPING`.<br>**Titular:** Coincide con solicitante. | OperaciÃ³n exitosa (HTTP 200). Retorna "Successfully extended task expiry". Historial registra `EXTENDED_FOR_MAPPING`. | MOD03-PE-004 (Clase VÃ¡lida) |
| **CP-3004-04** | Solicitud de ExtensiÃ³n.<br>**Estado:** `READY`. | OperaciÃ³n denegada (HTTP 403). Retorna el mensaje de error: `TaskStatusNotLocked`. | MOD03-PE-004 (Clase No VÃ¡lida) |
| **CP-3004-05** | Solicitud de ExtensiÃ³n.<br>**Estado:** `LOCKED_FOR_MAPPING`.<br>**Titular:** Usuario B (Diferente al solicitante). | OperaciÃ³n denegada (HTTP 403). Retorna el mensaje de error: `LockedByAnotherUser`. El bloqueo original no se altera. | MOD03-PE-004 (Clase No VÃ¡lida) |

### 3.5. Escenario: [ESC-3005] - InteracciÃ³n CartogrÃ¡fica y VisualizaciÃ³n de Trazabilidad (Historial)

**A. DefiniciÃ³n del Escenario**

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el entorno de ediciÃ³n integrado (Editor iD) responde de manera dinÃ¡mica a la selecciÃ³n de elementos geogrÃ¡ficos en el mapa, mostrando sus atributos correspondientes. SimultÃ¡neamente, validar que el panel de control del Tasking Manager renderiza el historial de la tarea, permitiendo filtrar correctamente los eventos de trazabilidad (comentarios y transiciones de estado). |
| **RF Asociados** | RF-3002 (IntegraciÃ³n de Editor Web), RF-7001 (Comentarios por Tarea) |
| **Precondiciones** | Proyecto en estado `PUBLISHED`. Usuario `MAPPER` (ACT-0002) autenticado en el sistema. Tarea seleccionada en estado `LOCKED_FOR_MAPPING` con el editor web (iD) completamente cargado en la interfaz. |
| **TÃ©cnicas aplicadas**| ParticiÃ³n de Equivalencia (PE). |
| **Resultado Esperado** | El sistema debe mostrar los detalles y etiquetas del polÃ­gono/lÃ­nea seleccionada en el panel izquierdo (Editor iD). En el panel derecho (Tasking Manager), la pestaÃ±a "Historial" debe aplicar los filtros visuales correctamente, discriminando entre comentarios de usuarios y registros del sistema, sin recargar la pÃ¡gina. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**

Para este escenario se ha seleccionado la **ParticiÃ³n de Equivalencia (PE)**. Esta tÃ©cnica es la mÃ¡s adecuada funcionalmente porque nos permite dividir los tipos de datos de entrada observables en la interfaz en grupos lÃ³gicos que el sistema debe procesar de manera distinta:
1.  **Filtros de Trazabilidad:** El usuario tiene tres opciones excluyentes en la UI (radio buttons) que alteran la renderizaciÃ³n del DOM en el panel derecho.
2.  **InteracciÃ³n Espacial:** La interacciÃ³n del cursor sobre el mapa se divide en dos grandes "clases" funcionales: clics dentro de la zona permitida (polÃ­gono de la tarea) y clics fuera del lÃ­mite establecido.

**B.1. ParticiÃ³n de Equivalencia (Filtros del Historial)**
EvalÃºa la reactividad del componente visual que lista la cronologÃ­a de eventos de la tarea.

| Cod. | Variable Analizada en UI | Clases VÃ¡lidas (Filtros UI) |
| :--- | :--- | :--- |
| **MOD03-PE-005** | Filtro de vista "Historial" | 1. **Comentarios:** Oculta eventos del sistema, muestra solo mensajes de texto ingresados por usuarios.<br>2. **Actividades:** Oculta mensajes, muestra solo transiciones de estado automÃ¡ticas y manuales (por ejemplo, "bloqueada para mapeo", "dividiÃ³ una tarea").<br>3. **Todos:** Renderiza la uniÃ³n cronolÃ³gica de las dos clases anteriores. |

**B.2. ParticiÃ³n de Equivalencia (LÃ­mites y GeometrÃ­a en Editor Web)**
Se ajusta la particiÃ³n para evaluar la respuesta de la interfaz (renderizado de guÃ­as visuales) frente al Ã¡rea de trabajo, no como un bloqueo transaccional.

| Cod. | Variable Analizada en UI | Clase VÃ¡lida (Dentro del AOI) | Clase VÃ¡lida (Fuera del AOI) |
| :--- | :--- | :--- | :--- |
| **MOD03-PE-006** | Ãrea visual de interacciÃ³n cartogrÃ¡fica (BBOX) | NavegaciÃ³n e interacciÃ³n dentro del polÃ­gono delimitado (sin mÃ¡scara de sombreado). | NavegaciÃ³n e interacciÃ³n fuera del polÃ­gono delimitado para la tarea asignada. |

*   *Comportamiento esperado (Dentro del AOI):* El usuario interactÃºa con los elementos con visibilidad normal.
*   *Comportamiento esperado (Fuera del AOI):* La interfaz superpone un sombreado oscuro, el lÃ­mite magenta y el texto *"Task for project [ID]. Do not edit outside of this area!"*. **El sistema permite la inserciÃ³n del elemento cartogrÃ¡fico**, cumpliendo la premisa de "guiar visualmente, no bloquear".

---

**C. Casos de Prueba Derivados**

| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada / Contexto | Resultado Esperado | TÃ©cnicas / Etiquetas Aplicadas |
| :--- | :--- | :--- | :--- | :--- |
| **CP-3005-01** | 1. En el panel derecho de Tasking Manager, hacer clic en la pestaÃ±a "Historial".<br>2. Seleccionar el radio button "Actividades". | **Filtro UI:** `Actividades` | La interfaz renderiza Ãºnicamente el rastro de auditorÃ­a del sistema (por ejemplo, "[Usuario] bloqueada para mapeo hace 42 minutos", "desbloqueada automÃ¡ticamente..."). Los comentarios desaparecen de la vista. | PE-005 (Filtro Actividades) |
| **CP-3005-02** | 1. En el panel derecho, seleccionar el radio button "Comentarios". | **Filtro UI:** `Comentarios` | La lista se actualiza dinÃ¡micamente ocultando los registros del sistema. Solo se visualizan avatares y mensajes de texto dejados por los mappers/validators previos. | PE-005 (Filtro Comentarios) |
| **CP-3005-03** | 1. En el Ã¡rea del mapa central, hacer clic sobre un polÃ­gono existente (por ejemplo, zona residencial) situado dentro del cuadro delimitador de la tarea. | **Elemento:** Ãrea dentro del BBOX | El panel izquierdo (iD) reacciona mostrando los metadatos del elemento (Tipo de elemento, Nombre, Etiquetas como `type=multipolygon`). | PE-006 (Clase VÃ¡lida Espacial) |
| **CP-3005-04** | 1. Desplazar la vista (Pan) hacia el exterior del borde magenta de la tarea.<br>2. Seleccionar la herramienta "Punto" o "Ãrea".<br>3. Hacer clic para crear el elemento en la zona sombreada. | **Elemento:** GeometrÃ­a nueva fuera del BBOX. | La UI mantiene visible el sombreado y la advertencia textual permanente. **El elemento se crea exitosamente en el mapa**, confirmando que el sistema proporciona una guÃ­a visual restrictiva pero no un bloqueo a nivel de herramienta. | PE-006 (Clase VÃ¡lida Fuera del AOI) |
## 4. Matriz de Trazabilidad del MÃ³dulo

Esta matriz consolida la relaciÃ³n bidireccional entre los Requerimientos Funcionales (RF) documentados y los artefactos de diseÃ±o generados para el mÃ³dulo **MOD-03: EjecuciÃ³n de Mapeo (Tasking)**. 

Se han incorporado las actualizaciones derivadas de los rediseÃ±os funcionales, incluyendo la adaptaciÃ³n del Escenario 2 a un enfoque estrictamente basado en la interfaz (eliminando las pruebas a nivel de API) y la integraciÃ³n del nuevo Escenario 5, asegurando asÃ­ una cobertura total y coherente de las reglas de negocio.

| Requerimiento Funcional (RF) | EspecificaciÃ³n de Escenario (ESC) | Casos de Prueba (CP) Derivados | TÃ©cnicas de DiseÃ±o Aplicadas |
| :--- | :--- | :--- | :--- |
| **RF-3001**, RF-3002, RF-3003 | **ESC-3001:** Solicitud de Bloqueo e Inicio de Tarea de Mapeo | **CP-3001-01** | Tabla de DecisiÃ³n (A), PE (Clase VÃ¡lida Web) |
| **RF-3001**, RF-3002, RF-3003 | ESC-3001 | **CP-3001-02** | Tabla de DecisiÃ³n (A), PE (Clase VÃ¡lida Local) |
| **RF-3001**, RF-3002, RF-3003 | ESC-3001 | **CP-3001-03**, **CP-3001-04**, **CP-3001-05**, **CP-3001-06** | Tabla de DecisiÃ³n (B, C, D, E) |
| **RF-3001**, RF-3002, RF-3003 | ESC-3001 | **CP-3001-07** | Tabla de DecisiÃ³n (A), PE (Clase No VÃ¡lida) |
| **RF-3004** | **ESC-3002:** LiberaciÃ³n y EnvÃ­o de Tarea de Mapeo (Submit) | **CP-3002-01**, **CP-3002-02** | TransiciÃ³n de Estados (VÃ¡lida), PE (Clase VÃ¡lida) |
| **RF-3004** | ESC-3002 | **CP-3002-03**, **CP-3002-04**, **CP-3002-05** | PE (Clase No VÃ¡lida en UI) |
| **RF-3005** | **ESC-3003:** DivisiÃ³n de Tarea de Mapeo (Split Task) | **CP-3003-01** | AVL-001 (VÃ¡lido), PE-003 (VÃ¡lido) |
| **RF-3005** | ESC-3003 | **CP-3003-02** | AVL-001 (InvÃ¡lido), PE-003 (VÃ¡lido) |
| **RF-3005** | ESC-3003 | **CP-3003-03**, **CP-3003-04** | AVL-001 (VÃ¡lido), PE-003 (No VÃ¡lido) |
| **RF-3006** | **ESC-3004:** ExpiraciÃ³n y ExtensiÃ³n de Bloqueo de Tarea | **CP-3004-01** | AVL-002 (VÃ¡lido) |
| **RF-3006** | ESC-3004 | **CP-3004-02** | AVL-002 (InvÃ¡lido) |
| **RF-3006** | ESC-3004 | **CP-3004-03** | PE-004 (Clase VÃ¡lida) |
| **RF-3006** | ESC-3004 | **CP-3004-04**, **CP-3004-05** | PE-004 (Clase No VÃ¡lida) |
| **RF-3002**, **RF-7001** | **ESC-3005:** InteracciÃ³n CartogrÃ¡fica y VisualizaciÃ³n de Trazabilidad | **CP-3005-01**, **CP-3005-02** | PE-005 (Filtros UI) |
| **RF-3002**, **RF-7001** | ESC-3005 | **CP-3005-03** | PE-006 (Clase VÃ¡lida Dentro del AOI) |
| **RF-3002**, **RF-7001** | ESC-3005 | **CP-3005-04** | PE-006 (Clase VÃ¡lida Fuera del AOI) |


