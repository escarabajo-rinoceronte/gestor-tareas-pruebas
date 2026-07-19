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
  <b>Proyecto:</b> HOT Tasking Manager — Documento de Pruebas <br>
  <b>Fecha de Elaboración:</b> 23/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

### MOD-0005: AdministraciÃ³n de Proyectos

## Resumen de EjecuciÃ³n (MÃ©tricas)

| MÃ©trica | Valor |
|---|---|
| **Casos preexistentes** | 0 |
| **Nuevos casos creados** | 25 |
| **Total de casos diseÃ±ados** | 25 |
| **Casos ejecutados con evidencia** | 25 (100%) |
| **Casos exitosos (PASS)** | 25 (100%) |
| **Casos fallidos (FAIL)** | 0 (0%) |
| **Defectos reportados** | 0 |

---

### 5.1.1. CreaciÃ³n de Ãrea de InterÃ©s mediante GeoJSON vÃ¡lido

**CP-MOD5-001**

| ID              | DescripciÃ³n                                                                                                                      | Tipo   | Estado  | Defectos                    |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-001** | Verificar que el sistema permita definir el Ãrea de InterÃ©s de un nuevo proyecto mediante la carga de un archivo GeoJSON vÃ¡lido. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                              | Resultado obtenido                                                                                                                                                                                  |
| :---------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe aceptar el archivo GeoJSON vÃ¡lido, representar el AOI en el mapa y permitir avanzar al siguiente paso de creaciÃ³n del proyecto. | El sistema aceptÃ³ el AOI cargado y permitiÃ³ avanzar al **Paso 2: Establecer tamaÃ±os de tareas**, mostrando el Ã¡rea definida sobre el mapa e indicando la cantidad de tareas generadas inicialmente. |

#### Evidencia CP-MOD5-001 â€” Pantalla inicial de definiciÃ³n de AOI

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-001-01-paso1-definir-aoi.png" alt="CP-MOD5-001 - Paso 1 Definir AOI" width="650">
</p>
Se observa la pantalla inicial del flujo de creaciÃ³n de proyecto, donde el sistema permite definir el Ãrea de InterÃ©s mediante dibujo manual o carga de archivo geogrÃ¡fico.

#### Evidencia CP-MOD5-001 â€” AOI aceptado y avance al Paso 2

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-001-02-aoi-aceptado-paso2.png" alt="CP-MOD5-001 - AOI aceptado y avance al Paso 2" width="650">
</p>
Se observa que el sistema aceptÃ³ correctamente el AOI definido y permitiÃ³ avanzar al **Paso 2: Establecer tamaÃ±os de tareas**. Esto evidencia que la entrada vÃ¡lida fue procesada correctamente desde la interfaz del usuario.

### 5.1.2. GeneraciÃ³n de grilla de tareas dentro del AOI

**CP-MOD5-002**

| ID              | DescripciÃ³n                                                                                                                                                         | Tipo   | Estado  | Defectos                    |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----- | :------ | :-------------------------- |
| **CP-MOD5-002** | Verificar que el sistema genere una cuadrÃ­cula de tareas dentro del Ãrea de InterÃ©s definida previamente y permita continuar con el flujo de creaciÃ³n del proyecto. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                                                   | Resultado obtenido                                                                                                                              |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe generar una grilla o cuadrÃ­cula de tareas dentro del AOI definido, mostrar visualmente las tareas generadas y permitir avanzar al siguiente paso del flujo de creaciÃ³n del proyecto. | El sistema generÃ³ la cuadrÃ­cula de tareas sobre el AOI previamente definido y permitiÃ³ avanzar al **Paso 3: Recortar la cuadrÃ­cula de tareas**. |

#### Evidencia CP-MOD5-002 â€” Grilla inicial generada

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-002-01-grilla-inicial.png" alt="CP-MOD5-002 - Grilla inicial generada" width="650">
</p>

Se observa que, despuÃ©s de definir el Ãrea de InterÃ©s, el sistema generÃ³ una cuadrÃ­cula inicial de tareas dentro del AOI. AdemÃ¡s, la interfaz muestra la cantidad de tareas que serÃ¡n creadas y permite ajustar el tamaÃ±o general de cada tarea.

#### Evidencia CP-MOD5-002 â€” Avance al paso de recorte de cuadrÃ­cula

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-002-03-avance-siguiente-paso.png" alt="CP-MOD5-002 - Avance al paso de recorte de cuadrÃ­cula" width="650">
</p>

Se evidencia que el sistema permitiÃ³ continuar hacia el **Paso 3: Recortar la cuadrÃ­cula de tareas**, confirmando que la generaciÃ³n inicial de la grilla fue procesada correctamente desde la interfaz del usuario.

### 5.1.3. Recorte de cuadrÃ­cula de tareas dentro del AOI

**CP-MOD5-003**

| ID              | DescripciÃ³n                                                                                                                                    | Tipo   | Estado  | Defectos                    |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-003** | Verificar que el sistema permita recortar la cuadrÃ­cula de tareas generada previamente y continuar con el flujo de creaciÃ³n del proyecto. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                       | Resultado obtenido                                                                                                                                                  |
| :------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| El sistema debe permitir recortar la cuadrÃ­cula de tareas al Ãrea de InterÃ©s definida, conservar las tareas vÃ¡lidas dentro del AOI y permitir avanzar al paso de revisiÃ³n del proyecto. | El sistema procesÃ³ correctamente el recorte de la cuadrÃ­cula y permitiÃ³ avanzar al **Paso 4: Revisar**, indicando que el proyecto se crearÃ¡ con **4 tareas**. |

#### Evidencia CP-MOD5-003 â€” Pantalla inicial de recorte de cuadrÃ­cula

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-003-01-paso3-recorte-inicial.png" alt="CP-MOD5-003 - Pantalla inicial de recorte de cuadrÃ­cula" width="650">
</p>

Se observa la pantalla correspondiente al **Paso 3: Recortar la cuadrÃ­cula de tareas**, donde el sistema permite conservar las tareas actuales o recortar la cuadrÃ­cula para ajustarla al Ãrea de InterÃ©s definida.

#### Evidencia CP-MOD5-003 â€” Avance al paso de revisiÃ³n del proyecto

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-003-04-avance-paso4-revisar.png" alt="CP-MOD5-003 - Avance al Paso 4 Revisar" width="300">
</p>

Se evidencia que el sistema procesÃ³ correctamente el recorte de la cuadrÃ­cula y permitiÃ³ avanzar al **Paso 4: Revisar**, mostrando que el proyecto serÃ¡ creado con 4 tareas.

### 5.1.4. CreaciÃ³n del proyecto con datos mÃ­nimos vÃ¡lidos

**CP-MOD5-004**

| ID              | DescripciÃ³n                                                                                                                  | Tipo   | Estado  | Defectos                    |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-004** | Verificar que el sistema permita crear un nuevo proyecto despuÃ©s de completar los datos mÃ­nimos requeridos en el paso de revisiÃ³n. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                     | Resultado obtenido                                                                                                                                                         |
| :----------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir crear el proyecto cuando el AOI, la grilla, el nombre del proyecto y la organizaciÃ³n son vÃ¡lidos. Luego debe mostrar una confirmaciÃ³n o redirigir a la pantalla de administraciÃ³n del proyecto creado. | El sistema creÃ³ correctamente el proyecto y redirigiÃ³ a la pantalla **Editar Proyecto**, donde se visualiza el nombre registrado: **Proyecto Arequipa**. |

#### Evidencia CP-MOD5-004 â€” Datos mÃ­nimos completados

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-004-02-datos-minimos-completos.png" alt="CP-MOD5-004 - Datos mÃ­nimos completados" width="300">
</p>

Se observa que el usuario completÃ³ los datos requeridos para continuar con la creaciÃ³n del proyecto.

#### Evidencia CP-MOD5-004 â€” Proyecto creado correctamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-004-03-proyecto-creado-editar.png" alt="CP-MOD5-004 - Proyecto creado correctamente" width="650">
</p>

Se evidencia que el sistema creÃ³ correctamente el proyecto y redirigiÃ³ a la pantalla de ediciÃ³n, donde se muestra el proyecto reciÃ©n creado con el nombre **Proyecto Arequipa**.

### 5.1.5. ValidaciÃ³n de GeoJSON invÃ¡lido en la creaciÃ³n de AOI

**CP-MOD5-005**

| ID              | DescripciÃ³n                                                                                                          | Tipo   | Estado  | Defectos                    |
| :-------------- | :------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-005** | Verificar que el sistema rechace un archivo GeoJSON invÃ¡lido durante la definiciÃ³n del Ãrea de InterÃ©s del proyecto. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                  | Resultado obtenido                                                                                                                                         |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe rechazar el GeoJSON invÃ¡lido, impedir su carga como AOI vÃ¡lido y evitar que el usuario avance al siguiente paso del flujo de creaciÃ³n del proyecto. | El sistema no permitiÃ³ cargar el GeoJSON invÃ¡lido y mostrÃ³ un error de validaciÃ³n, evitando que la geometrÃ­a incorrecta sea aceptada como Ãrea de InterÃ©s. |

#### Evidencia CP-MOD5-005 â€” GeoJSON invÃ¡lido utilizado

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-005-01-geojson-invalido-codigo.png" alt="CP-MOD5-005 - GeoJSON invÃ¡lido utilizado" width="350">
</p>

Se observa el contenido del archivo GeoJSON utilizado como dato de prueba. El archivo presenta una geometrÃ­a invÃ¡lida, por lo que no cumple con las condiciones necesarias para ser aceptado como Ãrea de InterÃ©s del proyecto.

#### Evidencia CP-MOD5-005 â€” Error al cargar GeoJSON invÃ¡lido

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-005-02-error-geojson-invalido.png" alt="CP-MOD5-005 - Error al cargar GeoJSON invÃ¡lido" width="550">
</p>

Se evidencia que el sistema rechaza el archivo GeoJSON invÃ¡lido y muestra un error de validaciÃ³n, impidiendo que el usuario continÃºe con una geometrÃ­a incorrecta.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la ejecuciÃ³n se comprobÃ³ que el sistema valida la entrada geogrÃ¡fica antes de aceptarla como Ãrea de InterÃ©s. Al detectar que el GeoJSON no cumple con el formato o estructura esperada, bloquea la carga del archivo y evita avanzar en el flujo de creaciÃ³n del proyecto.

### 5.1.6. ValidaciÃ³n de archivo GeoJSON vacÃ­o

**CP-MOD5-006**

| ID              | DescripciÃ³n                                                                                                       | Tipo   | Estado  | Defectos                    |
| :-------------- | :---------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-006** | Verificar que el sistema rechace un archivo GeoJSON vacÃ­o durante la definiciÃ³n del Ãrea de InterÃ©s del proyecto. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                          | Resultado obtenido                                                                                                                             |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe rechazar el archivo GeoJSON vacÃ­o, impedir su carga como AOI vÃ¡lido y evitar que el usuario avance al siguiente paso del flujo de creaciÃ³n. | El sistema no aceptÃ³ el archivo GeoJSON vacÃ­o y mostrÃ³ un error de validaciÃ³n, evitando que se defina un Ãrea de InterÃ©s sin geometrÃ­a vÃ¡lida. |

#### Evidencia CP-MOD5-006 â€” Archivo GeoJSON vacÃ­o utilizado

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-006-01-archivo-geojson-vacio.png" alt="CP-MOD5-006 - Archivo GeoJSON vacÃ­o utilizado" width="650">
</p>

Se observa el archivo GeoJSON utilizado como dato de prueba, el cual no contiene informaciÃ³n geogrÃ¡fica ni geometrÃ­a vÃ¡lida para definir el Ãrea de InterÃ©s.

#### Evidencia CP-MOD5-006 â€” Error al cargar archivo GeoJSON vacÃ­o

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-006-02-error-archivo-geojson-vacio.png" alt="CP-MOD5-006 - Error al cargar archivo GeoJSON vacÃ­o" width="400">
</p>

Se evidencia que el sistema rechaza el archivo GeoJSON vacÃ­o y muestra un error de validaciÃ³n, impidiendo continuar con el flujo de creaciÃ³n del proyecto.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la ejecuciÃ³n se comprobÃ³ que el sistema valida el contenido del archivo antes de aceptarlo como Ãrea de InterÃ©s. Al detectar que el archivo se encuentra vacÃ­o y no contiene geometrÃ­a vÃ¡lida, bloquea la carga y evita avanzar al siguiente paso.

### 5.1.7. ValidaciÃ³n de AOI fuera del Ã¡rea permitida

**CP-MOD5-007**

| ID              | DescripciÃ³n                                                                                                                             | Tipo   | Estado  | Defectos                    |
| :-------------- | :-------------------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-007** | Verificar que el sistema rechace o bloquee un Ãrea de InterÃ©s que excede las restricciones permitidas durante la creaciÃ³n del proyecto. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                            | Resultado obtenido                                                                                                                                                                    |
| :-------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| El sistema debe rechazar el AOI o impedir el avance cuando el Ã¡rea cargada excede las restricciones permitidas para la creaciÃ³n del proyecto. | El sistema cargÃ³ la validaciÃ³n correspondiente y no permitiÃ³ avanzar con el AOI ingresado, evitando continuar el flujo de creaciÃ³n con un Ã¡rea fuera de las restricciones permitidas. |

#### Evidencia CP-MOD5-007 â€” GeoJSON con AOI fuera del Ã¡rea permitida

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-007-01-aoi-grande-geojson.png" alt="CP-MOD5-007 - GeoJSON con AOI fuera del Ã¡rea permitida" width="250">
</p>

Se observa el contenido del archivo GeoJSON utilizado como dato de prueba. Aunque el archivo tiene una estructura vÃ¡lida, representa un Ãrea de InterÃ©s demasiado grande para las restricciones esperadas del sistema.

#### Evidencia CP-MOD5-007 â€” ValidaciÃ³n de AOI fuera del Ã¡rea permitida

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-007-02-validacion-aoi-grande.png" alt="CP-MOD5-007 - ValidaciÃ³n de AOI fuera del Ã¡rea permitida" width="550">
</p>

Se evidencia que el sistema no permitiÃ³ avanzar con el AOI cargado, mostrando una validaciÃ³n o bloqueo asociado al tamaÃ±o o restricciones del Ãrea de InterÃ©s.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la ejecuciÃ³n se comprobÃ³ que el sistema controla las restricciones del Ãrea de InterÃ©s antes de permitir continuar con la generaciÃ³n de tareas. Al identificar que el AOI excede las condiciones permitidas, bloquea el avance y evita que se genere una grilla basada en un Ã¡rea no vÃ¡lida.


### 5.2.1. ValidaciÃ³n de campos obligatorios al guardar proyecto

**CP-MOD5-008**

| ID              | DescripciÃ³n                                                                                                                              | Tipo   | Estado  | Defectos                    |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-008** | Verificar que el sistema impida guardar un proyecto cuando existen campos obligatorios incompletos en la configuraciÃ³n del proyecto. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                      | Resultado obtenido                                                                                                                                                                                                                                                                                  |
| :------------------------------------------------------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe rechazar el guardado del proyecto si faltan campos obligatorios como descripciÃ³n, instrucciones o tipo de mapeo, mostrando un mensaje de validaciÃ³n comprensible para el usuario. | El sistema impidiÃ³ guardar el proyecto y mostrÃ³ un mensaje de validaciÃ³n indicando que falta informaciÃ³n en el idioma predeterminado del proyecto, especÃ­ficamente **DescripciÃ³n corta**, **DescripciÃ³n**, **Instrucciones detalladas** y el campo obligatorio **Tipos de mapeo**. |

#### Evidencia CP-MOD5-008 â€” Proyecto con campos obligatorios incompletos

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-008-01-proyecto-sin-campos-obligatorios.png" alt="CP-MOD5-008 - Proyecto sin campos obligatorios completos" width="400">
</p>

Se observa la pantalla de ediciÃ³n del proyecto con secciones obligatorias pendientes de completar, como descripciÃ³n, instrucciones y metadatos.

#### Evidencia CP-MOD5-008 â€” ValidaciÃ³n de campos obligatorios

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-008-02-validacion-campos-obligatorios.png" alt="CP-MOD5-008 - ValidaciÃ³n de campos obligatorios" width="300">
</p>

Se evidencia que el sistema bloqueÃ³ el guardado del proyecto y mostrÃ³ un mensaje de validaciÃ³n detallando los campos obligatorios faltantes. Esto confirma que el sistema controla entradas incompletas antes de guardar la configuraciÃ³n del proyecto.

### 5.2.2. Guardado de proyecto con campos obligatorios completos

**CP-MOD5-009**

| ID              | DescripciÃ³n                                                                                                                          | Tipo   | Estado  | Defectos                    |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-009** | Verificar que el sistema permita guardar un proyecto cuando los campos obligatorios de descripciÃ³n, instrucciones y metadatos han sido completados correctamente. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                          | Resultado obtenido                                                                                                                                                 |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir guardar el proyecto cuando los campos obligatorios se encuentran completos y vÃ¡lidos, mostrando una confirmaciÃ³n de actualizaciÃ³n exitosa. | El sistema guardÃ³ correctamente la configuraciÃ³n del proyecto y mostrÃ³ el mensaje **â€œProyecto actualizado correctamente.â€**. |

#### Evidencia CP-MOD5-009 â€” Campos obligatorios completados

<table>
  <tr>
    <td align="center">
      <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-009-01-descripcion-completa.png" alt="CP-MOD5-009 - DescripciÃ³n completada" width="350">
      <br>
      <strong>DescripciÃ³n completada</strong>
    </td>
    <td align="center">
      <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-009-02-instrucciones-completas.png" alt="CP-MOD5-009 - Instrucciones completadas" width="450">
      <br>
      <strong>Instrucciones completadas</strong>
    </td>
    <td align="center">
      <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-009-03-metadatos-tipo-mapeo.png" alt="CP-MOD5-009 - Metadatos completados" width="300">
      <br>
      <strong>Metadatos completados</strong>
    </td>
  </tr>
</table>

Se observa que el usuario completÃ³ las secciones obligatorias del proyecto: descripciÃ³n, instrucciones y metadatos, incluyendo el tipo de mapeo requerido por el sistema.
#### Evidencia CP-MOD5-009 â€” Proyecto guardado exitosamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-009-04-proyecto-guardado-exitosamente.png" alt="CP-MOD5-009 - Proyecto guardado exitosamente" width="400">
</p>

Se evidencia que el sistema aceptÃ³ la informaciÃ³n ingresada y mostrÃ³ el mensaje **â€œProyecto actualizado correctamente.â€**, confirmando que el proyecto fue guardado sin defectos.
### 5.2.3. ModificaciÃ³n del nombre del proyecto

**CP-MOD5-010**

| ID              | DescripciÃ³n                                                                                                 | Tipo   | Estado  | Defectos                    |
| :-------------- | :---------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-010** | Verificar que el sistema permita modificar el nombre de un proyecto existente desde la pantalla de ediciÃ³n. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                | Resultado obtenido                                                                                                             |
| :------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir modificar el nombre del proyecto, guardar el cambio y mostrar el nuevo nombre correctamente despuÃ©s de la actualizaciÃ³n. | El sistema permitiÃ³ modificar el nombre del proyecto, guardar los cambios y mostrar correctamente el nuevo nombre actualizado. |

#### Evidencia CP-MOD5-010 â€” Nombre inicial del proyecto

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-010-01-nombre-proyecto-inicial.png" alt="CP-MOD5-010 - Nombre inicial del proyecto" width="300">
</p>

Se observa el nombre inicial del proyecto antes de realizar la modificaciÃ³n desde la pantalla de ediciÃ³n.

#### Evidencia CP-MOD5-010 â€” Nombre del proyecto modificado

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-010-02-nombre-proyecto-modificado.png" alt="CP-MOD5-010 - Nombre del proyecto modificado" width="600">
</p>

Se evidencia que el usuario ingresÃ³ un nuevo nombre vÃ¡lido para el proyecto antes de guardar los cambios.

#### Evidencia CP-MOD5-010 â€” Nombre actualizado guardado correctamente

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-010-03-nombre-proyecto-guardado.png" alt="CP-MOD5-010 - Nombre actualizado guardado correctamente" width="300">
</p>

Se evidencia que el sistema guardÃ³ correctamente el nuevo nombre del proyecto y lo muestra actualizado en la interfaz.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la ejecuciÃ³n se comprobÃ³ que el sistema permite editar el nombre de un proyecto existente y conservar el cambio despuÃ©s de guardar. No se observaron errores ni pÃ©rdida de informaciÃ³n durante la actualizaciÃ³n.

### 5.2.4. ModificaciÃ³n de la descripciÃ³n corta del proyecto

**CP-MOD5-011**

| ID              | DescripciÃ³n                                                                                                            | Tipo   | Estado  | Defectos                    |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-011** | Verificar que el sistema permita modificar la descripciÃ³n corta de un proyecto existente desde la pantalla de ediciÃ³n. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                            | Resultado obtenido                                                                                                                                  |
| :-------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir modificar la descripciÃ³n corta del proyecto, guardar el cambio y mostrar una confirmaciÃ³n de actualizaciÃ³n correcta. | El sistema permitiÃ³ modificar la descripciÃ³n corta del proyecto y mostrÃ³ una notificaciÃ³n indicando que los cambios fueron guardados correctamente. |

#### Evidencia CP-MOD5-011 â€” DescripciÃ³n corta inicial

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-011-01-descripcion-corta-inicial.png" alt="CP-MOD5-011 - DescripciÃ³n corta inicial" width="500">
</p>

Se observa la descripciÃ³n corta del proyecto antes de realizar la modificaciÃ³n.

#### Evidencia CP-MOD5-011 â€” DescripciÃ³n corta modificada

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-011-02-descripcion-corta-modificada.png" alt="CP-MOD5-011 - DescripciÃ³n corta modificada" width="500">
</p>

Se evidencia que el usuario ingresÃ³ una nueva descripciÃ³n corta vÃ¡lida en la pantalla de ediciÃ³n del proyecto.

#### Evidencia CP-MOD5-011 â€” ConfirmaciÃ³n de guardado correcto

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-011-03-descripcion-corta-guardada.png" alt="CP-MOD5-011 - ConfirmaciÃ³n de guardado correcto" width="500">
</p>

Se evidencia que el sistema mostrÃ³ una notificaciÃ³n de guardado correcto, confirmando que la modificaciÃ³n de la descripciÃ³n corta fue procesada exitosamente.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la ejecuciÃ³n se comprobÃ³ que el sistema permite editar la descripciÃ³n corta del proyecto y guardar el cambio sin errores visibles. La notificaciÃ³n de confirmaciÃ³n permite verificar que la actualizaciÃ³n fue aceptada por el sistema.

### 5.2.5. ModificaciÃ³n de instrucciones detalladas del proyecto

**CP-MOD5-012**

| ID              | DescripciÃ³n                                                                                                                    | Tipo   | Estado  | Defectos                    |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-012** | Verificar que el sistema permita modificar las instrucciones detalladas de un proyecto existente desde la pantalla de ediciÃ³n. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                   | Resultado obtenido                                                                                                                                                            |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir modificar las instrucciones detalladas del proyecto, guardar los cambios y mantener el contenido actualizado en la secciÃ³n correspondiente. | El sistema permitiÃ³ modificar las instrucciones detalladas del proyecto y guardÃ³ correctamente los cambios, mostrando el contenido actualizado en la secciÃ³n correspondiente. |

#### Evidencia CP-MOD5-012 â€” Instrucciones detalladas iniciales

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-012-01-instrucciones-detalladas-inicial.png" alt="CP-MOD5-012 - Instrucciones detalladas iniciales" width="450">
</p>

Se observa el contenido inicial de las instrucciones detalladas del proyecto antes de realizar la modificaciÃ³n.

#### Evidencia CP-MOD5-012 â€” Instrucciones detalladas modificadas

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-012-02-instrucciones-detalladas-modificadas.png" alt="CP-MOD5-012 - Instrucciones detalladas modificadas" width="450">
</p>

Se evidencia que el usuario ingresÃ³ nuevas instrucciones detalladas vÃ¡lidas desde la pantalla de ediciÃ³n del proyecto.

#### Evidencia CP-MOD5-012 â€” Instrucciones detalladas guardadas correctamente

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-012-03-instrucciones-detalladas-guardadas.png" alt="CP-MOD5-012 - Instrucciones detalladas guardadas correctamente" width="650">
</p>

Se evidencia que el sistema mostrÃ³ o mantuvo las instrucciones detalladas actualizadas, confirmando que la modificaciÃ³n fue procesada correctamente.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la ejecuciÃ³n se comprobÃ³ que el sistema permite editar las instrucciones detalladas del proyecto y conservar los cambios despuÃ©s del guardado. No se observaron errores visibles ni pÃ©rdida de informaciÃ³n durante la actualizaciÃ³n.

### 5.2.6. ValidaciÃ³n de guardado sin cambios en la configuraciÃ³n del proyecto

**CP-MOD5-013**

| ID              | DescripciÃ³n                                                                                                                            | Tipo   | Estado  | Defectos                    |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-013** | Verificar que el sistema permita guardar la configuraciÃ³n de un proyecto sin realizar modificaciones visibles en los campos editables. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                     | Resultado obtenido                                                                                                                             |
| :----------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir guardar la configuraciÃ³n sin realizar cambios, mantener la informaciÃ³n existente y no presentar errores durante la operaciÃ³n. | El sistema permitiÃ³ guardar la configuraciÃ³n del proyecto sin realizar modificaciones visibles y mostrÃ³ una confirmaciÃ³n de guardado correcto. |

#### Evidencia CP-MOD5-013 â€” ConfiguraciÃ³n sin modificaciÃ³n

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-013-01-configuracion-sin-modificacion.png" alt="CP-MOD5-013 - ConfiguraciÃ³n sin modificaciÃ³n" width="650">
</p>

Se observa la pantalla de configuraciÃ³n del proyecto sin modificaciones visibles realizadas por el usuario antes de ejecutar la acciÃ³n de guardado.

#### Evidencia CP-MOD5-013 â€” ConfirmaciÃ³n de guardado sin cambios

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-013-02-confirmacion-guardado-sin-cambios.png" alt="CP-MOD5-013 - ConfirmaciÃ³n de guardado sin cambios" width="650">
</p>

Se evidencia que el sistema mostrÃ³ una confirmaciÃ³n de guardado correcto aun cuando no se realizaron cambios visibles en la configuraciÃ³n del proyecto.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la ejecuciÃ³n se comprobÃ³ que el sistema permite guardar la configuraciÃ³n del proyecto sin modificar campos. La informaciÃ³n existente se mantuvo estable y no se presentaron errores visibles durante la operaciÃ³n.


### 5.3.1. PublicaciÃ³n del proyecto desde estado Borrador

**CP-MOD5-014**

| ID              | DescripciÃ³n                                                                                                                  | Tipo   | Estado  | Defectos                    |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-014** | Verificar que el sistema permita cambiar el estado de un proyecto desde **Borrador** hacia **Publicado** cuando la configuraciÃ³n obligatoria se encuentra completa. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                              | Resultado obtenido                                                                                                                                                     |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir cambiar el estado del proyecto de **Borrador** a **Publicado**, guardar la modificaciÃ³n y mostrar una confirmaciÃ³n de actualizaciÃ³n exitosa. | El sistema permitiÃ³ seleccionar el estado **Publicado**, guardÃ³ correctamente el cambio y mostrÃ³ la confirmaciÃ³n de actualizaciÃ³n del proyecto. |

#### Evidencia CP-MOD5-014 â€” Estado inicial Borrador

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-014-01-estado-borrador.png" alt="CP-MOD5-014 - Estado inicial Borrador" width="450">
</p>

Se observa que el proyecto se encuentra inicialmente en estado **Borrador**, antes de realizar la transiciÃ³n de estado.

#### Evidencia CP-MOD5-014 â€” Estado Publicado seleccionado

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-014-02-estado-publicado-seleccionado.png" alt="CP-MOD5-014 - Estado Publicado seleccionado" width="450">
</p>

Se observa que el usuario seleccionÃ³ el estado **Publicado** como nuevo estado del proyecto.

#### Evidencia CP-MOD5-014 â€” Proyecto publicado correctamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-014-03-proyecto-publicado-guardado.png" alt="CP-MOD5-014 - Proyecto publicado correctamente" width="450">
</p>

Se evidencia que el sistema guardÃ³ correctamente el cambio de estado y confirmÃ³ la actualizaciÃ³n del proyecto. Esto demuestra que la transiciÃ³n **Borrador â†’ Publicado** fue realizada correctamente desde la interfaz.
### 5.3.2. Intento de publicar proyecto con campos obligatorios incompletos

**CP-MOD5-015**

| ID              | DescripciÃ³n                                                                                          | Tipo   | Estado  | Defectos                    |
| :-------------- | :--------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-015** | Verificar que el sistema impida publicar un proyecto cuando existen campos obligatorios incompletos. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                  | Resultado obtenido                                                                                                                         |
| :-------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe impedir la publicaciÃ³n del proyecto si faltan campos obligatorios, mostrando mensajes de validaciÃ³n sobre la informaciÃ³n requerida. | El sistema no permitiÃ³ publicar el proyecto y mostrÃ³ un error indicando que faltaba informaciÃ³n obligatoria para completar la publicaciÃ³n. |

#### Evidencia CP-MOD5-015 â€” Proyecto en borrador con informaciÃ³n incompleta

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-015-01-proyecto-borrador-incompleto.png" alt="CP-MOD5-015 - Proyecto en borrador con informaciÃ³n incompleta" width="350">
</p>

Se observa el proyecto en estado de ediciÃ³n/borrador con informaciÃ³n obligatoria incompleta antes de intentar su publicaciÃ³n.

#### Evidencia CP-MOD5-015 â€” Intento de publicaciÃ³n del proyecto incompleto

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-015-02-intento-publicacion-incompleta.png" alt="CP-MOD5-015 - Intento de publicaciÃ³n incompleta" width="350">
</p>

Se evidencia el intento de cambiar el estado del proyecto a publicado sin contar con toda la informaciÃ³n obligatoria requerida.

#### Evidencia CP-MOD5-015 â€” ValidaciÃ³n por informaciÃ³n incompleta

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-015-03-validacion-publicacion-incompleta.png" alt="CP-MOD5-015 - ValidaciÃ³n por informaciÃ³n incompleta" width="450">
</p>

Se evidencia que el sistema mostrÃ³ un mensaje de validaciÃ³n indicando que faltaba informaciÃ³n obligatoria, impidiendo la publicaciÃ³n del proyecto.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la ejecuciÃ³n se comprobÃ³ que el sistema valida la informaciÃ³n obligatoria antes de permitir la publicaciÃ³n de un proyecto. Al detectar campos incompletos, bloqueÃ³ el cambio de estado y evitÃ³ que el proyecto sea publicado sin cumplir las condiciones requeridas.

### 5.3.3. Cambio de estado de proyecto publicado a borrador

**CP-MOD5-016**

| ID              | DescripciÃ³n                                                                                                          | Tipo   | Estado  | Defectos                    |
| :-------------- | :------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-016** | Verificar que el sistema permita cambiar el estado de un proyecto publicado a borrador desde la pantalla de ediciÃ³n. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                         | Resultado obtenido                                                                                                           |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir cambiar el estado del proyecto de Publicado a Borrador, guardar el cambio y mantener el nuevo estado despuÃ©s de la actualizaciÃ³n. | El sistema permitiÃ³ cambiar el estado del proyecto de Publicado a Borrador y guardÃ³ correctamente la modificaciÃ³n realizada. |

#### Evidencia CP-MOD5-016 â€” Proyecto en estado publicado

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-016-01-proyecto-estado-publicado.png" alt="CP-MOD5-016 - Proyecto en estado publicado" width="350">
</p>

Se observa que el proyecto se encontraba inicialmente en estado **Publicado** antes de realizar la modificaciÃ³n.

#### Evidencia CP-MOD5-016 â€” Cambio de estado a borrador

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-016-02-cambio-estado-borrador.png" alt="CP-MOD5-016 - Cambio de estado a borrador" width="350">
</p>

Se evidencia que el usuario seleccionÃ³ el estado **Borrador** desde la pantalla de ediciÃ³n del proyecto.

#### Evidencia CP-MOD5-016 â€” Estado borrador guardado correctamente

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-016-03-estado-borrador-guardado.png" alt="CP-MOD5-016 - Estado borrador guardado correctamente" width="450">
</p>

Se evidencia que el sistema guardÃ³ correctamente el cambio de estado, manteniendo el proyecto como **Borrador** despuÃ©s de la actualizaciÃ³n.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la ejecuciÃ³n se comprobÃ³ que el sistema permite revertir el estado de un proyecto publicado a borrador. El cambio fue procesado correctamente y no se presentaron errores visibles durante el guardado.



### 5.4.1. ConfiguraciÃ³n de permisos del proyecto

**CP-MOD5-017**

| ID              | DescripciÃ³n                                                                                                                        | Tipo   | Estado  | Defectos                    |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-017** | Verificar que el sistema permita configurar los permisos de mapeo y validaciÃ³n de un proyecto mediante niveles mÃ­nimos de usuario. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                      | Resultado obtenido                                                                                                                                                                                                              |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| El sistema debe permitir modificar los permisos del proyecto, estableciendo niveles mÃ­nimos requeridos para mapear y validar, y guardar la configuraciÃ³n correctamente. | El sistema permitiÃ³ modificar los permisos del proyecto, estableciendo el nivel **INTERMEDIATE** para mapeo y validaciÃ³n. La configuraciÃ³n fue guardada correctamente y permaneciÃ³ visible en la secciÃ³n de equipos y permisos. |

#### Evidencia CP-MOD5-017 â€” Pantalla inicial de permisos

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-017-01-pantalla-permisos-inicial.png" alt="CP-MOD5-017 - Pantalla inicial de permisos" width="450">
</p>

Se observa la secciÃ³n de permisos del proyecto, donde el sistema permite definir quÃ© usuarios pueden mapear y validar, asÃ­ como los niveles mÃ­nimos requeridos para cada acciÃ³n.

#### Evidencia CP-MOD5-017 â€” Nivel mÃ­nimo de mapeo modificado

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-017-02-nivel-mapeo-intermediate.png" alt="CP-MOD5-017 - Nivel mÃ­nimo de mapeo modificado" width="550">
</p>

Se observa que el usuario modificÃ³ la configuraciÃ³n de permisos, estableciendo un nivel mÃ­nimo requerido para acceder a las acciones del proyecto.

#### Evidencia CP-MOD5-017 â€” Permisos guardados correctamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-017-03-permisos-guardados-correctamente.png" alt="CP-MOD5-017 - Permisos guardados correctamente" width="550">
</p>

Se evidencia que el sistema guardÃ³ correctamente la configuraciÃ³n de permisos, mostrando que todos los usuarios con nivel **INTERMEDIATE** o superior pueden mapear y validar el proyecto.

### 5.4.2. ActivaciÃ³n de privacidad del proyecto

**CP-MOD5-018**

| ID              | DescripciÃ³n                                                                                                                 | Tipo   | Estado  | Defectos                    |
| :-------------- | :-------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-018** | Verificar que el sistema permita activar la opciÃ³n de proyecto privado dentro de la configuraciÃ³n de permisos del proyecto. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                         | Resultado obtenido                                                                                                                                                     |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir activar la privacidad del proyecto, guardar la configuraciÃ³n y mantener activa la opciÃ³n **Proyecto privado** despuÃ©s de guardar. | El sistema permitiÃ³ activar la opciÃ³n **Proyecto privado**, guardÃ³ correctamente el cambio y mantuvo la configuraciÃ³n aplicada en la secciÃ³n de permisos del proyecto. |

#### Evidencia CP-MOD5-018 â€” Privacidad inicial del proyecto

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-018-01-privacidad-inicial.png" alt="CP-MOD5-018 - Privacidad inicial del proyecto" width="650">
</p>

Se observa la secciÃ³n de privacidad del proyecto antes de realizar la modificaciÃ³n, donde la opciÃ³n **Proyecto privado** se encuentra inicialmente desactivada.

#### Evidencia CP-MOD5-018 â€” Proyecto privado activado

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-018-02-proyecto-privado-activado.png" alt="CP-MOD5-018 - Proyecto privado activado" width="650">
</p>

Se observa que el usuario activÃ³ la opciÃ³n **Proyecto privado**, modificando la configuraciÃ³n de acceso al proyecto.

#### Evidencia CP-MOD5-018 â€” Privacidad guardada correctamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-018-03-privacidad-guardada-correctamente.png" alt="CP-MOD5-018 - Privacidad guardada correctamente" width="400">
</p>

Se evidencia que el sistema guardÃ³ correctamente la configuraciÃ³n de privacidad del proyecto. Esto confirma que la opciÃ³n de proyecto privado puede ser modificada desde la interfaz y persistida correctamente.


### 5.4.3. Transferencia de propiedad del proyecto

**CP-MOD5-019**

| ID              | DescripciÃ³n                                                                                                                                              | Tipo   | Estado  | Defectos                    |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-019** | Verificar que el sistema permita transferir la propiedad de un proyecto a otro usuario administrador de Tasking Manager perteneciente a la organizaciÃ³n. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                                           | Resultado obtenido                                                                                                                                                         |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir seleccionar un nuevo propietario vÃ¡lido del proyecto y transferir la propiedad cuando el usuario seleccionado tiene permisos suficientes dentro de Tasking Manager. | El sistema permitiÃ³ seleccionar otro administrador de Tasking Manager perteneciente a la organizaciÃ³n y realizar correctamente la transferencia de propiedad del proyecto. |

#### Evidencia CP-MOD5-019 â€” Formulario de transferencia de propiedad

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-019-01-formulario-transferencia-propiedad.png" alt="CP-MOD5-019 - Formulario de transferencia de propiedad" width="650">
</p>

Se observa la secciÃ³n de transferencia de propiedad del proyecto. El sistema muestra una advertencia indicando que esta acciÃ³n no se puede deshacer, lo cual informa al usuario sobre el impacto de la operaciÃ³n antes de ejecutarla.

#### Evidencia CP-MOD5-019 â€” SelecciÃ³n de nuevo propietario

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-019-02-admin-tm-seleccionado.png" alt="CP-MOD5-019 - Administrador seleccionado como nuevo propietario" width="650">
</p>

Se observa que el usuario seleccionÃ³ como nuevo propietario a otro administrador de Tasking Manager perteneciente a la organizaciÃ³n, cumpliendo la condiciÃ³n requerida para realizar la transferencia.

#### Evidencia CP-MOD5-019 â€” Propiedad transferida correctamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-019-03-propiedad-transferida-correctamente.png" alt="CP-MOD5-019 - Propiedad transferida correctamente" width="650">
</p>

Se evidencia que el sistema ejecutÃ³ correctamente la transferencia de propiedad del proyecto. Esto confirma que la funcionalidad permite cambiar el propietario del proyecto hacia otro usuario con permisos suficientes dentro de la organizaciÃ³n.
### 5.4.4. ConfiguraciÃ³n de dificultad del proyecto

**CP-MOD5-020**

| ID              | DescripciÃ³n                                                                                                     | Tipo   | Estado  | Defectos                    |
| :-------------- | :-------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-020** | Verificar que el sistema permita modificar la dificultad de un proyecto existente desde la pantalla de ediciÃ³n. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                              | Resultado obtenido                                                                                   |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| El sistema debe permitir seleccionar una dificultad vÃ¡lida para el proyecto, guardar el cambio y mantener la dificultad actualizada despuÃ©s de la modificaciÃ³n. | El sistema permitiÃ³ modificar la dificultad del proyecto y guardÃ³ correctamente el cambio realizado. |

#### Evidencia CP-MOD5-020 â€” Dificultad inicial del proyecto

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-020-01-dificultad-inicial.png" alt="CP-MOD5-020 - Dificultad inicial del proyecto" width="450">
</p>

Se observa la dificultad inicial configurada en el proyecto antes de realizar la modificaciÃ³n.

#### Evidencia CP-MOD5-020 â€” Dificultad modificada

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-020-02-dificultad-modificada.png" alt="CP-MOD5-020 - Dificultad modificada" width="450">
</p>

Se evidencia que el usuario seleccionÃ³ una nueva dificultad vÃ¡lida desde la pantalla de ediciÃ³n del proyecto.

#### Evidencia CP-MOD5-020 â€” Dificultad guardada correctamente

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-020-03-dificultad-guardada.png" alt="CP-MOD5-020 - Dificultad guardada correctamente" width="250">
</p>

Se evidencia que el sistema guardÃ³ correctamente el cambio de dificultad del proyecto, sin mostrar errores visibles.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la ejecuciÃ³n se comprobÃ³ que el sistema permite modificar la dificultad del proyecto y guardar el cambio correctamente. La operaciÃ³n se completÃ³ sin errores visibles en la interfaz.

### 5.4.5. ConfiguraciÃ³n de prioridad del proyecto

**CP-MOD5-021**

| ID              | DescripciÃ³n                                                                                                    | Tipo   | Estado  | Defectos                    |
| :-------------- | :------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-021** | Verificar que el sistema permita modificar la prioridad de un proyecto existente desde la pantalla de ediciÃ³n. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                            | Resultado obtenido                                                                                  |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------- |
| El sistema debe permitir seleccionar una prioridad vÃ¡lida para el proyecto, guardar el cambio y mantener la prioridad actualizada despuÃ©s de la modificaciÃ³n. | El sistema permitiÃ³ modificar la prioridad del proyecto y guardÃ³ correctamente el cambio realizado. |

#### Evidencia CP-MOD5-021 â€” Prioridad inicial del proyecto

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-021-01-prioridad-inicial.png" alt="CP-MOD5-021 - Prioridad inicial del proyecto" width="550">
</p>

Se observa la prioridad inicial configurada en el proyecto antes de realizar la modificaciÃ³n.

#### Evidencia CP-MOD5-021 â€” Prioridad modificada

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-021-02-prioridad-modificada.png" alt="CP-MOD5-021 - Prioridad modificada" width="550">
</p>

Se evidencia que el usuario seleccionÃ³ una nueva prioridad vÃ¡lida desde la pantalla de ediciÃ³n del proyecto.

#### Evidencia CP-MOD5-021 â€” Prioridad guardada correctamente

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-021-03-prioridad-guardada.png" alt="CP-MOD5-021 - Prioridad guardada correctamente" width="650">
</p>

Se evidencia que el sistema guardÃ³ correctamente el cambio de prioridad del proyecto, sin mostrar errores visibles.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la ejecuciÃ³n se comprobÃ³ que el sistema permite modificar la prioridad del proyecto y guardar el cambio correctamente. La operaciÃ³n se completÃ³ sin errores visibles en la interfaz.

### 5.5.1. ClonaciÃ³n de proyecto existente

**CP-MOD5-022**

| ID              | DescripciÃ³n                                                                                                                               | Tipo   | Estado  | Defectos                    |
| :-------------- | :---------------------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-022** | Verificar que el sistema permita clonar un proyecto existente y generar un nuevo proyecto basado en la informaciÃ³n del proyecto original. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                                 | Resultado obtenido                                                                                                                                                                                             |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir iniciar el flujo de clonaciÃ³n desde un proyecto existente, conservar la informaciÃ³n base del proyecto original y generar un nuevo proyecto independiente. | El sistema iniciÃ³ correctamente el flujo de clonaciÃ³n del proyecto **#1 Proyecto Arequipa** y generÃ³ un nuevo proyecto clonado identificado como **#3 Proyecto Arequipa**, visible en el listado de proyectos. |

#### Evidencia CP-MOD5-022 â€” OpciÃ³n de clonar proyecto

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-022-01-opcion-clonar-proyecto.png" alt="CP-MOD5-022 - OpciÃ³n de clonar proyecto" width="650">
</p>

Se observa la opciÃ³n que permite iniciar la clonaciÃ³n de un proyecto existente desde las acciones disponibles para el proyecto.

#### Evidencia CP-MOD5-022 â€” Flujo de clonaciÃ³n iniciado

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-022-02-flujo-clonacion-iniciado.png" alt="CP-MOD5-022 - Flujo de clonaciÃ³n iniciado" width="350">
</p>

Se evidencia que el sistema iniciÃ³ el flujo de clonaciÃ³n e indicÃ³ que el nuevo proyecto serÃ¡ un clon del proyecto **#1 Proyecto Arequipa**.

#### Evidencia CP-MOD5-022 â€” RevisiÃ³n del proyecto clonado

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-022-03-revision-proyecto-clonado.png" alt="CP-MOD5-022 - RevisiÃ³n del proyecto clonado" width="450">
</p>

Se observa el paso de revisiÃ³n del proyecto clonado antes de finalizar su creaciÃ³n.

#### Evidencia CP-MOD5-022 â€” Proyecto clonado creado correctamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-022-04-proyecto-clonado-creado.png" alt="CP-MOD5-022 - Proyecto clonado creado correctamente" width="450">
</p>

Se evidencia que el sistema creÃ³ correctamente un nuevo proyecto clonado. En el listado se muestran dos proyectos: el proyecto original **#1 Proyecto Arequipa** y el proyecto clonado **#3 Proyecto Arequipa**, confirmando que la clonaciÃ³n fue ejecutada correctamente.

### 5.5.2. EliminaciÃ³n controlada de proyecto

**CP-MOD5-023**

| ID              | DescripciÃ³n                                                                                                                                               | Tipo   | Estado  | Defectos                    |
| :-------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-023** | Verificar que el sistema permita eliminar un proyecto desde la secciÃ³n de acciones y redirija correctamente al usuario despuÃ©s de completar la operaciÃ³n. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                                                                                     | Resultado obtenido                                                                                                                                                             |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir eliminar un proyecto mediante una acciÃ³n controlada, mostrar una confirmaciÃ³n o advertencia antes de ejecutar la operaciÃ³n y redirigir al usuario a una vista adecuada despuÃ©s de eliminarlo. | El sistema eliminÃ³ correctamente el proyecto seleccionado y redirigiÃ³ al usuario a la vista de gestiÃ³n de proyectos, confirmando que la operaciÃ³n fue ejecutada correctamente. |

#### Evidencia CP-MOD5-023 â€” OpciÃ³n de eliminar proyecto

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-023-01-opcion-eliminar-proyecto.png" alt="CP-MOD5-023 - OpciÃ³n de eliminar proyecto" width="650">
</p>

Se observa la opciÃ³n disponible para eliminar el proyecto desde la secciÃ³n de acciones. Esta funcionalidad permite al usuario autorizado iniciar una operaciÃ³n sensible sobre el proyecto.

#### Evidencia CP-MOD5-023 â€” ConfirmaciÃ³n de eliminaciÃ³n

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-023-02-confirmacion-eliminacion.png" alt="CP-MOD5-023 - ConfirmaciÃ³n de eliminaciÃ³n" width="650">
</p>

Se observa la confirmaciÃ³n o advertencia previa a la eliminaciÃ³n del proyecto, lo cual permite evitar una eliminaciÃ³n accidental.

#### Evidencia CP-MOD5-023 â€” Proyecto eliminado y redirecciÃ³n a gestiÃ³n de proyectos

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-023-03-proyecto-eliminado-vista-gestion.png" alt="CP-MOD5-023 - Proyecto eliminado y redirecciÃ³n" width="650">
</p>

Se evidencia que el sistema eliminÃ³ correctamente el proyecto y redirigiÃ³ al usuario a la vista de gestiÃ³n de proyectos. Esto confirma que la eliminaciÃ³n fue procesada de forma controlada desde la interfaz.

### 5.5.3. ConfiguraciÃ³n de fuente de imÃ¡genes del proyecto

**CP-MOD5-024**

| ID              | DescripciÃ³n                                                                                                                     | Tipo   | Estado  | Defectos                    |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------ | :----- | :------ | :-------------------------- |
| **CP-MOD5-024** | Verificar que el sistema permita seleccionar una fuente de imÃ¡genes vÃ¡lida para el proyecto y guardar correctamente la configuraciÃ³n. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                        | Resultado obtenido                                                                                                                                               |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe permitir seleccionar una fuente de imÃ¡genes vÃ¡lida para el proyecto, guardar la configuraciÃ³n y mantener visible la opciÃ³n seleccionada. | El sistema permitiÃ³ seleccionar la fuente de imÃ¡genes **Bing**, guardÃ³ correctamente la configuraciÃ³n y mostrÃ³ el mensaje de actualizaciÃ³n exitosa del proyecto. |

#### Evidencia CP-MOD5-024 â€” Pantalla inicial de imÃ¡genes

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-024-01-pantalla-imagenes-inicial.png" alt="CP-MOD5-024 - Pantalla inicial de imÃ¡genes" width="650">
</p>

Se observa la secciÃ³n **ImÃ¡genes** del proyecto, donde el sistema presenta distintas fuentes de imÃ¡genes disponibles para configurar el mapeo del proyecto, tales como Bing, Mapbox Satellite, ESRI World Imagery y Maxar Standard.

#### Evidencia CP-MOD5-024 â€” Fuente Bing seleccionada y guardada correctamente

<p align="center">
  <img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-0005-administracion-proyectos/CP-MOD5-024-02-fuente-bing-guardada-correctamente.png" alt="CP-MOD5-024 - Fuente Bing guardada correctamente" width="550">
</p>

Se evidencia que el usuario seleccionÃ³ la fuente de imÃ¡genes **Bing** y que el sistema guardÃ³ correctamente la configuraciÃ³n, confirmando que la fuente de mapeo fue actualizada sin defectos.
### 5.5.4. CancelaciÃ³n de eliminaciÃ³n de proyecto

**CP-MOD5-025**

| ID              | DescripciÃ³n                                                                                              | Tipo   | Estado  | Defectos                    |
| :-------------- | :------------------------------------------------------------------------------------------------------- | :----- | :------ | :-------------------------- |
| **CP-MOD5-025** | Verificar que el sistema permita cancelar la eliminaciÃ³n de un proyecto antes de confirmar la operaciÃ³n. | Manual | Exitoso | No se encontraron defectos. |

| Resultado esperado                                                                                                                                    | Resultado obtenido                                                                                                                                             |
| :---------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El sistema debe mostrar una confirmaciÃ³n antes de eliminar el proyecto, permitir cancelar la operaciÃ³n y mantener el proyecto disponible sin cambios. | El sistema permitiÃ³ cancelar la eliminaciÃ³n del proyecto correctamente. DespuÃ©s de cancelar, el proyecto no fue eliminado y continuÃ³ disponible en el sistema. |

#### Evidencia CP-MOD5-025 â€” OpciÃ³n de eliminar proyecto

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-025-01-opcion-eliminar-proyecto.png" alt="CP-MOD5-025 - OpciÃ³n de eliminar proyecto" width="450">
</p>

Se observa la opciÃ³n disponible para iniciar la eliminaciÃ³n del proyecto desde la interfaz de administraciÃ³n.

#### Evidencia CP-MOD5-025 â€” ConfirmaciÃ³n de eliminaciÃ³n

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-025-02-confirmacion-eliminacion.png" alt="CP-MOD5-025 - ConfirmaciÃ³n de eliminaciÃ³n" width="450">
</p>

Se evidencia que el sistema muestra una ventana o mensaje de confirmaciÃ³n antes de ejecutar la eliminaciÃ³n del proyecto.

#### Evidencia CP-MOD5-025 â€” CancelaciÃ³n de eliminaciÃ³n

<p align="center">
  <img src="./img/MOD-0005-administracion-proyectos/CP-MOD5-025-03-cancelacion-eliminacion.png" alt="CP-MOD5-025 - CancelaciÃ³n de eliminaciÃ³n" width="300">
</p>

Se evidencia que la operaciÃ³n de eliminaciÃ³n fue cancelada y que el proyecto continuÃ³ disponible en el sistema.

#### ObservaciÃ³n de ejecuciÃ³n

Durante la ejecuciÃ³n se comprobÃ³ que el sistema solicita confirmaciÃ³n antes de eliminar un proyecto. Al cancelar la operaciÃ³n, el proyecto no fue eliminado y se mantuvo disponible, evitando una eliminaciÃ³n accidental.






