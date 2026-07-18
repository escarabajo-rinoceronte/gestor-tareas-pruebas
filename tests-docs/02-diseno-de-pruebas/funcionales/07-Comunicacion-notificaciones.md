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
  <b>Proyecto:</b> HOT Tasking Manager — DiseÃ±o de Pruebas Funcionales: MOD-0007 - ComunicaciÃ³n y Notificaciones <br>
  <b>Fecha de Elaboración:</b> 12/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# DiseÃ±o de Pruebas Funcionales: MOD-0007 - ComunicaciÃ³n y Notificaciones

**VersiÃ³n del Documento:** 1.0  
**Tipo de AnÃ¡lisis:** DiseÃ±o de Pruebas de Sistema (Caja Negra)  
**MÃ³dulo evaluado:** MOD-0007 - ComunicaciÃ³n y Notificaciones  

---

## 1. Contexto del MÃ³dulo

El mÃ³dulo **MOD-0007: ComunicaciÃ³n y Notificaciones** agrupa las funcionalidades relacionadas con la interacciÃ³n comunicativa dentro del sistema HOTOSM Tasking Manager. Este mÃ³dulo permite registrar comentarios asociados a tareas, utilizar menciones a usuarios y generar alertas internas o por correo electrÃ³nico ante eventos relevantes.

Desde el punto de vista funcional, este mÃ³dulo es importante porque permite mantener trazabilidad de las observaciones realizadas durante el trabajo de mapeo y validaciÃ³n. AdemÃ¡s, facilita que los usuarios sean informados cuando ocurre un evento que requiere su atenciÃ³n, como una menciÃ³n, una tarea invalidada o una notificaciÃ³n generada por el sistema.

Los principales actores involucrados son:   

| Actor | Rol dentro del mÃ³dulo |
| :--- | :--- |
| **ACT-0002 - Mapper** | Usuario que puede registrar comentarios durante el flujo de mapeo. |
| **ACT-0003 - Validator** | Usuario que puede registrar observaciones durante el proceso de validaciÃ³n. |
| **ACT-0006 - Sistema** | Encargado de generar notificaciones internas o por correo ante eventos relevantes. |

*Para consultar el detalle de actores, mÃ³dulos y requerimientos funcionales, referirse al documento `01-requerimientos-funcionales.md`.*

---

## 2. Estrategia de DiseÃ±o de Pruebas

### 2.1. Enfoque general

El enfoque de pruebas aplicado al mÃ³dulo serÃ¡ de **caja negra**, evaluando el comportamiento observable del sistema desde la interfaz web y desde las respuestas visibles para el usuario, sin analizar la implementaciÃ³n interna del cÃ³digo.

Las pruebas se diseÃ±an a partir de los requerimientos funcionales asociados al mÃ³dulo **MOD-0007**, principalmente:

- **RF-7001:** Comentarios por tarea.
- **RF-7002:** Notificaciones in-app.
- **RF-7003:** EnvÃ­o de emails.

El objetivo del diseÃ±o es validar que el sistema permita registrar comentarios vÃ¡lidos, controle entradas no vÃ¡lidas, procese menciones a usuarios, genere notificaciones internas cuando corresponda y respete las condiciones necesarias para el envÃ­o de notificaciones por correo electrÃ³nico.

---

### 2.2. TÃ©cnicas de Caja Negra Utilizadas

Para este mÃ³dulo se aplicarÃ¡n las siguientes tÃ©cnicas de diseÃ±o de pruebas funcionales:

#### ParticiÃ³n de Equivalencia

Se utiliza para clasificar las entradas relacionadas con comentarios y destinatarios de notificaciÃ³n en grupos vÃ¡lidos e invÃ¡lidos.

Aplicaciones dentro del mÃ³dulo:

- Comentario vÃ¡lido.
- Comentario vacÃ­o.
- Comentario con formato Markdown.
- Comentario con menciÃ³n vÃ¡lida.
- Comentario con menciÃ³n inexistente o mal formada.

#### Tabla de DecisiÃ³n

Se utiliza cuando el resultado depende de la combinaciÃ³n de varias condiciones, especialmente en la generaciÃ³n de notificaciones.

Aplicaciones dentro del mÃ³dulo:

- Usuario mencionado o no mencionado.
- Notificaciones activadas o desactivadas.
- Evento notificable o no notificable.
- Usuario destinatario vÃ¡lido o no vÃ¡lido.
- Preferencia de correo habilitada o deshabilitada.

#### Flujo funcional

Se utiliza para validar secuencias completas visibles para el usuario, como registrar un comentario y verificar su apariciÃ³n en el historial de una tarea.

Aplicaciones dentro del mÃ³dulo:

- Crear comentario.
- Guardar comentario.
- Visualizar comentario en el historial.
- Generar notificaciÃ³n asociada.

---

## 3. Especificaciones de Escenarios de Prueba

Para organizar el diseÃ±o del mÃ³dulo **MOD-0007**, los casos funcionales se agrupan en cuatro escenarios principales.

| ID Escenario | DescripciÃ³n breve | RF cubiertos | Alcance funcional | TÃ©cnica principal |
| :--- | :--- | :--- | :--- | :--- |
| **ESC-7001** | Registro de comentarios en tareas | RF-7001 | Valida que el usuario pueda registrar comentarios asociados a una tarea y que el sistema controle entradas vÃ¡lidas e invÃ¡lidas. | ParticiÃ³n de Equivalencia |
| **ESC-7002** | Comentarios con formato y menciones | RF-7001, RF-7002 | Valida comentarios con Markdown bÃ¡sico y menciones a usuarios mediante `@usuario`. | ParticiÃ³n de Equivalencia / Tabla de DecisiÃ³n |
| **ESC-7003** | Notificaciones internas | RF-7002 | Verifica la generaciÃ³n de notificaciones in-app ante eventos relevantes. | Tabla de DecisiÃ³n |
| **ESC-7004** | Preferencias y envÃ­o de emails | RF-7003 | Valida las condiciones necesarias para que el sistema envÃ­e o no notificaciones por correo. | Tabla de DecisiÃ³n |

---

## 4. Escenarios Detallados y Casos Derivados

---

## 4.1. Escenario: [ESC-7001] - Registro de comentarios en tareas

### A. DefiniciÃ³n del Escenario

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el sistema permita registrar comentarios asociados al historial de una tarea y que controle entradas no vÃ¡lidas. |
| **RF asociados** | RF-7001 |
| **Actor principal** | ACT-0002 - Mapper / ACT-0003 - Validator |
| **Precondiciones** | El usuario se encuentra autenticado y accede a una tarea disponible dentro de un proyecto. |
| **TÃ©cnicas aplicadas** | ParticiÃ³n de Equivalencia y flujo funcional. |
| **Resultado esperado** | El sistema registra comentarios vÃ¡lidos en el historial de la tarea y evita guardar comentarios vacÃ­os o invÃ¡lidos. |

### B. AplicaciÃ³n de TÃ©cnicas

#### B.1. ParticiÃ³n de Equivalencia para comentarios

| Clase invÃ¡lida | Clase vÃ¡lida | Clase vÃ¡lida |
| :--- | :--- | :--- |
| Comentario vacÃ­o o compuesto solo por espacios. | Comentario de texto plano vÃ¡lido. | Comentario con contenido descriptivo relacionado con la tarea. |
| **Comportamiento esperado:** el sistema no debe registrar el comentario o debe mostrar validaciÃ³n. | **Comportamiento esperado:** el sistema debe registrar el comentario. | **Comportamiento esperado:** el sistema debe registrar el comentario en el historial. |

#### B.2. Flujo funcional de registro de comentario

El flujo esperado es:

1. Ingresar a una tarea.
2. Abrir la secciÃ³n de comentarios o historial.
3. Escribir un comentario vÃ¡lido.
4. Enviar o guardar el comentario.
5. Verificar que el comentario aparezca en la interfaz.

### C. Casos de Prueba Derivados

| ID Caso | Pasos de ejecuciÃ³n resumidos | Datos de entrada / contexto | Resultado esperado |
| :--- | :--- | :--- | :--- |
| **CP-MOD7-001** | Registrar un comentario vÃ¡lido en una tarea. | Comentario de texto plano relacionado con la tarea. | El sistema guarda el comentario y lo muestra en el historial. |
| **CP-MOD7-002** | Intentar registrar un comentario vacÃ­o. | Campo de comentario vacÃ­o o con espacios. | El sistema no registra el comentario o muestra una validaciÃ³n. |

---

## 4.2. Escenario: [ESC-7002] - Comentarios con formato y menciones

### A. DefiniciÃ³n del Escenario

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el sistema procese comentarios con formato bÃ¡sico y menciones a usuarios mediante el uso de `@usuario`. |
| **RF asociados** | RF-7001, RF-7002 |
| **Actor principal** | ACT-0002 - Mapper / ACT-0003 - Validator |
| **Precondiciones** | Existe una tarea disponible y al menos un usuario que pueda ser mencionado. |
| **TÃ©cnicas aplicadas** | ParticiÃ³n de Equivalencia y Tabla de DecisiÃ³n. |
| **Resultado esperado** | El sistema registra comentarios con formato permitido y genera notificaciones cuando existe una menciÃ³n vÃ¡lida. |

### B. AplicaciÃ³n de TÃ©cnicas

#### B.1. ParticiÃ³n de Equivalencia para contenido del comentario

| Clase invÃ¡lida | Clase vÃ¡lida | Clase vÃ¡lida |
| :--- | :--- | :--- |
| MenciÃ³n mal formada o usuario inexistente. | Comentario con Markdown bÃ¡sico. | Comentario con menciÃ³n vÃ¡lida a un usuario existente. |
| **Comportamiento esperado:** el sistema no debe generar notificaciÃ³n vÃ¡lida o debe mostrar la menciÃ³n como texto normal. | **Comportamiento esperado:** el sistema debe guardar el contenido sin romper la interfaz. | **Comportamiento esperado:** el sistema debe registrar el comentario y generar notificaciÃ³n al usuario mencionado. |

#### B.2. Tabla de DecisiÃ³n para menciones

| Condiciones / Acciones | Regla 1 | Regla 2 | Regla 3 | Regla 4 |
| :--- | :---: | :---: | :---: | :---: |
| **Condiciones** | | | | |
| Â¿El comentario contiene menciÃ³n? | SÃ­ | SÃ­ | No | SÃ­ |
| Â¿El usuario mencionado existe? | SÃ­ | No | N/A | SÃ­ |
| Â¿El usuario mencionado tiene notificaciones activas? | SÃ­ | N/A | N/A | No |
| **Acciones** | | | | |
| Registrar comentario | X | X | X | X |
| Generar notificaciÃ³n in-app | X | | | |
| No generar notificaciÃ³n por usuario inexistente | | X | | |
| No generar notificaciÃ³n por preferencias desactivadas | | | | X |

En esta tabla, `N/A` significa que la condiciÃ³n no aplica para esa regla. La marca `X` indica la acciÃ³n esperada para cada combinaciÃ³n de condiciones.

### C. Casos de Prueba Derivados

| ID Caso | Pasos de ejecuciÃ³n resumidos | Datos de entrada / contexto | Resultado esperado |
| :--- | :--- | :--- | :--- |
| **CP-MOD7-003** | Registrar un comentario con formato Markdown bÃ¡sico. | Comentario con negrita, lista o enlace permitido. | El sistema guarda el comentario sin romper la visualizaciÃ³n. |
| **CP-MOD7-004** | Registrar un comentario mencionando a un usuario existente. | Comentario con `@usuario`. | El sistema registra el comentario y genera notificaciÃ³n para el usuario mencionado. |
| **CP-MOD7-005** | Registrar un comentario con menciÃ³n inexistente. | Comentario con `@usuario_inexistente`. | El sistema registra el comentario sin generar notificaciÃ³n vÃ¡lida. |

---

## 4.3. Escenario: [ESC-7003] - Notificaciones internas in-app

### A. DefiniciÃ³n del Escenario

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el sistema genere notificaciones internas visibles para el usuario cuando ocurre un evento relevante. |
| **RF asociados** | RF-7002 |
| **Actor principal** | ACT-0006 - Sistema |
| **Precondiciones** | Existe un usuario autenticado que puede recibir notificaciones internas. |
| **TÃ©cnicas aplicadas** | Tabla de DecisiÃ³n. |
| **Resultado esperado** | El sistema muestra una notificaciÃ³n interna cuando ocurre un evento notificable. |

### B. AplicaciÃ³n de TÃ©cnicas

#### B.1. Tabla de DecisiÃ³n para notificaciones in-app

| Condiciones / Acciones | Regla 1 | Regla 2 | Regla 3 | Regla 4 |
| :--- | :---: | :---: | :---: | :---: |
| **Condiciones** | | | | |
| Â¿Existe evento notificable? | SÃ­ | SÃ­ | No | SÃ­ |
| Â¿Existe destinatario vÃ¡lido? | SÃ­ | No | N/A | SÃ­ |
| Â¿Notificaciones in-app activas? | SÃ­ | N/A | N/A | No |
| **Acciones** | | | | |
| Mostrar notificaciÃ³n in-app | X | | | |
| No mostrar notificaciÃ³n por destinatario invÃ¡lido | | X | | |
| No mostrar notificaciÃ³n porque no existe evento | | | X | |
| No mostrar notificaciÃ³n por preferencia desactivada | | | | X |

### C. Casos de Prueba Derivados

| ID Caso | Pasos de ejecuciÃ³n resumidos | Datos de entrada / contexto | Resultado esperado |
| :--- | :--- | :--- | :--- |
| **CP-MOD7-006** | Generar un evento de menciÃ³n hacia un usuario vÃ¡lido. | Usuario mencionado con notificaciones activas. | El sistema muestra una notificaciÃ³n interna. |
| **CP-MOD7-007** | Revisar la bandeja o Ã¡rea de notificaciones despuÃ©s de un evento. | Evento notificable ejecutado previamente. | La notificaciÃ³n aparece en la interfaz del usuario destinatario. |

---

## 4.4. Escenario: [ESC-7004] - Preferencias y envÃ­o de emails

### A. DefiniciÃ³n del Escenario

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el sistema respete las condiciones necesarias para el envÃ­o de notificaciones por correo electrÃ³nico. |
| **RF asociados** | RF-7003 |
| **Actor principal** | ACT-0006 - Sistema |
| **Precondiciones** | El usuario posee correo registrado y el entorno cuenta con configuraciÃ³n SMTP disponible. |
| **TÃ©cnicas aplicadas** | Tabla de DecisiÃ³n y ParticiÃ³n de Equivalencia. |
| **Resultado esperado** | El sistema envÃ­a correos solo cuando el usuario tiene correo habilitado, existe un evento notificable y el entorno permite el envÃ­o SMTP. |

### B. AplicaciÃ³n de TÃ©cnicas

#### B.1. Tabla de DecisiÃ³n para envÃ­o de emails

| Condiciones / Acciones | Regla 1 | Regla 2 | Regla 3 | Regla 4 |
| :--- | :---: | :---: | :---: | :---: |
| **Condiciones** | | | | |
| Â¿Evento notificable? | SÃ­ | SÃ­ | SÃ­ | No |
| Â¿Usuario tiene email registrado? | SÃ­ | No | SÃ­ | N/A |
| Â¿Correos habilitados en preferencias? | SÃ­ | N/A | No | N/A |
| Â¿SMTP disponible? | SÃ­ | N/A | N/A | N/A |
| **Acciones** | | | | |
| Enviar correo | X | | | |
| No enviar por falta de email | | X | | |
| No enviar por preferencia desactivada | | | X | |
| No enviar porque no existe evento | | | | X |

#### B.2. ParticiÃ³n de Equivalencia para correo del usuario

| Clase invÃ¡lida | Clase vÃ¡lida |
| :--- | :--- |
| Usuario sin correo registrado o con correo no vÃ¡lido. | Usuario con correo registrado y preferencias de correo activas. |
| **Comportamiento esperado:** el sistema no debe enviar correo. | **Comportamiento esperado:** el sistema debe enviar correo si existe evento notificable y SMTP disponible. |

### C. Casos de Prueba Derivados

| ID Caso | Pasos de ejecuciÃ³n resumidos | Datos de entrada / contexto | Resultado esperado |
| :--- | :--- | :--- | :--- |
| **CP-MOD7-008** | Activar preferencias de correo y generar un evento notificable. | Usuario con email registrado y SMTP disponible. | El sistema envÃ­a o programa el envÃ­o de correo. |
| **CP-MOD7-009** | Desactivar preferencias de correo y generar un evento notificable. | Usuario con correo registrado, pero correos desactivados. | El sistema no envÃ­a correo. |
| **CP-MOD7-010** | Generar evento notificable con usuario sin correo registrado. | Usuario sin email vÃ¡lido. | El sistema no envÃ­a correo. |

---

## 5. Matriz de Trazabilidad del DiseÃ±o

| Requisito funcional | Escenario asociado | Casos derivados | TÃ©cnica principal |
| :--- | :--- | :--- | :--- |
| **RF-7001** | ESC-7001, ESC-7002 | CP-MOD7-001, CP-MOD7-002, CP-MOD7-003, CP-MOD7-004, CP-MOD7-005 | ParticiÃ³n de Equivalencia / Flujo funcional |
| **RF-7002** | ESC-7002, ESC-7003 | CP-MOD7-004, CP-MOD7-006, CP-MOD7-007 | Tabla de DecisiÃ³n |
| **RF-7003** | ESC-7004 | CP-MOD7-008, CP-MOD7-009, CP-MOD7-010 | Tabla de DecisiÃ³n / ParticiÃ³n de Equivalencia |

---



