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
  <b>Proyecto:</b> HOT Tasking Manager — DiseÃ±o de Pruebas Funcionales: MOD-02 - ExploraciÃ³n de Proyectos <br>
  <b>Fecha de Elaboración:</b> 12/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# DiseÃ±o de Pruebas Funcionales: MOD-02 - ExploraciÃ³n de Proyectos
**VersiÃ³n del Documento:** 1.0
**Tipo de AnÃ¡lisis:** DiseÃ±o de Pruebas de Sistema (Caja Negra)

---

## 1. Contexto del MÃ³dulo
Este mÃ³dulo es responsable de la persistencia visual, indexaciÃ³n y recuperaciÃ³n de los proyectos de mapeo en la plataforma. Permite a los usuarios buscar proyectos mediante un motor de texto predictivo, segmentar el universo cartogrÃ¡fico aplicando filtros avanzados (segÃºn el estado del proyecto, la dificultad tÃ©cnica del mapper y las campaÃ±as globales asociadas), ordenar los resultados por relevancia o urgencia, y renderizar geogrÃ¡ficamente los lÃ­mites espaciales (Bounding Box - BBOX) sobre un mapa interactivo.

*Para consultar el detalle exhaustivo de los actores, restricciones y reglas de negocio, referirse al [CatÃ¡logo de Requerimientos Funcionales](/tests-docs/02-diseno-de-pruebas/funcionales/00-requerimientos-funcionales.md).*


---

## 2. Estrategia de DiseÃ±o de Pruebas

### 2.1. Enfoque general
Las pruebas se concentrarÃ¡n en garantizar la integridad de la interfaz de usuario (UI) al combinar mÃºltiples criterios de bÃºsqueda y al interactuar con el mapa. La estrategia verificarÃ¡ que la lista de tarjetas de proyectos se actualice de forma sÃ­ncrona/asÃ­ncrona con los controles de filtrado y que el mapa encuadre correctamente el BBOX del proyecto seleccionado sin generar errores de renderizado.

El alcance cubre las interacciones de los siguientes actores:
* **ACT-01 Usuario AnÃ³nimo:** NavegaciÃ³n libre, aplicaciÃ³n de filtros y visualizaciÃ³n del mapa pÃºblico.
* **ACT-02 Mapper:** BÃºsqueda orientada a proyectos que coincidan estrictamente con su nivel de experiencia calculado.

| Actor de Impacto | Rol en este MÃ³dulo | Contexto de Prueba |
| :--- | :--- | :--- |
| **ACT-01** / **ACT-02** | Explorador de Proyectos | Uso del motor de bÃºsqueda, filtros avanzados y ordenamiento. |
| **ACT-01** / **ACT-02** | Visualizador CartogrÃ¡fico | InteracciÃ³n con el mapa y renderizado del Bounding Box (BBOX). |

### 2.2. TÃ©cnicas de Caja Negra Utilizadas
* **Tablas de DecisiÃ³n:** Aplicada al motor de bÃºsqueda con filtros avanzados (RF-2001). Permite validar de forma matemÃ¡tica cÃ³mo responde la pantalla cuando se combinan o contradicen los filtros de Estado, Dificultad y CampaÃ±a.
* **ParticiÃ³n de Equivalencia (PE)** y **AnÃ¡lisis de Valores LÃ­mite (AVL):** Utilizadas para la barra de bÃºsqueda por texto y las coordenadas del mapa (BBOX) (RF-2002). Limita las pruebas de caracteres en la barra de bÃºsqueda y las fronteras geoespaciales numÃ©ricas del mapa.
* **TransiciÃ³n de Estados:** Aplicada a la vista del mapa interactivo (RF-2003). Modela cÃ³mo cambia la interfaz del mapa (Modo Lista, Vista de CuadrÃ­cula, Zoom al BBOX y Carga AsÃ­ncrona de Capas) segÃºn los clics del usuario.

---

## 3. Especificaciones de Escenarios y Casos de Prueba

### 3.1. Escenario: ESC-2001 - Motor de BÃºsqueda y CombinaciÃ³n de Filtros Avanzados

**A. DefiniciÃ³n del Escenario**
| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que la interfaz actualice correctamente la lista de proyectos mostrados al activar, combinar o limpiar los filtros avanzados de Estado (Activo/Archivado), Dificultad (Beginner/Intermediate/Advanced) y CampaÃ±a. |
| **RF Asociados** | RF-2001 |
| **Precondiciones** | El usuario se encuentra en la pantalla principal de exploraciÃ³n ("Explore Projects"). La base de datos contiene proyectos diversificados con diferentes etiquetas. |
| **TÃ©cnicas aplicadas**| Tablas de DecisiÃ³n |
| **Resultado Esperado** | La UI debe renderizar exclusivamente las tarjetas de proyectos que cumplan con la intersecciÃ³n lÃ³gica de todos los filtros seleccionados, mostrando un mensaje claro de "No se encontraron resultados" si la combinaciÃ³n estÃ¡ vacÃ­a. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**
Para este escenario, se modela el comportamiento lÃ³gico de la pantalla utilizando la tÃ©cnica de **Tablas de DecisiÃ³n**, identificando los criterios de filtrado interactivos:

* **Condiciones de Entrada (Controles de la UI):**
    * `CE-1`: Se selecciona un filtro de Estado vÃ¡lido (ej. "Activo").
    * `CE-2`: Se selecciona un filtro de Dificultad acorde al Mapper (ej. "Beginner").
    * `CE-3`: Se selecciona un filtro de CampaÃ±a especÃ­fico (ej. "Response COVID-19").
* **Condiciones de Salida (Resultados en la UI):**
    * `CS-1`: Renderizar lista filtrada con coincidencia exacta (IntersecciÃ³n lÃ³gica).
    * `CS-2`: Desplegar mensaje de alerta "No se encontraron proyectos que coincidan con los filtros".
    * `CS-3`: Mostrar el catÃ¡logo completo de proyectos (Estado por defecto / Sin filtros).

#### B.1. Tablas de DecisiÃ³n
Se cruzan las condiciones de los selectores aplicando guiones (**-**) para representar estados indiferentes y optimizar las pruebas en la interfaz:

| Tipo de Control | Variables de la Interfaz de Usuario | A | B | C | D |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Condiciones de Entrada** | `CE-1`: Filtro de Estado seleccionado | **F** | **V** | **V** | **V** |
| | `CE-2`: Filtro de Dificultad seleccionado | **F** | **F** | **V** | **V** |
| | `CE-3`: Filtro de CampaÃ±a seleccionado | **F** | **-** | **F** | **V** |
| **Condiciones de Salida** | `CS-1`: Renderizar lista filtrada exacta | **F** | **V** | **V** | **V** |
| | `CS-2`: Desplegar mensaje "Sin resultados" | **F** | **F** | **F** | **F** |
| | `CS-3`: Mostrar catÃ¡logo completo (Defecto)| **V** | **F** | **F** | **F** |

*Nota sobre el anÃ¡lisis:* Si la base de datos devuelve vacÃ­o para una combinaciÃ³n (por ejemplo, en la columna D no hay proyectos "Activos + Beginner + COVID-19"), la salida `CS-1` pasarÃ­a a Falso y se activarÃ­a de inmediato `CS-2`.

---

**C. Casos de Prueba Derivados**

| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada (Reglas Aplicadas) | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CP-2001-01** | 1. Ingresar a la secciÃ³n "Explorar Proyectos".<br>2. Verificar el estado inicial de la pantalla sin interactuar con los desplegables. | **Filtros:** Ninguno activo.<br>*(Regla de Columna A)* | La interfaz carga por defecto el catÃ¡logo completo de proyectos disponibles en el sistema (`CS-3 = V`). |
| **CP-2001-02** | 1. Hacer clic en el selector de Estado y marcar "Activo".<br>2. Mantener el resto de filtros vacÃ­os. | **Estado:** Activo.<br>**Dificultad:** Sin filtro.<br>*(Regla de Columna B)* | La pantalla se actualiza asÃ­ncronamente mostrando Ãºnicamente las tarjetas de proyectos cuyo estado sea "Activo" (`CS-1 = V`). |
| **CP-2001-03** | 1. Manteniendo el filtro "Activo", abrir el selector de Dificultad y marcar "Beginner". | **Estado:** Activo.<br>**Dificultad:** Beginner.<br>*(Regla de Columna C)* | La lista reduce sus elementos, mostrando solo los proyectos que son "Activos" y que simultÃ¡neamente aceptan mappers "Beginner" (`CS-1 = V`). |
| **CP-2001-04** | 1. Mantener activos los filtros anteriores.<br>2. Abrir el selector de CampÃ±as y marcar una campaÃ±a existente (ej. "Malaria"). | **Estado:** Activo.<br>**Dificultad:** Beginner.<br>**CampaÃ±a:** Malaria.<br>*(Regla de Columna D)* | La interfaz procesa la intersecciÃ³n final. Muestra en pantalla solo los proyectos que cumplan estrictamente con los tres criterios en simultÃ¡neo (`CS-1 = V`). |

---

### 3.2. Escenario: ESC-2002 - ValidaciÃ³n de Barra de BÃºsqueda por Texto y LÃ­mites del BBOX

**A. DefiniciÃ³n del Escenario**
| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar la precisiÃ³n del motor de bÃºsqueda al ingresar cadenas de caracteres de texto en el input flotante, y la correcta recepciÃ³n de coordenadas numÃ©ricas lÃ­mites del Bounding Box (BBOX) que encuadran geogrÃ¡ficamente un proyecto en el mapa. |
| **RF Asociados** | RF-2002 |
| **Precondiciones** | El usuario se encuentra en la pantalla de exploraciÃ³n. El mapa interactivo base (OpenStreetMap) estÃ¡ completamente cargado y listo para recibir coordenadas perimetrales de renderizado. |
| **TÃ©cnicas aplicadas**| ParticiÃ³n de Equivalencia (PE) y AnÃ¡lisis de Valores LÃ­mite (AVL) |
| **Resultado Esperado** | El input de texto debe filtrar los proyectos en tiempo real aceptando un nÃºmero prudente de caracteres, mientras que el motor cartogrÃ¡fico debe interpretar con exactitud los lÃ­mites decimales del BBOX sin desbordar el renderizado en la pantalla. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**

#### B.1. ParticiÃ³n de Equivalencia (PE)
Se agrupa el universo de datos para la barra de bÃºsqueda (longitud de caracteres del string) y las coordenadas geogrÃ¡ficas de latitud vÃ¡lidas para el encuadre del BBOX:

| Clase VÃ¡lida | Clases No VÃ¡lidas | Rango Evaluado |
| :--- | :--- | :---: |
| **PE-V01** (Texto estÃ¡ndar) | - | De 1 a 50 caracteres |
| - | **PE-NV01** (Texto VacÃ­o) | 0 caracteres |
| - | **PE-NV02** (Texto Excesivo) | mas de 51 caracteres |
| **PE-V02** (Latitud VÃ¡lida BBOX) | - | De -90.00 a +90.00 |
| - | **PE-NV03** (Latitud Fuera de Rango)| < -90.00 o > +90.00 |

#### B.2. AnÃ¡lisis de Valores LÃ­mite (AVL)
Se identifican los valores de prueba crÃ­ticos situados en las fronteras exactas de longitud de caracteres de bÃºsqueda y bordes geogrÃ¡ficos de latitud para el BBOX:

| LÃ­mite Inferior VÃ¡lido | LÃ­mite Inferior No VÃ¡lido | LÃ­mite Superior VÃ¡lido | LÃ­mite Superior No VÃ¡lido | Rango de Clase Asociado |
| :---: | :---: | :---: | :---: | :---: |
| **1** | **0** | **50** | **51** | Longitud del Input de BÃºsqueda |
| **-90.0000** | **-90.0001** | **90.0000** | **90.0001** | Coordenadas de Latitud (BBOX) |

---

**C. Casos de Prueba Derivados**

| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada (Clases aplicadas) | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CP-2002-01** | 1. Hacer clic en el input de bÃºsqueda.<br>2. Presionar la barra espaciadora o dejar el campo vacÃ­o y presionar Enter. | **Texto de bÃºsqueda:** (VacÃ­o)<br>*(LÃ­mite Inferior No VÃ¡lido)* | El sistema ignora la acciÃ³n de filtrado por texto, no realiza peticiones asÃ­ncronas innecesarias y mantiene el catÃ¡logo base intacto. |
| **CP-2002-02** | 1. Digitar un solo carÃ¡cter vÃ¡lido (ej: "P") en la barra de bÃºsqueda de proyectos. | **Texto de bÃºsqueda:** "P"<br>*(LÃ­mite Inferior VÃ¡lido)* | La interfaz responde de inmediato al primer carÃ¡cter, desplegando las tarjetas de proyectos cuyos nombres inicien o contengan la letra "P". |
| **CP-2002-03** | 1. Introducir una cadena de texto que contenga exactamente 50 caracteres alfabÃ©ticos en el input. | **Texto de bÃºsqueda:** String de 50 caracteres.<br>*(LÃ­mite Superior VÃ¡lido)* | La interfaz de usuario procesa el texto completo sin truncar la caja de ediciÃ³n y actualiza la lista con los proyectos coincidentes. |
| **CP-2002-04** | 1. Intentar escribir o pegar una cadena de texto que posea 51 caracteres en la barra de bÃºsqueda. | **Texto de bÃºsqueda:** String de 51 caracteres.<br>*(LÃ­mite Superior No VÃ¡lido)* | La interfaz restringe el exceso de datos mediante un bloqueo de entrada fÃ­sico (`maxlength="50"`) impidiendo que el carÃ¡cter nÃºmero 51 sea renderizado en pantalla. |
| **CP-2002-05** | 1. Seleccionar un proyecto cuyas coordenadas perimetrales del BBOX toquen el extremo del polo sur geogrÃ¡fico. | **Latitud del BBOX:** -90.0000<br>*(LÃ­mite Inferior VÃ¡lido)* | El mapa interactivo se reubica de forma correcta, encuadrando y dibujando el polÃ­gono del proyecto en el lÃ­mite exacto de la visualizaciÃ³n cartogrÃ¡fica. |
| **CP-2002-06** | 1. Simular mediante la URL o la carga de mapa un proyecto con un BBOX corrupto que sobrepase el lÃ­mite norte. | **Latitud del BBOX:** 90.0001<br>*(LÃ­mite Superior No VÃ¡lido)* | La interfaz atrapa la excepciÃ³n de desborde geogrÃ¡fico, el mapa evita romperse (pantalla en blanco) y renderiza una alerta visual de "Error al cargar la delimitaciÃ³n espacial". |

---

### 3.3. Escenario: ESC-2003 - RestricciÃ³n de Visibilidad y Acceso a Proyectos Privados

**A. DefiniciÃ³n del Escenario**
| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el catÃ¡logo de exploraciÃ³n oculte o muestre de forma dinÃ¡mica los proyectos marcados como privados en la interfaz, permitiendo el acceso Ãºnicamente a usuarios logueados que pertenezcan al equipo autorizado o posean rol de Administrador. |
| **RF Asociados** | RF-2003 (Dependiente de RF-1001) |
| **Precondiciones** | El usuario se encuentra en la pantalla de exploraciÃ³n de proyectos (`Explore Projects`). Existen proyectos en la base de datos configurados con visibilidad "Privada". |
| **TÃ©cnicas aplicadas**| TransiciÃ³n de Estados |
| **Resultado Esperado** | La interfaz de usuario debe restringir la visualizaciÃ³n de las tarjetas privadas a usuarios anÃ³nimos (ACT-01), mutando el catÃ¡logo de forma inmediata al iniciar sesiÃ³n si el usuario posee las credenciales autorizadas. |

**B. AplicaciÃ³n de TÃ©cnicas (AnÃ¡lisis)**
Para este escenario, se modela el comportamiento del sistema mediante los componentes de la tÃ©cnica de **TransiciÃ³n de Estados** extraÃ­dos del diagrama oficial del mÃ³dulo:

* **Estados del Sistema Identificados:**
    * `CatalogoPublico`: Estado inicial de la pantalla para cualquier internauta. Solo se renderizan los proyectos con visibilidad abierta.
    * `ValidandoCredenciales`: Estado transitorio de la interfaz tras el inicio de sesiÃ³n (`RF-1001`), donde el sistema verifica los permisos del usuario contra el proyecto privado.
    * `CatalogoRestringido`: Estado de la UI donde se incorporan y muestran de manera exclusiva las tarjetas de los proyectos privados autorizados para el usuario.
    * `AccesoDenegado`: Estado de error visual (alerta en la interfaz o redirecciÃ³n) si un usuario intenta forzar el ingreso a la URL de un proyecto privado sin permisos.
* **Transiciones / Eventos Evaluados:**
    * `Usuario inicia sesion`
    * `Sistema verifica permisos`
    * `Usuario desautorizado fuerza URL`
    * `Cierre de sesion del usuario`
    * `Redireccion automatica UI`

![Diagrama de TransiciÃ³n de Estados - ESC-2003](/tests-docs/02-diseno-de-pruebas/funcionales/img/transicion-estado-ESC-2003.png)

---

**C. Casos de Prueba Derivados**

| ID Caso | Pasos de EjecuciÃ³n | Datos de Entrada (Clases aplicadas) | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CP-2003-01** | 1. Ingresar a la secciÃ³n "Explorar Proyectos" abriendo una pestaÃ±a en modo incÃ³gnito (`CatalogoPublico`).<br>2. Digitar el nombre de un proyecto de carÃ¡cter estrictamente cerrado en la barra de bÃºsqueda. | **Rol de Usuario:** AnÃ³nimo (`ACT-01`).<br>**Texto bÃºsqueda:** "Proyecto Privado Equipo A". | El sistema procesa la bÃºsqueda local sin colgarse y la interfaz muestra de forma limpia el mensaje "0 proyectos encontrados", manteniendo oculta la tarjeta. |
| **CP-2003-02** | 1. Estando en el explorador base, hacer clic en el botÃ³n principal "Log In" de la barra superior (`Usuario inicia sesion`).<br>2. Completar el inicio de sesiÃ³n vÃ­a OAuth (`ValidandoCredenciales`).<br>3. Ingresar al catÃ¡logo usando una cuenta que forme parte activa del equipo del proyecto (`Sistema verifica permisos`). | **Rol de Usuario:** Mapper Autorizado (`ACT-02`).<br>**Credenciales:** Token de sesiÃ³n vÃ¡lido. | La interfaz transiciona al estado `CatalogoRestringido`: la pantalla se refresca asÃ­ncronamente inyectando la tarjeta del proyecto privado con un indicador visual de acceso exclusivo. |
| **CP-2003-03** | 1. Estando en la vista del catÃ¡logo con las tarjetas restringidas visibles (`CatalogoRestringido`).<br>2. Desplegar el menÃº del perfil de usuario y hacer clic en la opciÃ³n "Log Out" (`Cierre de sesion del usuario`). | **AcciÃ³n UI:** Clic en Cerrar SesiÃ³n. | El navegador elimina el token de autenticaciÃ³n del almacenamiento, la interfaz parpadea borrando las tarjetas privadas y regresa de inmediato al estado `CatalogoPublico`. |
| **CP-2003-04** | 1. Copiar de forma externa la ruta directa de mapeo de un proyecto privado (ej: `/projects/10/map`).<br>2. Pegarla directamente en la barra de direcciones de una ventana sin autenticar (`Usuario desautorizado fuerza URL`). | **Ruta forzada:** URL interna protegida. | La aplicaciÃ³n interrumpe la carga normal y cambia al estado `AccesoDenegado`: renderiza en pantalla una alerta roja de error "403 No Autorizado" y tras 3 segundos (`Redireccion automatica UI`) redirige al usuario de vuelta al `CatalogoPublico`. |



