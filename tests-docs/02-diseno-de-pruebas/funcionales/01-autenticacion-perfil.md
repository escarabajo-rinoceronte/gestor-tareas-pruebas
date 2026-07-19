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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — DiseÃ±o de Pruebas Funcionales: MOD-01 - AutenticaciÃ³n y Perfil</td></tr>
      <tr><td class="label">Fecha</td><td>12/06/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# DiseÃ±o de Pruebas Funcionales: MOD-01 - AutenticaciÃ³n y Perfil
**VersiÃ³n del Documento:** 1.0
**Tipo de AnÃ¡lisis:** DiseÃ±o de Pruebas de Sistema (Caja Negra)

---

## 1. Contexto del MÃ³dulo
Este mÃ³dulo gestiona el ciclo de vida de la identidad, sesiÃ³n y experiencia del usuario en la plataforma. Es responsable de controlar el acceso seguro mediante OAuth 2.0 con OpenStreetMap, calcular y actualizar el nivel tÃ©cnico del mapper (BEGINNER, INTERMEDIATE, ADVANCED) segÃºn sus mÃ©tricas, restringir contribuciones mediante la aceptaciÃ³n obligatoria de licencias, y permitir la personalizaciÃ³n de ajustes del perfil desde la interfaz.

*Para consultar el detalle exhaustivo de los actores, restricciones y reglas de negocio, referirse al [CatÃ¡logo de Requerimientos Funcionales](/tests-docs/02-diseno-de-pruebas/funcionales/00-requerimientos-funcionales.md).*

---

## 2. Estrategia de DiseÃ±o de Pruebas

### 2.1. Enfoque general
Las pruebas se centrarÃ¡n de manera estricta en la validaciÃ³n visual y de comportamiento a nivel de Interfaz de Usuario (UI). La estrategia se enfocarÃ¡ en verificar la correcta sincronizaciÃ³n de datos con el proveedor externo (OSM), el bloqueo preventivo de funciones de mapeo cuando existan licencias pendientes de aprobaciÃ³n, y la correcta respuesta visual ante cambios en el formulario de configuraciÃ³n del perfil del usuario.

El alcance de estas pruebas cubre las interacciones de los siguientes actores clave del sistema:
* **ACT-01 Usuario AnÃ³nimo:** Evaluando su restricciÃ³n de acceso a menÃºs privados y su transiciÃ³n hacia la pasarela de autenticaciÃ³n.
* **ACT-02 Mapper:** Validando su experiencia visual en el Dashboard, la ediciÃ³n de sus preferencias y el impacto de su nivel calculado en la interfaz.
* **ACT-06 Sistema:** Verificando cÃ³mo los procesos automatizados en segundo plano (consultas de APIs externas como Ohsome) impactan y actualizan los datos visuales del perfil del Mapper en tiempo real.

| Actor de Impacto | Rol en este MÃ³dulo | Contexto de Prueba |
| :--- | :--- | :--- |
| **ACT-01** Usuario AnÃ³nimo | Solicitante de acceso | Intento de Login / NavegaciÃ³n pÃºblica inicial (RF-1001). |
| **ACT-02** Mapper | Usuario core autenticado | AceptaciÃ³n de licencias (RF-1003) y actualizaciÃ³n de datos (RF-1004). |
| **ACT-06** Sistema | Proveedor de datos asÃ­ncrono | CÃ¡lculo automÃ¡tico y visualizaciÃ³n del nivel tÃ©cnico (RF-1002). |

### 2.2. TÃ©cnicas de Caja Negra Utilizadas

* **TransiciÃ³n de Estados:** Utilizada para modelar y evaluar el flujo del login delegado (RF-1001) y la actualizaciÃ³n de perfil (RF-1004). Permite verificar cÃ³mo cambia la interfaz entre diferentes estados (ej. Usuario AnÃ³nimo, Pantalla Externa de OSM, SesiÃ³n Activa, o Alertas de ValidaciÃ³n en el formulario) basÃ¡ndose puramente en las interacciones y clics del usuario.
* **ParticiÃ³n de Equivalencia (PE)** y **AnÃ¡lisis de Valores LÃ­mite (AVL):** Aplicadas de manera conjunta para el cÃ¡lculo del nivel de Mapper (RF-1002). Permiten agrupar los rangos numÃ©ricos de las ediciones en clases representativas y evaluar con total precisiÃ³n en la pantalla los "bordes" o fronteras exactas donde la etiqueta visual del nivel debe cambiar de forma automÃ¡tica.
* **Tablas de DecisiÃ³n:** Utilizada para la funcionalidad de aceptaciÃ³n de licencias (RF-1003). Permite validar de forma rigurosa las combinaciones lÃ³gicas de entrada (estado de la autenticaciÃ³n y configuraciÃ³n de restricciones del proyecto) para asegurar que el sistema ejecute correctamente la acciÃ³n de habilitar o mantener bloqueado el botÃ³n de contribuciÃ³n en el mapa.

---

## 3. Especificaciones de Escenarios y Casos de Prueba

### 3.1. Escenario: ESC-1001 - AutenticaciÃ³n Delegada de Usuario vÃ­a OAuth 2.0 con OSM

**A. DefiniciÃ³n del Escenario**
| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar el ciclo de vida del inicio y cierre de sesiÃ³n del usuario en la interfaz del Tasking Manager, siguiendo las transiciones de estado del protocolo OAuth 2.0 con OpenStreetMap. |
| **RF Asociados** | RF-1001 |
| **Precondiciones** | El usuario debe contar con una cuenta activa y credenciales vÃ¡lidas en la plataforma oficial openstreetmap.org. El sistema debe encontrarse en la Landing Page pÃºblica. |
| **TÃ©cnicas aplicadas**| TransiciÃ³n de Estados |
| **Resultado Esperado** | La interfaz debe guiar al usuario a travÃ©s del flujo externo de autorizaciÃ³n y, tras el Ã©xito o la cancelaciÃ³n del proceso, actualizar el estado de la pantalla local de forma segura y coherente. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**
Para este escenario, se modela el comportamiento del sistema mediante los componentes de la tÃ©cnica de **TransiciÃ³n de Estados** extraÃ­dos del diagrama oficial del mÃ³dulo:

* **Estados del Sistema Identificados:**
    * `NoAutenticado`: Estado inicial pÃºblico donde el usuario navega como invitado en la interfaz.
    * `RedirigidoOSM`: El sistema deriva el control visual a la URL externa de OpenStreetMap.
    * `AutenticandoOSM`: Estado intermedio de callback donde el Tasking Manager procesa la respuesta del token en segundo plano.
    * `SesionActiva`: Estado final exitoso donde el usuario accede a su perfil y dashboard con sus datos visibles en pantalla.
* **Transiciones / Eventos Evaluados:**
    * `Inicia autenticacion OAuth`
    * `Usuario en OSM`
    * `Autenticacion exitosa`
    * `Cancelacion o error`
    * `Cierre de sesion`

![Diagrama de TransiciÃ³n de Estados - ESC-1001](/tests-docs/02-diseno-de-pruebas/funcionales/img/transicion-estado-ESC-1001.png) 

---

**C. Casos de Prueba Derivados**

| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada (Clases aplicadas) | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CP-1001-01** | 1. Ingresar a la URL principal del Tasking Manager (`NoAutenticado`).<br>2. Hacer clic en el botÃ³n "Log In" (`Inicia autenticacion OAuth`).<br>3. En la interfaz externa de OSM (`RedirigidoOSM`), ingresar credenciales y autorizar (`Usuario en OSM`).<br>4. Esperar el procesamiento de la respuesta (`AutenticandoOSM`). | **Credenciales OSM:** VÃ¡lidas.<br>**AcciÃ³n en OSM:** Autorizar acceso. | El sistema completa la transiciÃ³n a `Autenticacion exitosa`, cargando la interfaz local en el estado `SesionActiva` con el Dashboard de mapeo disponible. |
| **CP-1001-02** | 1. Ingresar a la URL principal del Tasking Manager (`NoAutenticado`).<br>2. Hacer clic en el botÃ³n "Log In" (`Inicia autenticacion OAuth`).<br>3. En la interfaz externa de OSM (`RedirigidoOSM`), hacer clic en el botÃ³n "Denegar" o "Cancelar". | **Credenciales OSM:** N/A.<br>**AcciÃ³n en OSM:** Denegar o Cancelar. | Al pasar al estado `AutenticandoOSM`, el sistema detecta la denegaciÃ³n y ejecuta la transiciÃ³n `Cancelacion o error`, devolviendo de inmediato la interfaz del usuario al estado inicial de `NoAutenticado`. |
| **CP-1001-03** | 1. Estando dentro de la plataforma con la sesiÃ³n iniciada (`SesionActiva`).<br>2. Desplegar el menÃº de perfil en la esquina superior derecha.<br>3. Hacer clic en la opciÃ³n "Log Out / Cerrar SesiÃ³n" (`Cierre de sesion`). | **Estado Inicial:** `SesionActiva`.<br>**AcciÃ³n de Salida:** Clic en Logout. | La aplicaciÃ³n destruye la sesiÃ³n de forma local y redirige la interfaz del usuario de regreso al estado inicial de `NoAutenticado` (Landing Page pÃºblica). |

---

### 3.2. Escenario: ESC-1002 - ClasificaciÃ³n Automatizada y VisualizaciÃ³n del Nivel del Mapper

**A. DefiniciÃ³n del Escenario**
| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el sistema (ACT-06) calcule correctamente el nivel tÃ©cnico de experiencia del usuario basÃ¡ndose en sus ediciones consumidas por API, y que la interfaz de usuario muestre la etiqueta correspondiente de manera exacta. |
| **RF Asociados** | RF-1002 |
| **Precondiciones** | El usuario (ACT-02) debe haber iniciado sesiÃ³n de forma exitosa mediante OAuth (RF-1001) y encontrarse visualizando la secciÃ³n de su perfil o el menÃº de mÃ©tricas del sistema. |
| **TÃ©cnicas aplicadas**| ParticiÃ³n de Equivalencia (PE) y AnÃ¡lisis de Valores LÃ­mite (AVL) |
| **Resultado Esperado** | La interfaz grÃ¡fica debe actualizar de forma automÃ¡tica la medalla o etiqueta de nivel (`BEGINNER`, `INTERMEDIATE`, `ADVANCED`) en el segundo exacto en que las mÃ©tricas del usuario toquen las fronteras numÃ©ricas establecidas. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**

#### B.1. ParticiÃ³n de Equivalencia (PE)
Se agrupa el universo de datos del contador numÃ©rico de ediciones en base a las categorÃ­as lÃ³gicas del sistema:

| Clase VÃ¡lida | Clases No VÃ¡lidas | Rango de Ediciones |
| :--- | :--- | :---: |
| **PE-V01** (Beginner) | - | de 0 a 250 |
| **PE-V02** (Intermediate) | - | de 251 a 1000 |
| **PE-V03** (Advanced) | - | mas 1001 |
| - | **PE-NV01** (Valores Corruptos) | < 0 |

#### B.2. AnÃ¡lisis de Valores LÃ­mite (AVL)
Se identifican los valores de prueba crÃ­ticos situados en los extremos numÃ©ricos exactos de las particiones:

| LÃ­mite Inferior VÃ¡lido | LÃ­mite Inferior No VÃ¡lido | LÃ­mite Superior VÃ¡lido | LÃ­mite Superior No VÃ¡lido | Rango de Clase Asociado |
| :---: | :---: | :---: | :---: | :---: |
| **0** | **-1** | **250** | **251** | Rango Beginner |
| **251** | **250** | **1000** | **1001** | Rango Intermediate |
| **1001** | **1000** | **no especificado** | - | Rango Advanced |

---

**C. Casos de Prueba Derivados**

| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada (Clases aplicadas) | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CP-1002-01** | 1. Acceder al Tasking Manager con un perfil que posea el valor base de la escala de mappers. | **Total Changesets:** 0 <br>*(LÃ­mite Inferior VÃ¡lido)* | La interfaz grÃ¡fica de usuario carga el perfil mostrando explÃ­citamente la etiqueta con el texto **BEGINNER**. |
| **CP-1002-02** | 1. Acceder al Tasking Manager con un perfil que posea exactamente el tope de la clase principiante. | **Total Changesets:** 250 <br>*(LÃ­mite Superior VÃ¡lido)* | La interfaz grÃ¡fica de usuario carga el perfil mostrando explÃ­citamente la etiqueta con el texto **BEGINNER**. |
| **CP-1002-03** | 1. Acceder al Tasking Manager con un perfil que posea el valor inmediatamente superior a la frontera Beginner. | **Total Changesets:** 251 <br>*(LÃ­mite Superior No VÃ¡lido)* | El sistema calcula la transiciÃ³n y la interfaz del usuario cambia de forma automÃ¡tica la medalla a la categorÃ­a **INTERMEDIATE**. |
| **CP-1002-04** | 1. Acceder al Tasking Manager con un perfil que se encuentre en el lÃ­mite estricto de la clase intermedia. | **Total Changesets:** 1000 <br>*(LÃ­mite Superior VÃ¡lido)* | La interfaz grÃ¡fica de usuario mantiene la consistencia visual mostrando la etiqueta fija de **INTERMEDIATE**. |
| **CP-1002-05** | 1. Acceder al Tasking Manager con un perfil que rompa el lÃ­mite intermedio por una sola ediciÃ³n. | **Total Changesets:** 1001 <br>*(LÃ­mite Superior No VÃ¡lido)* | El sistema evalÃºa el cambio de rango de forma inmediata y la interfaz de usuario renderiza la etiqueta de mÃ¡ximo nivel: **ADVANCED**. |

---

### 3.3. Escenario: ESC-1003 - RestricciÃ³n de ContribuciÃ³n por AceptaciÃ³n de Licencias de Proyecto

**A. DefiniciÃ³n del Escenario**
| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que la interfaz restrinja el acceso a las funciones de mapeo de un proyecto cuando este exija tÃ©rminos legales especÃ­ficos, impidiendo la contribuciÃ³n hasta que el usuario confirme su aceptaciÃ³n. |
| **RF Asociados** | RF-1003 (Dependiente de RF-1001) |
| **Precondiciones** | El usuario (ACT-02) intenta interactuar con la vista de asignaciÃ³n de tareas cartogrÃ¡ficas de un proyecto especÃ­fico. |
| **TÃ©cnicas aplicadas**| Tablas de DecisiÃ³n |
| **Resultado Esperado** | La interfaz de usuario debe bloquear dinÃ¡micamente los botones de interacciÃ³n cartogrÃ¡fica y forzar la apariciÃ³n de un componente modal/banner legal, el cual se liberarÃ¡ Ãºnicamente al registrar la confirmaciÃ³n del usuario. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**
Para este escenario, se modela el comportamiento lÃ³gico de la interfaz mediante los componentes de la tÃ©cnica de **Tablas de DecisiÃ³n**, mapeando las variables de entrada y las respuestas visuales del sistema:

* **Condiciones de Entrada (Controles de la UI):**
    * `CE-1`: Â¿El usuario cuenta con una sesiÃ³n autenticada activa? (RF-1001)
    * `CE-2`: Â¿El proyecto seleccionado exige la firma/aceptaciÃ³n de una licencia?
    * `CE-3`: Â¿El usuario hace clic en "Aceptar tÃ©rminos" en la ventana modal/banner?
* **Condiciones de Salida (Resultados en la UI):**
    * `CS-1`: Redirigir de forma inmediata a la Landing Page pÃºblica y forzar el Login.
    * `CS-2`: Desplegar ventana modal/banner obligatorio de tÃ©rminos legales en pantalla.
    * `CS-3`: Mantener inhabilitado el botÃ³n de contribuciÃ³n ("Mapear Tarea") en gris.
    * `CS-4`: Habilitar por completo el botÃ³n de contribuciÃ³n ("Mapear Tarea") en color activo.

#### B.1. Tablas de DecisiÃ³n
Se cruzan las condiciones utilizando la simplificaciÃ³n por equivalencias (guiones) para optimizar la cobertura de pruebas de la interfaz:

| Tipo de Control | Variables de la Interfaz de Usuario | A | B | C | D |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Condiciones de Entrada** | `CE-1`: SesiÃ³n de usuario activa | **F** | **V** | **V** | **V** |
| | `CE-2`: Proyecto exige licencia | **-** | **F** | **V** | **V** |
| | `CE-3`: Usuario acepta tÃ©rminos en pantalla | **-** | **-** | **F** | **V** |
| **Condiciones de Salida** | `CS-1`: Redirigir de forma forzada a Landing/Login | **V** | **F** | **F** | **F** |
| | `CS-2`: Desplegar modal/banner legal | **F** | **F** | **V** | **F** |
| | `CS-3`: BotÃ³n "Mapear Tarea" inhabilitado (Gris) | **F** | **F** | **V** | **F** |
| | `CS-4`: BotÃ³n "Mapear Tarea" habilitado (Activo) | **F** | **V** | **F** | **V** |

---

**C. Casos de Prueba Derivados**

| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada (Reglas Aplicadas) | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CP-1003-01** | 1. Intentar ingresar directamente a la URL de contribuciÃ³n de un proyecto restrictivo sin autenticaciÃ³n previa. | **Estado SesiÃ³n:** No Autenticado.<br>*(Regla de Columna A)* | El sistema bloquea la carga de la interfaz del proyecto, redirige de inmediato al usuario a la Landing Page pÃºblica (`CS-1 = V`) y solicita el login vÃ­a OSM. |
| **CP-1003-02** | 1. Iniciar sesiÃ³n con una cuenta de Mapper (`ACT-02`).<br>2. Navegar e ingresar a un proyecto pÃºblico estÃ¡ndar que **no** tiene ninguna licencia configurada. | **Estado SesiÃ³n:** Activa.<br>**ConfiguraciÃ³n:** Proyecto sin licencia.<br>*(Regla de Columna B)* | La interfaz no despliega alertas visuales, carga la cuadrÃ­cula del mapa de forma limpia y el botÃ³n "Mapear Tarea" se muestra directamente activo y habilitado (`CS-4 = V`). |
| **CP-1003-03** | 1. Iniciar sesiÃ³n con una cuenta de Mapper (`ACT-02`).<br>2. Navegar e ingresar a un proyecto configurado con licencias legales obligatorias.<br>3. Intentar seleccionar un cuadrante o interactuar con el mapa ignorando los textos. | **Estado SesiÃ³n:** Activa.<br>**ConfiguraciÃ³n:** Proyecto con licencia.<br>**AcciÃ³n:** Sin aceptar tÃ©rminos.<br>*(Regla de Columna C)* | La interfaz congela las interacciones desplegando de forma obligatoria la ventana modal de tÃ©rminos legales (`CS-2 = V`). El botÃ³n principal "Mapear Tarea" permanece bloqueado en color gris (`CS-3 = V`). |
| **CP-1003-04** | 1. Estando ante la ventana modal obligatoria de tÃ©rminos legales de un proyecto (Contexto CP-1003-03).<br>2. Hacer clic en el botÃ³n o casilla "Acepto los tÃ©rminos y licencias" de la pantalla. | **Estado SesiÃ³n:** Activa.<br>**ConfiguraciÃ³n:** Proyecto con licencia.<br>**AcciÃ³n:** Clic en Aceptar.<br>*(Regla de Columna D)* | El componente modal legal se oculta automÃ¡ticamente en la interfaz. El botÃ³n principal "Mapear Tarea" cambia de estado visual de gris a su color activo (azul/verde) quedando totalmente habilitado (`CS-4 = V`). |

---

### 3.4. Escenario: ESC-1004 - ModificaciÃ³n de Preferencias y ActualizaciÃ³n de Perfil

**A. DefiniciÃ³n del Escenario**
| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que la interfaz del perfil de usuario permita modificar las preferencias personales (idioma, correo, editor preferido), controlling visualmente los estados del formulario desde la ediciÃ³n hasta el guardado exitoso o el rechazo por datos invÃ¡lidos. |
| **RF Asociados** | RF-1004 |
| **Precondiciones** | El usuario (ACT-02) debe tener una sesiÃ³n activa (`SesionActiva`), haber ingresado a la secciÃ³n "Ajustes de Perfil" y el formulario debe cargarse con sus datos actuales en modo lectura. |
| **TÃ©cnicas aplicadas**| TransiciÃ³n de Estados |
| **Resultado Esperado** | La interfaz grÃ¡fica debe guiar al usuario bloqueando o habilitando el botÃ³n de guardado segÃºn el estado del formulario, mostrando alertas instantÃ¡neas ante errores de formato y confirmando visualmente cuando los cambios se almacenen con Ã©xito. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**
Para este escenario, se modela el comportamiento del sistema mediante los componentes de la tÃ©cnica de **TransiciÃ³n de Estados** extraÃ­dos del diagrama oficial del mÃ³dulo:

* **Estados del Sistema Identificados:**
    * `PerfilConsultado`: Estado inicial donde el formulario se muestra en modo lectura con la informaciÃ³n guardada. El botÃ³n "Guardar Cambios" permanece oculto o inhabilitado.
    * `PerfilEnEdicion`: Estado en el cual el usuario altera al menos un input vÃ¡lido. El botÃ³n de guardado transiciona a un estado activo en la pantalla.
    * `FormularioInvalido`: Estado de alerta visual activado al introducir un dato errÃ³neo (ej. correo sin formato `@`). El botÃ³n de guardado se congela y se renderiza texto rojo de advertencia.
    * `GuardandoCambios`: Estado transitorio de procesamiento donde la interfaz muestra un indicador de carga (Spinner) y congela temporalmente los campos.
* **Transiciones / Eventos Evaluados:**
    * `Usuario modifica campo`
    * `Introduce dato invalido`
    * `Corrige dato en input`
    * `Clic en Guardar Cambios`
    * `Confirmacion exitosa del backend`

![Diagrama de TransiciÃ³n de Estados - ESC-1004](/tests-docs/02-diseno-de-pruebas/funcionales/img/transicion-estado-ESC-1004.png)

---

**C. Casos de Prueba Derivados**

| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada (Clases aplicadas) | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CP-1004-01** | 1. Ingresar a la secciÃ³n "Ajustes de Perfil" (`PerfilConsultado`).<br>2. Cambiar el "Editor por defecto" de ID Editor a JOSM (`Usuario modifica campo`).<br>3. Hacer clic en el botÃ³n activo "Guardar Cambios" (`Clic en Guardar Cambios`).<br>4. Esperar el procesamiento asÃ­ncrono de la pantalla (`GuardandoCambios`). | **Editor seleccionado:** JOSM.<br>**AcciÃ³n:** Enviar cambios de preferencias. | El sistema procesa la actualizaciÃ³n (`Confirmacion exitosa del backend`), la interfaz despliega un mensaje Toast emergente de Ã©xito y el formulario regresa al estado base de `PerfilConsultado`. |
| **CP-1004-02** | 1. Ingresar a la secciÃ³n "Ajustes de Perfil" (`PerfilConsultado`).<br>2. Borrar el correo electrÃ³nico actual y escribir el texto "usuario_mapeo" sin dominio (`Introduce dato invalido`). | **Correo ingresado:** usuario_mapeo<br>*(Sintaxis incorrecta)* | La interfaz cambia al estado `FormularioInvalido`: el botÃ³n "Guardar Cambios" se deshabilita automÃ¡ticamente y aparece un mensaje de error en texto rojo indicando el fallo de formato. |
| **CP-1004-03** | 1. Estando en la pantalla de perfil con el error visual de correo electrÃ³nico activo (`FormularioInvalido`).<br>2. Completar la direcciÃ³n agregando "@gmail.com" al input (`Corrige dato en input`). | **Correo corregido:** usuario_mapeo@gmail.com | La aplicaciÃ³n detecta el cambio en tiempo real, borra la alerta roja de la pantalla y transiciona al estado `PerfilEnEdicion`, reactivando visualmente el botÃ³n "Guardar Cambios". |

