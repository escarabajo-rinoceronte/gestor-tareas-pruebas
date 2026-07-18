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
  <b>Proyecto:</b> HOT Tasking Manager — DiseÃ±o de Pruebas Funcionales: MOD-04 - Proceso de ValidaciÃ³n <br>
  <b>Fecha de Elaboración:</b> 12/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# DiseÃ±o de Pruebas Funcionales: MOD-04 - Proceso de ValidaciÃ³n

**VersiÃ³n del Documento:** 1.0
**Tipo de AnÃ¡lisis:** DiseÃ±o de Pruebas de Sistema (Caja Negra)

---

## 1. Contexto del MÃ³dulo

Este mÃ³dulo gestiona el flujo de control de calidad o validaciÃ³n de las tareas. Su objetivo principal es asegurar que los mapeos realizados cumplan con los estÃ¡ndares, bloqueando tareas para revisiÃ³n (una o mÃºltiples), impidiendo la auto-validaciÃ³n y permitiendo evaluaciones (aprobar o rechazar), ademÃ¡s de deshacer acciones previas.

_Para consultar el detalle exhaustivo de los actores, restricciones y reglas de negocio, referirse al [CatÃ¡logo de Requerimientos Funcionales](/tests-docs/02-diseno-de-pruebas/funcionales/00-requerimientos-funcionales.md)._

---

## 2. Estrategia de DiseÃ±o de Pruebas

### 2.1. Enfoque general

Las pruebas se centrarÃ¡n en corroborar los controles de acceso (usuario apto para la funciÃ³n de Validator frente a otros), la correcta transiciÃ³n de estados de las tareas tras cada acciÃ³n y las validaciones lÃ³gicas del sistema, especialmente las polÃ­ticas preventivas (auto-validaciÃ³n) contempladas por las reglas de plataforma.

### 2.2. TÃ©cnicas de Caja Negra Utilizadas

- **ParticiÃ³n de Equivalencia:** Utilizada para agrupar las condiciones del usuario que intenta validar (idÃ©ntico al que mapeÃ³ frente a usuario distinto) y el nivel del autor que efectÃºa la acciÃ³n, dividiÃ©ndolo de acuerdo con los niveles vÃ¡lidos (`VALIDATOR` por experiencia) e invÃ¡lidos (`MAPPER` sin nivel suficiente, AnÃ³nimo).
- **TransiciÃ³n de Estados:** Se aplica a los ciclos de vida de una tarea para confirmar que los estados cambien correctamente (`MAPPED` -> `LOCKED_FOR_VALIDATION` -> `VALIDATED`/`INVALIDATED`).
- **Casos de Uso / Pruebas Basadas en Escenarios:** Permite la derivaciÃ³n de casos asegurando que cada etapa lÃ³gica y limitaciÃ³n de las reglas (ej. deshacer o validar calidad) se prueben como la interacciÃ³n completa de un actor contra el TM.

---

## 3. Especificaciones de Escenarios y Casos de Prueba

### 3.1. Escenario: ESC-4001 - Bloqueo y PrevenciÃ³n de Auto-validaciÃ³n

**A. DefiniciÃ³n del Escenario**
| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que un usuario asumiendo la funciÃ³n de Validator pueda iniciar el bloqueo de una tarea para revisiÃ³n, pero que el sistema le impida validar una tarea donde Ã©l mismo haya proporcionado previamente el mapeo. |
| **RF Asociados** | RF-4001, RF-4002 |
| **Precondiciones** | Usuario con nivel de experiencia para asumir la funciÃ³n de Validator (o Admin). Tareas disponibles en estado `MAPPED`. El usuario tiene al menos una tarea que mapeÃ³ previamente e intenta validar, y otra que fue mapeada por un tercero. |
| **TÃ©cnicas aplicadas**| ParticiÃ³n de Equivalencia, TransiciÃ³n de Estados |
| **Resultado Esperado** | El sistema debe conceder el bloqueo (`LOCKED_FOR_VALIDATION`) a tareas ajenas y emitir una denegaciÃ³n u ocultar la opciÃ³n para la auto-validaciÃ³n, respetando la separaciÃ³n de labores. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**

- **ParticiÃ³n de Equivalencia (AutorÃ­a de Mapeo):**
  - _Clase VÃ¡lida:_ El usuario en funciÃ³n de Validator NO es el autor del Ãºltimo estado MAPPED.
  - _Clase InvÃ¡lida:_ El usuario en funciÃ³n de Validator ES el autor del Ãºltimo estado MAPPED.
- **TransiciÃ³n de Estados (Pre-bloqueo):**
  - _TransiciÃ³n vÃ¡lida:_ De `MAPPED` a `LOCKED_FOR_VALIDATION`.

**C. Casos de Prueba Derivados**
| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada (Clases aplicadas) | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CP-4001-01** | 1. Iniciar sesiÃ³n con un usuario apto para la funciÃ³n de Validator. <br>2. Seleccionar una tarea en estado `MAPPED` de otro usuario.<br>3. Solicitar validaciÃ³n. | **AutorÃ­a:** Tercero<br>**Cant:** Singular | El sistema asigna la tarea al usuario, cambiando su estado a `LOCKED_FOR_VALIDATION` y habilitando el panel de evaluaciÃ³n. |
| **CP-4001-02** | 1. Iniciar sesiÃ³n con un usuario apto para la funciÃ³n de Validator. <br>2. Seleccionar una tarea en estado `MAPPED` registrada por sÃ­ mismo.<br>3. Intentar validarla. | **AutorÃ­a:** Propia<br>**Cant:** Singular | El sistema impide el acceso de validaciÃ³n sobre la tarea y alerta sobre la restricciÃ³n de validarse a sÃ­ mismo. |
| **CP-4001-03** | 1. Iniciar sesiÃ³n como `Mapper` (Nivel de experiencia sin permisos de validaciÃ³n). <br>2. Seleccionar una tarea en estado `MAPPED` de otro usuario.<br>3. Intentar bloquearla para revisiÃ³n. | **Rol:** Mapper | El sistema oculta la opciÃ³n de validaciÃ³n o deniega el acceso con un mensaje de permisos insuficientes. |
| **CP-4001-04** | 1. Iniciar sesiÃ³n con un usuario apto para la funciÃ³n de Validator. <br>2. Seleccionar mÃºltiples tareas (>1) en estado `MAPPED` de otros usuarios.<br>3. Solicitar validaciÃ³n en lote. | **AutorÃ­a:** Tercero<br>**Cant:** MÃºltiple | El sistema asigna todas las tareas seleccionadas al usuario, pasando el conjunto a estado `LOCKED_FOR_VALIDATION`. |
| **CP-4001-05** | 1. Iniciar sesiÃ³n con un usuario apto para la funciÃ³n de Validator. <br>2. Seleccionar mÃºltiples tareas en lote (incluyendo una mapeada por sÃ­ mismo y otras de terceros).<br>3. Solicitar validaciÃ³n de la selecciÃ³n. | **AutorÃ­a:** Mixta<br>**Cant:** MÃºltiple | El sistema bloquea las tareas de terceros y rechaza aisladamente/advierte sobre la tarea propia impidiendo que transicione. |
| **CP-4001-06** | 1. Iniciar sesiÃ³n con un usuario apto para la funciÃ³n de Validator. <br>2. Seleccionar tarea en estado `READY` o `LOCKED_FOR_MAPPING`.<br>3. Intentar acceder a su validaciÃ³n. | **Estado Tarea:** Ready | La interfaz de usuario deshabilita el botÃ³n de validaciÃ³n, imposibilitando la acciÃ³n sobre estados no listos. |
| **CP-4001-07** | 1. Iniciar sesiÃ³n con un usuario apto para la funciÃ³n de Validator.<br>2. Seleccionar una tarea que se encuentre bloqueada por otro validador (con el icono de candado).<br>3. Intentar iniciar la validaciÃ³n de esa celda especÃ­fica. | **AutorÃ­a:** Tercero<br>**Estado Tarea:** Locked por tercero | La interfaz de usuario no muestra controles de validaciÃ³n individuales para esa tarea y el mapa refleja el icono de bloqueo, forzando al usuario mediante el botÃ³n principal a "Validar otra tarea". |
| **CP-4001-08** | 1. Iniciar sesiÃ³n con un usuario apto para la funciÃ³n de Validator.<br>2. Seleccionar una tarea en estado `VALIDATED` (Terminada).<br>3. Intentar iniciar un bloqueo de validaciÃ³n sobre ella. | **AutorÃ­a:** Tercero<br>**Estado Tarea:** Validated | La interfaz de usuario no muestra controles individuales de asignaciÃ³n ni bloqueo para esa tarea por haber cerrado su ciclo de calidad, habilitando Ãºnicamente el botÃ³n principal "Validar otra tarea". |
| **CP-4001-09** | 1. Iniciar sesiÃ³n con un usuario apto para la funciÃ³n de Validator.<br>2. Sellecionar una tarea en estado `INVALIDATED` (Rechazada previamente).<br>3. Intentar iniciar un nuevo bloqueo de validaciÃ³n sobre ella antes de que sea re-mapeada. | **AutorÃ­a:** Tercero<br>**Estado Tarea:** Invalidated | El sistema restringe las opciones de validaciÃ³n, ocultando dichos controles y mostrando en su lugar el botÃ³n principal "Mapear tarea seleccionada" para forzar el flujo de correcciÃ³n previo. |
| **CP-4001-10** | 1. Iniciar sesiÃ³n con un usuario apto para la funciÃ³n de Validator que posea ademÃ¡s privilegios de Administrador global.<br>2. Seleccionar una tarea en estado `MAPPED` registrada por sÃ­ mismo.<br>3. Solicitar el bloqueo para validaciÃ³n. | **AutorÃ­a:** Propia<br>**Rol:** Validator + Admin | El sistema permite al usuario con perfil de Administrador omitir la regla de auto-validaciÃ³n general, asignÃ¡ndole la tarea y transicionÃ¡ndola con Ã©xito a estado `LOCKED_FOR_VALIDATION`. |

---

### 3.2. Escenario: ESC-4002 - EvaluaciÃ³n de Calidad de Tareas Mapeadas

**A. DefiniciÃ³n del Escenario**
| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que un usuario apto para evaluar pueda calificar satisfactoriamente, o rechazar, una tarea bloqueada; aplicando la designaciÃ³n final y retornando a la cola si fuera necesario. |
| **RF Asociados** | RF-4003 |
| **Precondiciones** | Usuario apto para la funciÃ³n de Validator autenticado. Tarea en estado `LOCKED_FOR_VALIDATION`. |
| **TÃ©cnicas aplicadas**| ParticiÃ³n de Equivalencia, TransiciÃ³n de Estados |
| **Resultado Esperado** | El sistema categoriza la tarea finalmente como `VALIDATED` (aprobado total) o `INVALIDATED` (para volver a mapear) y libera la tarea de su estatus bloqueado. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**

- **ParticiÃ³n de Equivalencia (DecisiÃ³n de Calidad):**
  - _Clase VÃ¡lida 1:_ Aprobar (Todo correcto).
  - _Clase VÃ¡lida 2:_ Rechazar / Invalidar (Errores presentes).
- **TransiciÃ³n de Estados:**
  - _TransiciÃ³n 1:_ De `LOCKED_FOR_VALIDATION` a `VALIDATED`.
  - _TransiciÃ³n 2:_ De `LOCKED_FOR_VALIDATION` a `INVALIDATED`.

**C. Casos de Prueba Derivados**
| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada (Clases aplicadas) | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CP-4002-01** | 1. Dentro del panel de evaluaciÃ³n, marcar la tarea como correctamente mapeada.<br>2. Enviar estado. | **DecisiÃ³n:** Aprobar | La tarea queda registrada en estado `VALIDATED`, finalizando su flujo bÃ¡sico de calidad. |
| **CP-4002-02** | 1. Dentro del panel, marcar la tarea como incorrecta, aÃ±adir comentario tÃ©cnico.<br>2. Enviar estado. | **DecisiÃ³n:** Rechazar | La tarea cambia a estado `INVALIDATED` y es de vuelta a disposiciÃ³n de los mappers, anotando la retroalimentaciÃ³n. |
| **CP-4002-03** | 1. Dentro del panel, marcar la tarea como incorrecta (Invalidar), dejando el comentario vacÃ­o.<br>2. Enviar estado. | **DecisiÃ³n:** Rechazar<br>**Comentario:** Nulo | El sistema previene el envÃ­o, requiriendo (habilitando alert/estado de error) que se adjunte un comentario explicativo. |
| **CP-4002-04** | 1. Con un lote de tareas bloqueadas simultÃ¡neamente, seleccionar Aprobar en unas e Invalidar en otras. <br>2. Enviar evaluaciones. | **DecisiÃ³n:** Mixta | El sistema actualiza cada tarea a su estado asignado individualmente (`VALIDATED` / `INVALIDATED`), liberando los bloqueos correspondientes. |
| **CP-4002-05** | 1. Mantener bloqueada una tarea para validaciÃ³n por tiempo excesivo (Timeout).<br>2. Intentar evaluarla despuÃ©s de este lÃ­mite de autoliberaciÃ³n. | **Estado:** Expirado | El sistema informa mediante de un error de timeout ("Ya no tienes esta tarea asignada") y la tarea se devuelve a su estado anterior. |
| **CP-4002-06** | 1. Iniciar sesiÃ³n con un usuario con funciÃ³n de Validator.<br>2. Seleccionar simultÃ¡neamente un lote de mÃºltiples tareas en estado `MAPPED` (Lista para validar).<br>3. Ejecutar la acciÃ³n de aprobaciÃ³n conjunta para las tareas seleccionadas. | **DecisiÃ³n:** Aprobar<br>**Cant:** MÃºltiple | El sistema procesa la transacciÃ³n masiva de forma directa, transicionando todas las celdas del lote seleccionado al estado `VALIDATED` simultÃ¡neamente y liberando sus bloqueos. |
| **CP-4002-07** | 1. Iniciar sesiÃ³n con un usuario con funciÃ³n de Validator.<br>2. Seleccionar simultÃ¡neamente un lote de mÃºltiples tareas en estado `MAPPED` (Lista para validar).<br>3. Ejecutar la acciÃ³n de invalidaciÃ³n o rechazo conjunto para las tareas seleccionadas. | **DecisiÃ³n:** Rechazar<br>**Cant:** MÃºltiple | El sistema procesa la transacciÃ³n masiva, transicionando todas las celdas del lote seleccionado al estado `INVALIDATED` simultÃ¡neamente y liberando sus bloqueos para que requieran nuevo mapeo. |
| **CP-4002-08** | 1. Dentro del panel de una tarea bloqueada, seleccionar la opciÃ³n para rechazar el mapeo (`INVALIDATED`).<br>2. En el cuadro de comentarios opcional, ingresar una cadena de texto tÃ©cnica que contenga caracteres especiales, sÃ­mbolos de mapeo o formato enriquecido.<br>3. Confirmar el envÃ­o de la evaluaciÃ³n. | **DecisiÃ³n:** Rechazar<br>**Comentario:** Caracteres especiales | El sistema procesa la invalidaciÃ³n cambiando el estado a `INVALIDATED` y guarda el texto en el historial de forma correcta sin corromper la codificaciÃ³n de los sÃ­mbolos. |
| **CP-4002-09** | 1. Dentro del panel de una tarea bloqueada, seleccionar la opciÃ³n para rechazar el mapeo (`INVALIDATED`).<br>2. En el cuadro de comentarios, introducir una retroalimentaciÃ³n detallada y extensa estructurada por secciones para describir las observaciones.<br>3. Confirmar el envÃ­o de la evaluaciÃ³n. | **DecisiÃ³n:** Rechazar<br>**Comentario:** Extenso estructurado | El sistema asimila el texto completo sin restricciones ni cortes de longitud, registra la tarea como `INVALIDATED` y guarda la retroalimentaciÃ³n Ã­ntegra en la lÃ­nea de tiempo de actividades. |
| **CP-4002-10** | 1. Dentro del panel de una tarea bloqueada, seleccionar la opciÃ³n para evaluar el mapeo (`VALIDATED` o `INVALIDATED`).<br>2. En el cuadro de comentarios, redactar una descripciÃ³n tÃ©cnica e insertar o adjuntar una imagen que evidencie el estado del elemento geogrÃ¡fico.<br>3. Confirmar el envÃ­o de la evaluaciÃ³n. | **DecisiÃ³n:** Evaluar con multimedia<br>**Comentario:** Texto e imagen | El sistema procesa el cambio de estado con Ã©xito, guarda el comentario y almacena la imagen adjunta de forma correcta, permitiendo su visualizaciÃ³n posterior en la lÃ­nea de tiempo de la tarea. |

---

### 3.3. Escenario: ESC-4003 - Revertir acciones previas (Undo)

**A. DefiniciÃ³n del Escenario**
| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Asegurar que el usuario pueda usar la funciÃ³n "deshacer" para revocar su Ãºltima operaciÃ³n sobre una tarea de revisiÃ³n, recuperando el estado funcional idÃ©ntico antes de tal acciÃ³n. |
| **RF Asociados** | RF-4004 |
| **Precondiciones** | Usuario (Mapper o con funciÃ³n de Validator) que acaba de ejecutar una transiciÃ³n en una tarea. La tarea todavÃ­a tiene a este usuario en el historial inmediato. |
| **TÃ©cnicas aplicadas**| TransiciÃ³n de Estados |
| **Resultado Esperado** | El estado de la tarea retorna exactamente al valor reportado anterior al dictamen, con constancia textual o sistÃ©mica de reversiÃ³n. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**

- **TransiciÃ³n de Estados (Vuelta atrÃ¡s):** ReversiÃ³n hacia los dictados anteriores (Ej. de `VALIDATED` a `LOCKED_FOR_VALIDATION` / `MAPPED` o simplemente deshacer mapping enviado).

**C. Casos de Prueba Derivados**
| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada (Clases aplicadas) | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CP-4003-01** | 1. Desde el historial de ejecuciÃ³n propio o del proyecto, buscar la tarea recientemente modificada.<br>2. Accionar el botÃ³n de Deshacer (Undo) Ãºltimo estado. | **DecisiÃ³n:** Ejecutar Undo (Desde Validated) | El sistema revierte la categorizaciÃ³n retornando la tarea al estado anterior, anotÃ¡ndolo en sus registros (timeline). |
| **CP-4003-02** | 1. Iniciar sesiÃ³n con un usuario apto para la funciÃ³n de Validator.<br>2. Seleccionar una tarea recientemente evaluada como `INVALIDATED` (Necesita mÃ¡s mapeo).<br>3. Abrir el historial o cuadro de actividades de la tarea.<br>4. Intentar accionar una opciÃ³n de reversiÃ³n (Undo) para deshacer la invalidaciÃ³n. | **DecisiÃ³n:** Intentar Undo (Desde Invalidated) | El sistema no ofrece controles o botones para deshacer la acciÃ³n (Undo) sobre elementos en estado invalidado, manteniendo la tarea de forma definitiva en el flujo de correcciÃ³n. |
| **CP-4003-03** | 1. Visualizar una tarea `VALIDATED` cuya evaluaciÃ³n final fue efectuada por OTRO usuario.<br>2. Intentar Deshacer (Undo) su acciÃ³n mediante el botÃ³n "Solicitar revalidaciÃ³n". | **Propiedad:** Tercero | El sistema permite la acciÃ³n; al contar con el rol de Validator, el botÃ³n "Solicitar revalidaciÃ³n" debe estar visible y habilitado, permitiendo revertir tareas validadas por otros usuarios. |
| **CP-4003-04** | 1. Tras presionar Undo una vez con Ã©xito, presionar Undo una segunda vez consecutiva sobre la misma tarea. | **DecisiÃ³n:** Undo recursivo | El sistema devuelve error o deshabilita la opciÃ³n notificando que no existe otra acciÃ³n reciente atribuible en el historial para ser deshecha. |
| **CP-4003-05** | 1. Iniciar sesiÃ³n con un usuario estÃ¡ndar que no posea la funciÃ³n de Validator asignada.<br>2. Seleccionar una tarea terminada (`VALIDATED`) del listado y abrir su historial.<br>3. Accionar la opciÃ³n de reversiÃ³n de estado (Undo).<br>4. Confirmar la acciÃ³n en el cuadro de diÃ¡logo emergente del sistema. | **Rol:** Mapper estÃ¡ndar<br>**AcciÃ³n:** Confirmar Undo en modal | El sistema muestra la advertencia de confirmaciÃ³n, pero al aceptar la acciÃ³n, restringe el proceso ignorando el cambio; el estado de la tarea permanece intacto y no se habilita ningÃºn panel adicional. |


---

## 4. Matriz de Trazabilidad del MÃ³dulo

| Requerimiento Funcional (RF) | EspecificaciÃ³n de Escenario (ESC) | Casos de Prueba (CP) derivados | TÃ©cnicas de DiseÃ±o Aplicadas |
| :--- | :--- | :--- | :--- |
| **RF-4001** | ESC-4001 | CP-4001-01, CP-4001-03, CP-4001-04, CP-4001-06, CP-4001-07, CP-4001-08, CP-4001-09 | ParticiÃ³n de Equivalencia, Trans. Estados |
| **RF-4002** | ESC-4001 | CP-4001-02, CP-4001-05, CP-4001-10 | ParticiÃ³n de Equivalencia |
| **RF-4003** | ESC-4002 | CP-4002-01, CP-4002-02, CP-4002-03, CP-4002-04, CP-4002-05, CP-4002-06, CP-4002-07, CP-4002-08, CP-4002-09, CP-4002-10 | ParticiÃ³n de Equivalencia, TransiciÃ³n Estados|
| **RF-4004** | ESC-4003 | CP-4003-01, CP-4003-02, CP-4003-03, CP-4003-04, CP-4003-05| TransiciÃ³n de Estados |


