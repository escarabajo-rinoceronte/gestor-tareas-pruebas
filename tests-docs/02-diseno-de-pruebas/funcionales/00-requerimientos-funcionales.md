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
  <b>Proyecto:</b> HOT Tasking Manager — Documento de EspecificaciÃ³n de Requerimientos Funcionales (DERF) <br>
  <b>Fecha de Elaboración:</b> 12/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Documento de EspecificaciÃ³n de Requerimientos Funcionales (DERF)
**Proyecto:** HOTOSM Tasking Manager
**VersiÃ³n del Documento:** 1.0
**Tipo de AnÃ¡lisis:** IngenierÃ­a Inversa de Requisitos / AnÃ¡lisis de Caja Negra

---

## 1. DescripciÃ³n general del sistema

El presente documento formaliza los requerimientos funcionales del **HOTOSM Tasking Manager (TM)**, la herramienta principal de coordinaciÃ³n para el mapeo colaborativo del Equipo Humanitario de OpenStreetMap (HOT).

*   **Objeto de anÃ¡lisis:** La instancia oficial de producciÃ³n ([tasks.hotosm.org](https://tasks.hotosm.org)).
*   **Alcance:** El anÃ¡lisis abarca la funcionalidad estrictamente observable desde la interfaz grÃ¡fica de usuario (UI)
*   **Objetivo:** Establecer una lÃ­nea base documentada, con alta trazabilidad que sirva como insumo oficial para el diseÃ±o, ejecuciÃ³n y automatizaciÃ³n de pruebas de software (Caja Negra, Pruebas de IntegraciÃ³n y Pruebas Unitarias).

---

## 2. Actores del sistema

El sistema implementa un modelo de Control de Acceso Basado en Roles (RBAC) superpuesto con un sistema de "Niveles de Experiencia" calculados dinÃ¡micamente.

| ID | Nombre del Actor | DescripciÃ³n Funcional |
| :--- | :--- | :--- |
| **ACT-01** | **Usuario AnÃ³nimo** | Visitante sin autenticar. Sus capacidades se limitan a la exploraciÃ³n de proyectos pÃºblicos, visualizaciÃ³n de estadÃ­sticas globales y acceso a documentaciÃ³n. |
| **ACT-02** | **Mapper** | Usuario autenticado vÃ­a OpenStreetMap. Posee un nivel de experiencia calculado automÃ¡ticamente (`BEGINNER`, `INTERMEDIATE`, `ADVANCED`). Puede bloquear, mapear y comentar tareas. |
| **ACT-03** | **Validator** | Usuario con permisos elevados (por su nivel de experiencia o por membresÃ­a en un equipo de validaciÃ³n) autorizado para auditar, aprobar o rechazar el mapeo realizado por otros usuarios. |
| **ACT-04** | **Project Manager (PM)** | Administrador a nivel de OrganizaciÃ³n o Equipo. Tiene privilegios para crear proyectos, definir Ãreas de InterÃ©s (AOI), asignar permisos, transferir propiedad y administrar membresÃ­as. |
| **ACT-05** | **SysAdmin** | Administrador global de la plataforma. Posee acceso irrestricto para gestionar campaÃ±as, licencias globales, roles de otros usuarios y configuraciones del sistema. |
| **ACT-06** | **Sistema** | Procesos automatizados en segundo plano (Cron Jobs / Background Tasks) encargados de liberar tareas expiradas, actualizar estadÃ­sticas contra APIs externas (Ohsome) y disparar notificaciones. |

---

## 3. MÃ³dulos del sistema

La arquitectura funcional del Tasking Manager se ha segmentado lÃ³gicamente en los siguientes mÃ³dulos para facilitar la cobertura de pruebas.

| ID | Nombre del MÃ³dulo | DescripciÃ³n |
| :--- | :--- | :--- |
| **MOD-01** | **AutenticaciÃ³n y Perfil** | GestiÃ³n del ciclo de vida de la sesiÃ³n (OAuth 2.0 con OSM), cÃ¡lculo de mÃ©tricas de usuario, niveles de mapeo y aceptaciÃ³n de licencias. |
| **MOD-02** | **ExploraciÃ³n de Proyectos** | Motor de bÃºsqueda, filtros avanzados (por estado, dificultad, campaÃ±as), ordenamiento y renderizado en mapa (BBOX). |
| **MOD-03** | **EjecuciÃ³n de Mapeo (Tasking)** | LÃ³gica core de bloqueo/desbloqueo de tareas, divisiÃ³n de grillas (Split) e integraciÃ³n con editores geogrÃ¡ficos externos (iD, JOSM, Rapid). |
| **MOD-04** | **Proceso de ValidaciÃ³n** | Flujo de control de calidad. Incluye bloqueo mÃºltiple, prevenciÃ³n de auto-validaciÃ³n y transiciones de estado (`VALIDATED`, `INVALIDATED`). |
| **MOD-05** | **AdministraciÃ³n de Proyectos** | CreaciÃ³n de proyectos (AOI, Tareas por grilla o arbitrarias), clonaciÃ³n, configuraciÃ³n de metadatos y privacidad. |
| **MOD-06** | **Gobernanza (Equipos y Orgs)** | GestiÃ³n jerÃ¡rquica de permisos. CreaciÃ³n de Organizaciones, Equipos, flujos de invitaciÃ³n/solicitud de uniÃ³n y asignaciÃ³n de proyectos. |
| **MOD-07** | **ComunicaciÃ³n y Alertas** | Subsistema de notificaciones (in-app y email), chat general de proyectos, menciones (`@usuario`) y comentarios por tarea. |

---

## 4. CatÃ¡logo de Requerimientos Funcionales

A continuaciÃ³n, se detallan los requerimientos funcionales extraÃ­dos y deducidos, estructurados para su directa conversiÃ³n en Casos de Prueba.

### MOD-01: AutenticaciÃ³n y Perfil
| ID | Nombre | DescripciÃ³n Funcional | Actor | MÃ³dulo | Prioridad | Dependencias |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RF-1001** | **Login delegado (OAuth)** | El sistema debe autenticar al usuario redirigiÃ©ndolo al proveedor OAuth de OSM y crear una sesiÃ³n local basada en el token devuelto. | ACT-01 | MOD-01 | Alta | - |
| **RF-1002** | **CÃ¡lculo de nivel de Mapper** | Tras la autenticaciÃ³n, el sistema debe consultar la API de OSM/Ohsome para contabilizar *changesets* y calcular el nivel del usuario (`BEGINNER`, `INTERMEDIATE`, `ADVANCED`). | ACT-06 | MOD-01 | Alta | RF-1001 |
| **RF-1003** | **AceptaciÃ³n de Licencias** | Si un proyecto tiene una licencia asignada, el sistema debe bloquear la contribuciÃ³n hasta que el usuario confirme la aceptaciÃ³n de los tÃ©rminos. | ACT-02 | MOD-01 | Alta | RF-1001, RF-3001 |
| **RF-1004** | **ActualizaciÃ³n de Perfil** | El usuario debe poder modificar su correo, gÃ©nero, y preferencias de notificaciones desde la interfaz de ajustes de perfil. | ACT-02 | MOD-01 | Media | RF-1001 |

### MOD-02: ExploraciÃ³n de Proyectos
| ID | Nombre | DescripciÃ³n Funcional | Actor | MÃ³dulo | Prioridad | Dependencias |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RF-2001** | **Filtros de BÃºsqueda** | El sistema debe permitir filtrar proyectos por nivel de dificultad, estado (`DRAFT`, `PUBLISHED`, `ARCHIVED`), campaÃ±a y tipo de mapeo. | ACT-01 | MOD-02 | Alta | - |
| **RF-2002** | **BÃºsqueda por BBOX** | El sistema debe renderizar en la vista de mapa solo los proyectos cuyos polÃ­gonos intersecten con las coordenadas de la vista actual (Bounding Box). | ACT-01 | MOD-02 | Media | - |
| **RF-2003** | **RestricciÃ³n de Proyectos Privados** | Los proyectos marcados como privados no deben ser listados en la exploraciÃ³n general a menos que el usuario pertenezca a un equipo autorizado o sea Admin. | ACT-02 | MOD-02 | Alta | RF-1001 |

### MOD-03: EjecuciÃ³n de Mapeo (Tasking)
| ID | Nombre | DescripciÃ³n Funcional | Actor | MÃ³dulo | Prioridad | Dependencias |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RF-3001** | **Bloqueo singular de tarea** | El sistema debe permitir a un Mapper bloquear una tarea en estado `READY` cambiÃ¡ndola a `LOCKED_FOR_MAPPING`. Solo se permite una tarea en mapeo a la vez por usuario. | ACT-02 | MOD-03 | CrÃ­tica | RF-1001 |
| **RF-3002** | **IntegraciÃ³n de Editor Web** | Al seleccionar iD o Rapid, el sistema debe inyectar la URL base con parÃ¡metros geogrÃ¡ficos (Zoom, X, Y) y comentarios predeterminados (`changesetComment`). | ACT-02 | MOD-03 | Alta | RF-3001 |
| **RF-3003** | **IntegraciÃ³n de Editor Local (JOSM)** | Al seleccionar JOSM, el sistema debe comprobar disponibilidad local (HTTP GET `127.0.0.1:8111`). Si no responde, debe mostrar un modal de error (`JOSMError`). | ACT-02 | MOD-03 | Alta | RF-3001 |
| **RF-3004** | **EnvÃ­o de estado (Submit)** | El sistema debe permitir desbloquear la tarea asignando un estado final: `MAPPED` (completada), `BADIMAGERY` (no mapeable) o regresar a `READY`. | ACT-02 | MOD-03 | CrÃ­tica | RF-3001 |
| **RF-3005** | **DivisiÃ³n de tarea (Split)** | Un Mapper debe poder dividir una tarea bloqueada en 4 sub-tareas mÃ¡s pequeÃ±as, sujeto al lÃ­mite mÃ¡ximo de zoom configurado. | ACT-02 | MOD-03 | Media | RF-3001 |
| **RF-3006** | **LiberaciÃ³n por tiempo (Auto-unlock)** | El sistema debe revertir automÃ¡ticamente tareas bloqueadas a estado `READY` si el tiempo de bloqueo excede la configuraciÃ³n (`autoUnlockSeconds`). | ACT-06 | MOD-03 | Alta | RF-3001 |

### MOD-04: Proceso de ValidaciÃ³n
| ID | Nombre | DescripciÃ³n Funcional | Actor | MÃ³dulo | Prioridad | Dependencias |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RF-4001** | **Bloqueo de tareas para validaciÃ³n** | El sistema debe permitir a un Validator bloquear una o mÃºltiples tareas en estado `MAPPED` (pasando a `LOCKED_FOR_VALIDATION`). | ACT-03 | MOD-04 | Alta | RF-3004 |
| **RF-4002** | **PrevenciÃ³n de Auto-ValidaciÃ³n** | El sistema debe rechazar la validaciÃ³n si el usuario intentando validar es el mismo que registrÃ³ el estado `MAPPED` de la tarea. | ACT-03 | MOD-04 | Alta | RF-4001 |
| **RF-4003** | **EvaluaciÃ³n de calidad** | El sistema debe permitir clasificar la tarea revisada como `VALIDATED` (aprobada) o `INVALIDATED` (rechazada, vuelve a requerir mapeo). | ACT-03 | MOD-04 | CrÃ­tica | RF-4001 |
| **RF-4004** | **Deshacer acciÃ³n (Undo)** | El usuario debe poder revertir su propia Ãºltima acciÃ³n en una tarea, regresando el estado previo, registrando un comentario en el historial. | ACT-02 | MOD-04 | Media | RF-3004, RF-4003 |

### MOD-05: AdministraciÃ³n de Proyectos
| ID | Nombre | DescripciÃ³n Funcional | Actor | MÃ³dulo | Prioridad | Dependencias |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RF-5001** | **CreaciÃ³n de Ãrea de InterÃ©s (AOI)** | El sistema debe procesar archivos GeoJSON/KML o dibujos en pantalla para definir el polÃ­gono general del proyecto (AOI) y validarlo contra `MAX_AOI_AREA`. | ACT-04 | MOD-05 | Alta | RF-1001 |
| **RF-5002** | **GeneraciÃ³n de Grilla** | El sistema debe calcular y recortar polÃ­gonos secundarios (Grid) para generar las Tareas dentro del AOI de forma automÃ¡tica. | ACT-04 | MOD-05 | Alta | RF-5001 |
| **RF-5003** | **Privacidad y Permisos** | El sistema debe permitir configurar la visibilidad (PÃºblico/Privado) y establecer quÃ© niveles o Equipos pueden Mapear y/o Validar. | ACT-04 | MOD-05 | Alta | - |
| **RF-5004** | **ClonaciÃ³n de Proyectos** | El sistema debe permitir generar un nuevo proyecto copiando el AOI, grilla, intereses y descripciÃ³n de un proyecto preexistente. | ACT-04 | MOD-05 | Media | - |
| **RF-5005** | **Transferencia de Propiedad** | El autor de un proyecto debe poder transferir la propiedad del mismo a otro usuario que posea privilegios de PM o Admin. | ACT-04 | MOD-05 | Baja | - |

### MOD-06: Gobernanza (Organizaciones y Equipos)
| ID | Nombre | DescripciÃ³n Funcional | Actor | MÃ³dulo | Prioridad | Dependencias |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RF-6001** | **GestiÃ³n de Equipos** | Un Admin o PM debe poder crear equipos, asignarles visibilidad (`PUBLIC`/`PRIVATE`) y mÃ©todo de ingreso (`ANY`, `BY_REQUEST`, `BY_INVITE`). | ACT-04 | MOD-06 | Alta | - |
| **RF-6002** | **Solicitud de MembresÃ­a** | Si el equipo es `BY_REQUEST`, un Mapper puede solicitar unirse, generando una notificaciÃ³n a los administradores del equipo. | ACT-02 | MOD-06 | Media | RF-6001 |
| **RF-6003** | **AprobaciÃ³n de MembresÃ­a** | Un Manager del equipo debe poder aceptar solicitudes de uniÃ³n, cambiando el estado del usuario dentro del equipo a Activo (`MEMBER`). | ACT-04 | MOD-06 | Media | RF-6002 |

### MOD-07: ComunicaciÃ³n y Notificaciones
| ID | Nombre | DescripciÃ³n Funcional | Actor | MÃ³dulo | Prioridad | Dependencias |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RF-7001** | **Comentarios por Tarea** | El sistema debe permitir adjuntar comentarios de texto plano o Markdown asociados al historial de una tarea especÃ­fica. | ACT-02 | MOD-07 | Alta | - |
| **RF-7002** | **Notificaciones in-app** | El sistema debe notificar al usuario cuando su tarea sea `INVALIDATED`, cuando sea mencionado (`@username`) o cuando suba de nivel de mapeo. | ACT-06 | MOD-07 | Alta | RF-4003 |
| **RF-7003** | **EnvÃ­o de Emails** | Si el usuario tiene correos habilitados, el sistema debe despachar alertas SMTP para notificaciones crÃ­ticas e hitos de finalizaciÃ³n de proyectos. | ACT-06 | MOD-07 | Media | RF-1004 |


