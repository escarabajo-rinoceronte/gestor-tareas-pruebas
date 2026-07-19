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
  <b>Proyecto:</b> HOT Tasking Manager — EjecuciÃ³n de Casos de Prueba del MOD-01: AutenticaciÃ³n y Perfil <br>
  <b>Fecha de Elaboración:</b> 12/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# EjecuciÃ³n de Casos de Prueba del MOD-01: AutenticaciÃ³n y Perfil

## 1. ESC-1001: AutenticaciÃ³n Delegada de Usuario vÃ­a OAuth 2.0 con OSM

### 1.1. EjecuciÃ³n de CP-1001-01

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-1001-01** | Validar ciclo de inicio de sesiÃ³n exitoso autorizando el acceso en la interfaz externa de OSM. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema completa la transiciÃ³n a `Autenticacion exitosa`, cargando la interfaz local en el estado `SesionActiva` con el Dashboard de mapeo disponible. | La interfaz cargÃ³ el Dashboard correctamente y mostrÃ³ el avatar del usuario en la barra superior. |

| Evidencia |
| :-- |
| RedirecciÃ³n y AutorizaciÃ³n en OSM<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-01-ejecucion-autenticacion-perfil/CP-1001-01-osm-auth.png" width="800px" alt="CP-1001-01 - RedirecciÃ³n y autorizaciÃ³n en OpenStreetMap"></a><br>Vista de la interfaz externa de OpenStreetMap solicitando permisos de acceso. |
| Dashboard con SesiÃ³n Activa<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-01-ejecucion-autenticacion-perfil/CP-1001-01-dashboard.png" width="800px" alt="CP-1001-01 - Dashboard con sesiÃ³n activa"></a><br>Interfaz del Tasking Manager en estado SesionActiva con el perfil del Mapper cargado. |

---

### 1.2. EjecuciÃ³n de CP-1001-02

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-1001-02** | Validar el comportamiento de la interfaz al denegar o cancelar los permisos en la plataforma externa de OSM. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| Al pasar al estado `AutenticandoOSM`, el sistema detecta la denegaciÃ³n y ejecuta la transiciÃ³n `Cancelacion o error`, devolviendo de inmediato la interfaz del usuario al estado inicial de `NoAutenticado`. | El sistema interceptÃ³ la cancelaciÃ³n y regresÃ³ a la Landing Page pÃºblica sin loguear. |

| Evidencia |
| :-- |
| CancelaciÃ³n de AutorizaciÃ³n<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-01-ejecucion-autenticacion-perfil/CP-1001-02-cancel.png" width="800px" alt="CP-1001-02 - CancelaciÃ³n de autorizaciÃ³n en OSM"></a><br>Clic en el botÃ³n 'Denegar' dentro de la pasarela de OSM. |

---

### 1.3. EjecuciÃ³n de CP-1001-03

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-1001-03** | Validar la destrucciÃ³n de la sesiÃ³n local al seleccionar la opciÃ³n de Log Out. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La aplicaciÃ³n destruye la sesiÃ³n de forma local y redirige la interfaz del usuario de regreso al estado inicial de `NoAutenticado` (Landing Page pÃºblica). | Se limpiÃ³ el token del navegador y la UI regresÃ³ instantÃ¡neamente a la vista pÃºblica de invitado. |

| Evidencia |
| :-- |
| Cierre de SesiÃ³n Exitoso<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-01-ejecucion-autenticacion-perfil/CP-1001-03-logout.png" width="800px" alt="CP-1001-03 - Cierre de sesiÃ³n exitoso"></a><br>ConfirmaciÃ³n visual de la Landing Page pÃºblica tras destruir la sesiÃ³n local. |

---

## 2. ESC-1002: ClasificaciÃ³n Automatizada y VisualizaciÃ³n del Nivel del Mapper

### 2.1. EjecuciÃ³n de CP-1002-01

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-1002-01** | Validar que la interfaz cargue y muestre explÃ­citamente la etiqueta BEGINNER con el valor base de 0 cambios. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La interfaz grÃ¡fica de usuario carga el perfil mostrando explÃ­citamente la etiqueta con el texto **BEGINNER**. | La UI procesÃ³ el valor base de forma limpia, renderizando la medalla de nivel en gris con la palabra BEGINNER junto al contador en cero. |

| Evidencia |
| :-- |
| Perfil con Nivel Base Beginner<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-01-ejecucion-autenticacion-perfil/CP-1002-01-nivel-beginner-base.png" width="800px" alt="CP-1002-01 - Perfil inicial con nivel BEGINNER"></a><br>Captura de la pantalla de perfil mostrando el contador de cambios en 0 y la etiqueta BEGINNER activa. |

---

### 2.2. EjecuciÃ³n de CP-1002-02

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-1002-02** | Validar que la interfaz mantenga la consistencia visual de la etiqueta BEGINNER en el tope exacto de 250 cambios. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La interfaz grÃ¡fica de usuario carga el perfil mostrando explÃ­citamente la etiqueta con el texto **BEGINNER**. | La pantalla procesÃ³ el lÃ­mite superior de la primera clase, manteniendo la etiqueta de BEGINNER fija y visualizando la barra de progreso al 100%. |

| Evidencia |
| :-- |
| Perfil en LÃ­mite Superior Beginner<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-01-ejecucion-autenticacion-perfil/CP-1002-02-nivel-beginner-tope.png" width="800px" alt="CP-1002-02 - Perfil en lÃ­mite superior BEGINNER"></a><br>Captura de la interfaz de usuario con 250 cambios reflejando el tope del rango inicial. |

---

### 2.3. EjecuciÃ³n de CP-1002-03

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-1002-03** | Validar que la interfaz mute automÃ¡ticamente la medalla a INTERMEDIATE al superar la frontera con 251 cambios. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema calcula la transiciÃ³n y la interfaz del usuario cambia de forma automÃ¡tica la medalla a la categorÃ­a **INTERMEDIATE**. | Al detectar el cambio nÃºmero 251, la interfaz actualizÃ³ asÃ­ncronamente el componente visual, inyectando la etiqueta INTERMEDIATE con su respectivo color distintivo. |

| Evidencia |
| :-- |
| TransiciÃ³n a Nivel Intermediate<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-01-ejecucion-autenticacion-perfil/CP-1002-03-cambio-intermediate.png" width="800px" alt="CP-1002-03 - Interfaz con medalla INTERMEDIATE"></a><br>Captura de la medalla actualizada a INTERMEDIATE inmediatamente tras cruzar el lÃ­mite fronterizo. |

---

### 2.4. EjecuciÃ³n de CP-1002-04

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-1002-04** | Validar la consistencia visual de la etiqueta INTERMEDIATE en su lÃ­mite estricto de 1000 cambios. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La interfaz grÃ¡fica de usuario mantiene la consistencia visual mostrando la etiqueta fija de **INTERMEDIATE**. | El sistema mantuvo la estabilidad visual del perfil sin saltos errÃ¡ticos, renderizando correctamente la medalla INTERMEDIATE fija en el valor tope del rango medio. |

| Evidencia |
| :-- |
| Perfil en LÃ­mite de Clase Intermedia<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-01-ejecucion-autenticacion-perfil/CP-1002-04-intermediate-tope.png" width="800px" alt="CP-1002-04 - Perfil en tope de INTERMEDIATE"></a><br>Vista del perfil del Mapper con el contador exactamente en 1000 cambios y la etiqueta intermedia estable. |

---

### 2.5. EjecuciÃ³n de CP-1002-05

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-1002-05** | Validar la mutaciÃ³n inmediata en la interfaz a la etiqueta ADVANCED al registrar 1001 cambios mappers. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema evalÃºa el cambio de rango de forma inmediata y la interfaz de usuario renderiza la etiqueta de mÃ¡ximo nivel: **ADVANCED**. | La pantalla asimilÃ³ la ruptura del lÃ­mite intermedio por un dÃ­gito, renderizando instantÃ¡neamente la medalla dorada de mÃ¡ximo rango con el texto ADVANCED. |

| Evidencia |
| :-- |
| Medalla de MÃ¡ximo Nivel Advanced<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-01-ejecucion-autenticacion-perfil/CP-1002-05-nivel-advanced.png" width="800px" alt="CP-1002-05 - Interfaz con medalla ADVANCED"></a><br>Captura de pantalla de la barra de usuario mostrando la insignia final de ADVANCED activa en la UI. |

---

## 3. ESC-1003: RestricciÃ³n de ContribuciÃ³n por AceptaciÃ³n de Licencias de Proyecto

### 3.1. EjecuciÃ³n de CP-1003-01

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-1003-01** | Validar que el sistema bloquee la carga de la interfaz del proyecto restrictivo si el usuario no estÃ¡ autenticado. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| El sistema bloquea la carga de la interfaz del proyecto, redirige de inmediato al usuario a la Landing Page pÃºblica (`CS-1 = V`) y solicita el login vÃ­a OSM. | La interfaz interrumpiÃ³ el acceso directo a la URL protegida, redirigiendo de forma forzada a la Landing Page e invocando la alerta de inicio de sesiÃ³n requerido. |

| Evidencia |
| :-- |
| **RedirecciÃ³n Forzada por Falta de SesiÃ³n**<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-01-ejecucion-autenticacion-perfil/CP-1003-01-redireccion-login.png" width="800px" alt="CP-1003-01 - RedirecciÃ³n forzada a Landing Page"></a><br>Captura de la pantalla pÃºblica tras el intento de acceso directo sin un token de sesiÃ³n activo.<br><br>**Pantalla de AutenticaciÃ³n Requerida**<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-01-ejecucion-autenticacion-perfil/CP-1003-01-login1.png" width="800px" alt="CP-1003-01 - Formulario de login requerido"></a><br>Detalle del modal o vista de inicio de sesiÃ³n que se le presenta al usuario para recuperar el acceso. |



---

