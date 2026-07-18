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
  <b>Proyecto:</b> HOT Tasking Manager — DiseÃ±o de Pruebas Funcionales: MOD-0005 - AdministraciÃ³n de Proyectos <br>
  <b>Fecha de Elaboración:</b> 12/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# DiseÃ±o de Pruebas Funcionales: MOD-0005 - AdministraciÃ³n de Proyectos

**Proyecto:** HOTOSM Tasking Manager  
**VersiÃ³n del Documento:** 1.0  
**Tipo de AnÃ¡lisis:** DiseÃ±o de Pruebas de Sistema (Caja Negra)  
**MÃ³dulo evaluado:** MOD-0005 - AdministraciÃ³n de Proyectos  

---

## 1. Contexto del MÃ³dulo

El mÃ³dulo **MOD-0005: AdministraciÃ³n de Proyectos** permite a un usuario con rol de **Project Manager (ACT-0004)** crear, configurar y administrar proyectos dentro de HOTOSM Tasking Manager.

Este mÃ³dulo cubre el flujo de creaciÃ³n de un proyecto desde la definiciÃ³n del Ãrea de InterÃ©s (AOI), la generaciÃ³n de tareas mediante grilla, la configuraciÃ³n de metadatos, permisos, privacidad, fuentes de imÃ¡genes, publicaciÃ³n, clonaciÃ³n, transferencia de propiedad y eliminaciÃ³n controlada.

Desde el punto de vista de pruebas funcionales, este mÃ³dulo es importante porque concentra operaciones crÃ­ticas del sistema: creaciÃ³n de proyectos, validaciÃ³n de datos obligatorios, cambios de estado, reglas de acceso y acciones administrativas sensibles.

*Para consultar el detalle de actores, mÃ³dulos y requerimientos funcionales, referirse al documento `01-requerimientos-funcionales.md`.*

---

## 2. Estrategia de DiseÃ±o de Pruebas

### 2.1. Enfoque general

El enfoque de pruebas aplicado al mÃ³dulo serÃ¡ de **caja negra**, evaluando Ãºnicamente el comportamiento observable del sistema desde la interfaz web, sin analizar la implementaciÃ³n interna del cÃ³digo.

Las pruebas se diseÃ±an tomando como base los requerimientos funcionales del mÃ³dulo **MOD-0005**. Se validarÃ¡ que el sistema responda correctamente ante entradas vÃ¡lidas, entradas incompletas, cambios de configuraciÃ³n, cambios de estado y acciones administrativas realizadas por un usuario autorizado.

El actor principal del flujo serÃ¡:

| Actor | Rol dentro de las pruebas |
| :--- | :--- |
| **ACT-0004 - Project Manager** | Usuario autorizado para crear, editar, publicar, clonar, transferir y eliminar proyectos. |

De forma complementaria, algunas acciones pueden involucrar restricciones asociadas a usuarios con privilegios suficientes dentro de la organizaciÃ³n o dentro de Tasking Manager.

---

### 2.2. TÃ©cnicas de Caja Negra Utilizadas

Para diseÃ±ar los casos de prueba funcionales se aplican las siguientes tÃ©cnicas de caja negra:

#### ParticiÃ³n de Equivalencia

Se utiliza para dividir las entradas en clases vÃ¡lidas e invÃ¡lidas. Esta tÃ©cnica permite seleccionar datos representativos para comprobar si el sistema acepta o rechaza correctamente una operaciÃ³n.

Aplicaciones dentro del mÃ³dulo:

- Archivo geogrÃ¡fico vÃ¡lido para definir el AOI.
- Campos obligatorios completos o incompletos.
- Fuente de imÃ¡genes vÃ¡lida.
- Usuario vÃ¡lido para transferencia de propiedad.

#### Tabla de DecisiÃ³n

Se utiliza cuando el resultado depende de la combinaciÃ³n de varias condiciones. En este mÃ³dulo se aplica principalmente a reglas de permisos, privacidad y transferencia de propiedad.

Aplicaciones dentro del mÃ³dulo:

- Nivel mÃ­nimo requerido para mapear o validar.
- Proyecto pÃºblico o privado.
- Usuario perteneciente o no a un equipo autorizado.
- Usuario con permisos suficientes para recibir la propiedad de un proyecto.

#### TransiciÃ³n de Estados

Se utiliza para validar que el sistema permita cambios correctos entre estados funcionales del proyecto.

Aplicaciones dentro del mÃ³dulo:

- Proyecto en estado **Borrador** que pasa a **Publicado**.
- Proyecto existente que pasa a estado eliminado.
- Proyecto pÃºblico que pasa a configuraciÃ³n privada.

#### AnÃ¡lisis de Valores LÃ­mite

Esta tÃ©cnica es aplicable a reglas con lÃ­mites numÃ©ricos, como tamaÃ±o mÃ¡ximo del AOI, tamaÃ±o de tareas o longitudes mÃ¡ximas/mÃ­nimas de campos. En este diseÃ±o se considera como tÃ©cnica aplicable al mÃ³dulo, aunque los casos ejecutados se enfocan principalmente en particiÃ³n de equivalencia, tabla de decisiÃ³n y transiciÃ³n de estados.

---

## 3. Especificaciones de Escenarios de Prueba

Para organizar el diseÃ±o del mÃ³dulo **MOD-0005**, los casos funcionales se agrupan en cinco escenarios principales. Cada escenario reÃºne requerimientos relacionados y aplica una o mÃ¡s tÃ©cnicas de caja negra.

| ID Escenario | DescripciÃ³n breve | RF cubiertos | Alcance funcional | TÃ©cnica principal |
| :--- | :--- | :--- | :--- | :--- |
| **ESC-5001** | CreaciÃ³n inicial del proyecto | RF-5001, RF-5002 | DefiniciÃ³n de AOI, generaciÃ³n de grilla, recorte de tareas y creaciÃ³n inicial del proyecto. | ParticiÃ³n de Equivalencia / Flujo funcional |
| **ESC-5002** | ValidaciÃ³n y guardado de metadatos | RF-5006 | ValidaciÃ³n de campos obligatorios y guardado de informaciÃ³n requerida del proyecto. | ParticiÃ³n de Equivalencia |
| **ESC-5003** | PublicaciÃ³n y estado del proyecto | RF-5007 | Cambio de estado del proyecto desde Borrador hacia Publicado. | TransiciÃ³n de Estados |
| **ESC-5004** | Permisos, privacidad y propiedad | RF-5003, RF-5005 | ConfiguraciÃ³n de permisos, privacidad y transferencia de propiedad. | Tabla de DecisiÃ³n |
| **ESC-5005** | Acciones administrativas y configuraciÃ³n complementaria | RF-5004, RF-5009, RF-5010 | ClonaciÃ³n, eliminaciÃ³n controlada y configuraciÃ³n de fuente de imÃ¡genes. | Flujo funcional / ParticiÃ³n de Equivalencia |

---

## 4. Escenarios Detallados y Casos Derivados

## 4.1. Escenario: [ESC-5001] - CreaciÃ³n inicial del proyecto

### A. DefiniciÃ³n del Escenario

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el sistema permita iniciar la creaciÃ³n de un proyecto mediante la definiciÃ³n de un Ãrea de InterÃ©s, la generaciÃ³n de una grilla de tareas y la creaciÃ³n inicial del proyecto. |
| **RF asociados** | RF-5001, RF-5002 |
| **Actor principal** | ACT-0004 - Project Manager |
| **Precondiciones** | El usuario se encuentra autenticado y posee permisos para crear proyectos. |
| **TÃ©cnicas aplicadas** | ParticiÃ³n de Equivalencia y flujo funcional. |
| **Resultado esperado** | El sistema acepta un AOI vÃ¡lido, genera la grilla, permite recortarla y crea el proyecto inicial correctamente. |

### B. AplicaciÃ³n de TÃ©cnicas

#### B.1. ParticiÃ³n de Equivalencia para entrada geogrÃ¡fica del AOI

| Clase invÃ¡lida | Clase vÃ¡lida | Clase invÃ¡lida |
| :--- | :--- | :--- |
| Archivo vacÃ­o, corrupto o con formato no soportado. | Archivo GeoJSON vÃ¡lido con geometrÃ­a reconocida por el sistema. | Archivo geogrÃ¡fico con geometrÃ­a invÃ¡lida o fuera de restricciones. |
| **Comportamiento esperado:** el sistema debe rechazar la entrada. | **Comportamiento esperado:** el sistema debe aceptar el AOI y representarlo en el mapa. | **Comportamiento esperado:** el sistema debe rechazar la entrada o mostrar validaciÃ³n. |

#### B.2. Flujo funcional de creaciÃ³n

El flujo funcional esperado es:

1. Definir Ãrea de InterÃ©s.
2. Generar grilla de tareas.
3. Recortar la cuadrÃ­cula si corresponde.
4. Revisar datos mÃ­nimos.
5. Crear proyecto.

### C. Casos de Prueba Derivados

| ID Caso         | Pasos de ejecuciÃ³n resumidos                                                    | Datos de entrada / contexto                                                                 | Resultado esperado                                                                                                              |
| :-------------- | :------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------ |
| **CP-MOD5-001** | Cargar un archivo GeoJSON vÃ¡lido en el Paso 1.                                  | GeoJSON vÃ¡lido con polÃ­gono de prueba.                                                      | El sistema acepta el AOI y permite avanzar al Paso 2.                                                                           |
| **CP-MOD5-002** | Continuar con la generaciÃ³n de la grilla.                                       | AOI previamente aceptado.                                                                   | El sistema genera la grilla dentro del AOI y permite avanzar.                                                                   |
| **CP-MOD5-003** | Recortar la cuadrÃ­cula de tareas.                                               | Grilla generada previamente.                                                                | El sistema procesa el recorte y permite avanzar al Paso 4.                                                                      |
| **CP-MOD5-004** | Completar datos mÃ­nimos y crear el proyecto.                                    | Nombre y organizaciÃ³n vÃ¡lidos.                                                              | El sistema crea el proyecto y redirige a la pantalla de ediciÃ³n.                                                                |
| **CP-MOD5-005** | Cargar un GeoJSON invÃ¡lido en el Paso 1 de creaciÃ³n del proyecto.               | GeoJSON con estructura incompleta, geometrÃ­a invÃ¡lida o coordenadas vacÃ­as.                 | El sistema rechaza el AOI invÃ¡lido, no permite avanzar al Paso 2 y muestra una validaciÃ³n o comportamiento de error controlado. |
| **CP-MOD5-006** | Intentar cargar un archivo GeoJSON vacÃ­o en el Paso 1 de creaciÃ³n del proyecto. | Archivo `.geojson` sin contenido o con contenido vacÃ­o.                                     | El sistema rechaza el archivo vacÃ­o, no permite definir el AOI y evita avanzar al Paso 2 del flujo de creaciÃ³n.                 |
| **CP-MOD5-007** | Cargar un AOI que excede las restricciones permitidas por el sistema.           | GeoJSON vÃ¡lido en formato, pero con Ã¡rea demasiado grande o fuera de los lÃ­mites aceptados. | El sistema rechaza el AOI o muestra una advertencia indicando que el Ã¡rea no cumple las restricciones permitidas.               |



---

## 4.2. Escenario: [ESC-5002] - ValidaciÃ³n y guardado de metadatos del proyecto

### A. DefiniciÃ³n del Escenario

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el sistema controle correctamente los campos obligatorios del proyecto y permita guardar solo cuando la informaciÃ³n requerida se encuentra completa. |
| **RF asociados** | RF-5006 |
| **Actor principal** | ACT-0004 - Project Manager |
| **Precondiciones** | Existe un proyecto creado y el usuario se encuentra en la pantalla de ediciÃ³n. |
| **TÃ©cnicas aplicadas** | ParticiÃ³n de Equivalencia. |
| **Resultado esperado** | El sistema rechaza configuraciones incompletas y acepta configuraciones completas. |

### B. AplicaciÃ³n de TÃ©cnicas

#### B.1. ParticiÃ³n de Equivalencia para campos obligatorios

| Clase invÃ¡lida | Clase vÃ¡lida |
| :--- | :--- |
| Proyecto con descripciÃ³n, instrucciones o tipo de mapeo incompletos. | Proyecto con descripciÃ³n, instrucciones y metadatos obligatorios completos. |
| **Comportamiento esperado:** el sistema debe impedir guardar y mostrar mensajes de validaciÃ³n. | **Comportamiento esperado:** el sistema debe guardar correctamente y mostrar confirmaciÃ³n. |

### C. Casos de Prueba Derivados

| ID Caso         | Pasos de ejecuciÃ³n resumidos                                                                            | Datos de entrada / contexto                                                                               | Resultado esperado                                                                                                                           |
| :-------------- | :------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
| **CP-MOD5-008** | Intentar guardar el proyecto sin completar campos obligatorios.                                         | DescripciÃ³n, instrucciones o tipo de mapeo incompletos.                                                   | El sistema bloquea el guardado y muestra mensaje de validaciÃ³n.                                                                              |
| **CP-MOD5-009** | Completar los campos obligatorios y guardar.                                                            | DescripciÃ³n, instrucciones y metadatos completos.                                                         | El sistema guarda correctamente y muestra confirmaciÃ³n.                                                                                      |
| **CP-MOD5-010** | Modificar el nombre del proyecto desde la pantalla de ediciÃ³n y guardar los cambios.                    | Proyecto existente con un nuevo nombre vÃ¡lido ingresado por el Project Manager.                           | El sistema guarda el nuevo nombre del proyecto y lo muestra correctamente despuÃ©s de actualizar la informaciÃ³n.                              |
| **CP-MOD5-011** | Modificar la descripciÃ³n corta del proyecto desde la pantalla de ediciÃ³n y guardar los cambios.         | Proyecto existente con una nueva descripciÃ³n corta vÃ¡lida ingresada por el Project Manager.               | El sistema guarda la nueva descripciÃ³n corta y la mantiene visible despuÃ©s de actualizar la informaciÃ³n del proyecto.                        |
| **CP-MOD5-012** | Modificar las instrucciones detalladas del proyecto desde la pantalla de ediciÃ³n y guardar los cambios. | Proyecto existente con nuevas instrucciones detalladas vÃ¡lidas para los mapeadores.                       | El sistema guarda las instrucciones detalladas y las mantiene disponibles en la secciÃ³n correspondiente del proyecto.                        |
| **CP-MOD5-013** | Guardar la configuraciÃ³n del proyecto sin realizar cambios visibles en los campos editables.            | Proyecto existente con configuraciÃ³n previamente guardada y sin modificaciones realizadas por el usuario. | El sistema procesa la acciÃ³n sin errores, mantiene la informaciÃ³n existente y muestra una confirmaciÃ³n o comportamiento estable de guardado. |



---

## 4.3. Escenario: [ESC-5003] - PublicaciÃ³n y estado del proyecto

### A. DefiniciÃ³n del Escenario

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el sistema permita cambiar el estado de un proyecto desde Borrador hacia Publicado cuando la configuraciÃ³n obligatoria estÃ¡ completa. |
| **RF asociados** | RF-5007 |
| **Actor principal** | ACT-0004 - Project Manager |
| **Precondiciones** | El proyecto existe, tiene informaciÃ³n obligatoria completa y se encuentra inicialmente en estado Borrador. |
| **TÃ©cnicas aplicadas** | TransiciÃ³n de Estados. |
| **Resultado esperado** | El sistema permite la transiciÃ³n de estado y conserva el nuevo estado despuÃ©s de guardar. |

### B. AplicaciÃ³n de TÃ©cnicas

#### B.1. TransiciÃ³n de Estados

| Estado inicial | AcciÃ³n | Estado final esperado |
| :--- | :--- | :--- |
| Borrador | Seleccionar estado Publicado y guardar. | Publicado |

La transiciÃ³n evaluada es vÃ¡lida porque el proyecto cuenta con los datos obligatorios necesarios para ser publicado.

### C. Casos de Prueba Derivados

| ID Caso         | Pasos de ejecuciÃ³n resumidos                                                                                | Datos de entrada / contexto                                                                      | Resultado esperado                                                                                                                 |
| :-------------- | :---------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| **CP-MOD5-014** | Cambiar el estado del proyecto de Borrador a Publicado y guardar.                                           | Proyecto con configuraciÃ³n completa.                                                             | El sistema actualiza el estado a Publicado y muestra confirmaciÃ³n.                                                                 |
| **CP-MOD5-015** | Intentar cambiar el estado del proyecto a Publicado sin completar todos los campos obligatorios requeridos. | Proyecto en estado Borrador con descripciÃ³n, instrucciones o metadatos obligatorios incompletos. | El sistema impide la publicaciÃ³n del proyecto y muestra mensajes de validaciÃ³n indicando la informaciÃ³n faltante.                  |
| **CP-MOD5-016** | Cambiar el estado de un proyecto publicado a Borrador y guardar los cambios.                                | Proyecto previamente publicado con configuraciÃ³n completa.                                       | El sistema permite cambiar el estado a Borrador, guarda el cambio y mantiene el nuevo estado despuÃ©s de actualizar la informaciÃ³n. |



---

## 4.4. Escenario: [ESC-5004] - Permisos, privacidad y transferencia de propiedad

### A. DefiniciÃ³n del Escenario

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar que el sistema permita configurar reglas de acceso al proyecto y ejecutar acciones de propiedad solo bajo condiciones vÃ¡lidas. |
| **RF asociados** | RF-5003, RF-5005 |
| **Actor principal** | ACT-0004 - Project Manager |
| **Precondiciones** | Existe un proyecto editable y el usuario posee permisos de administraciÃ³n. |
| **TÃ©cnicas aplicadas** | Tabla de DecisiÃ³n y ParticiÃ³n de Equivalencia. |
| **Resultado esperado** | El sistema guarda correctamente permisos, privacidad y transferencia cuando se cumplen las condiciones requeridas. |

### B. AplicaciÃ³n de TÃ©cnicas

#### B.1. Tabla de DecisiÃ³n para permisos y privacidad

| Condiciones / Acciones | Regla 1 | Regla 2 | Regla 3 | Regla 4 |
| :--- | :---: | :---: | :---: | :---: |
| **Condiciones** | | | | |
| Â¿Proyecto privado? | No | No | SÃ­ | SÃ­ |
| Â¿Usuario pertenece a equipo autorizado? | N/A | N/A | SÃ­ | No |
| Â¿Usuario cumple nivel mÃ­nimo requerido? | SÃ­ | No | SÃ­ | SÃ­ |
| **Acciones** | | | | |
| Permitir mapear / validar | X | | X | |
| Restringir por nivel insuficiente | | X | | |
| Restringir por no pertenecer al equipo | | | | X |

#### B.2. ParticiÃ³n de Equivalencia para transferencia de propiedad

| Clase invÃ¡lida | Clase vÃ¡lida |
| :--- | :--- |
| Usuario inexistente o sin permisos suficientes. | Usuario administrador o Project Manager vÃ¡lido dentro de la organizaciÃ³n. |
| **Comportamiento esperado:** el sistema no debe permitir la transferencia. | **Comportamiento esperado:** el sistema debe permitir transferir la propiedad. |

### C. Casos de Prueba Derivados

| ID Caso         | Pasos de ejecuciÃ³n resumidos                                                              | Datos de entrada / contexto                                                               | Resultado esperado                                                                                                |
| :-------------- | :---------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| **CP-MOD5-017** | Cambiar niveles mÃ­nimos de mapeo y validaciÃ³n.                                            | Nivel mÃ­nimo configurado como INTERMEDIATE.                                               | El sistema guarda los permisos correctamente.                                                                     |
| **CP-MOD5-018** | Activar la opciÃ³n de proyecto privado y guardar.                                          | Proyecto existente con configuraciÃ³n editable.                                            | El sistema guarda la privacidad del proyecto.                                                                     |
| **CP-MOD5-019** | Seleccionar un nuevo propietario vÃ¡lido y transferir propiedad.                           | Usuario administrador de Tasking Manager perteneciente a la organizaciÃ³n.                 | El sistema transfiere correctamente la propiedad del proyecto.                                                    |
| **CP-MOD5-020** | Configurar la dificultad del proyecto desde la pantalla de ediciÃ³n y guardar los cambios. | Proyecto existente con un nivel de dificultad vÃ¡lido seleccionado por el Project Manager. | El sistema guarda la dificultad del proyecto y la muestra correctamente en la configuraciÃ³n del proyecto.         |
| **CP-MOD5-021** | Configurar la prioridad del proyecto desde la pantalla de ediciÃ³n y guardar los cambios.  | Proyecto existente con una prioridad vÃ¡lida seleccionada por el Project Manager.          | El sistema guarda la prioridad asignada al proyecto y la mantiene visible despuÃ©s de actualizar la configuraciÃ³n. |



---

## 4.5. Escenario: [ESC-5005] - Acciones administrativas y configuraciÃ³n complementaria

### A. DefiniciÃ³n del Escenario

| Atributo | Detalle |
| :--- | :--- |
| **DescripciÃ³n** | Validar acciones administrativas adicionales del proyecto, como clonaciÃ³n, eliminaciÃ³n controlada y configuraciÃ³n de fuente de imÃ¡genes. |
| **RF asociados** | RF-5004, RF-5009, RF-5010 |
| **Actor principal** | ACT-0004 - Project Manager |
| **Precondiciones** | Existe un proyecto administrable y el usuario posee permisos suficientes. |
| **TÃ©cnicas aplicadas** | Flujo funcional, transiciÃ³n de estados y particiÃ³n de equivalencia. |
| **Resultado esperado** | El sistema permite completar correctamente acciones administrativas vÃ¡lidas y conserva los resultados esperados. |

### B. AplicaciÃ³n de TÃ©cnicas

#### B.1. Flujo funcional para clonaciÃ³n

El flujo de clonaciÃ³n esperado es:

1. Ingresar a acciones del proyecto.
2. Seleccionar clonar proyecto.
3. Confirmar o continuar el flujo de creaciÃ³n del clon.
4. Crear el nuevo proyecto.
5. Verificar que el proyecto clonado aparezca como una entidad independiente.

#### B.2. TransiciÃ³n funcional para eliminaciÃ³n

| Estado inicial | AcciÃ³n | Estado final esperado |
| :--- | :--- | :--- |
| Proyecto existente | Confirmar eliminaciÃ³n | Proyecto eliminado y redirecciÃ³n a gestiÃ³n de proyectos |

#### B.3. ParticiÃ³n de Equivalencia para fuente de imÃ¡genes

| Clase invÃ¡lida | Clase vÃ¡lida |
| :--- | :--- |
| Fuente vacÃ­a, no soportada o configuraciÃ³n invÃ¡lida. | Fuente disponible en el sistema, como Bing o ESRI World Imagery. |
| **Comportamiento esperado:** el sistema debe rechazar o advertir. | **Comportamiento esperado:** el sistema debe guardar correctamente la fuente seleccionada. |

### C. Casos de Prueba Derivados

| ID Caso         | Pasos de ejecuciÃ³n resumidos                                                                  | Datos de entrada / contexto                                                      | Resultado esperado                                                                                                     |
| :-------------- | :-------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| **CP-MOD5-022** | Seleccionar clonar proyecto y completar el flujo del nuevo proyecto.                          | Proyecto original existente.                                                     | El sistema crea un proyecto clonado independiente.                                                                     |
| **CP-MOD5-023** | Eliminar un proyecto desde la secciÃ³n de acciones.                                            | Proyecto clonado o administrable.                                                | El sistema elimina el proyecto y redirige a gestiÃ³n de proyectos.                                                      |
| **CP-MOD5-024** | Seleccionar una fuente de imÃ¡genes vÃ¡lida y guardar.                                          | Fuente Bing seleccionada.                                                        | El sistema guarda correctamente la fuente de imÃ¡genes.                                                                 |
| **CP-MOD5-025** | Iniciar la acciÃ³n de eliminaciÃ³n de un proyecto y cancelar la operaciÃ³n antes de confirmarla. | Proyecto existente con opciÃ³n de eliminaciÃ³n disponible para el Project Manager. | El sistema cancela la operaciÃ³n, no elimina el proyecto y mantiene la informaciÃ³n del proyecto disponible sin cambios. |



---



