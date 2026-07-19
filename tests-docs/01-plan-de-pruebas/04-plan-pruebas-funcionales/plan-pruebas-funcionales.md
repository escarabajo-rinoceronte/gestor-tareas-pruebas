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
  <b>Proyecto:</b> HOT Tasking Manager — Plan de Pruebas Funcionales (Caja Negra) <br>
  <b>Fecha de Elaboración:</b> 11/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Plan de Pruebas Funcionales (Caja Negra)

**Proyecto:** HOT OSM Tasking Manager  
**Equipo de Pruebas:** Escarabajo Rinoceronte  
**EstÃ¡ndar de Referencia:** ISO/IEC/IEEE 29119-3:2013 (Sub-process Test Plan)  
**Tipo de documento:** Plan de Pruebas Funcionales (Conceptual)  

---

## 1. IntroducciÃ³n

### 1.1. PropÃ³sito y Enfoque del Documento
El presente documento define el Plan de Pruebas Funcionales de Caja Negra para el proyecto Tasking Manager. El objetivo primordial es estructurar la validaciÃ³n del sistema centrÃ¡ndose exclusivamente en el comportamiento observable de la interfaz grÃ¡fica de usuario (UI), asegurando que las funcionalidades operen de acuerdo con las expectativas y necesidades operativas de los usuarios finales (Mapeadores y Validadores).

### 1.2. DeclaraciÃ³n de IngenierÃ­a Inversa de Requisitos (Importante)
Dado que el repositorio original de cÃ³digo abierto **HOT OSM Tasking Manager** no cuenta con una especificaciÃ³n formal de requisitos de software (SRS) o un documento de requerimientos funcionales explÃ­citos en su cÃ³digo base, **el equipo de Aseguramiento de la Calidad (QA) ha generado y formalizado de manera analÃ­tica los requerimientos funcionales a propio criterio y mediante ingenierÃ­a inversa** (documentados en `02-diseno-de-pruebas/funcionales/01-requerimientos-funcionales.md`). Esta especificaciÃ³n deducida actÃºa como la lÃ­nea base funcional oficial para el diseÃ±o y ejecuciÃ³n de todos los escenarios de Caja Negra.

---

## 2. Alcance del Testing Funcional

### Dentro del Alcance (In-Scope):
*   ValidaciÃ³n de la interfaz de usuario (React) interactuando con los endpoints de la API.
*   Pruebas manuales de Caja Negra sobre los flujos de administraciÃ³n de proyectos, mapeo y bloqueo de tareas.
*   VerificaciÃ³n de restricciones lÃ³gicas, control de acceso basado en roles (RBAC) y validaciÃ³n de formularios.

### Fuera del Alcance (Out-of-Scope):
*   Pruebas de la arquitectura interna de cÃ³digo, anÃ¡lisis estÃ¡tico y cobertura lÃ³gica (cubiertos en el Plan Unitario).
*   Pruebas de rendimiento, escalabilidad o respuesta ante cargas concurrentes extremas en el servidor local.

---

## 3. Estrategia de Pruebas de Caja Negra

Para garantizar la cobertura del comportamiento del sistema, los Test Designers aplicarÃ¡n las siguientes tÃ©cnicas estipuladas por la norma **ISO/IEC/IEEE 29119-4**:

### 3.1. ParticiÃ³n de Equivalencia (PE)
Se dividirÃ¡ el dominio de los datos de entrada en clases vÃ¡lidas e invÃ¡lidas para minimizar la cantidad de casos necesarios manteniendo una cobertura exhaustiva (ejemplo: validar la carga de polÃ­gonos GeoJSON correctos vs. formatos de archivos no permitidos).

### 3.2. AnÃ¡lisis de Valores LÃ­mite (AVL)
VerificaciÃ³n de los extremos numÃ©ricos y de longitud en campos restrictivos del sistema (ejemplo: probar nombres de proyectos vacÃ­os, con un solo carÃ¡cter o que excedan el lÃ­mite de 100 caracteres).

### 3.3. Tablas de DecisiÃ³n (TD)
Modelado de combinaciones lÃ³gicas de permisos y roles del sistema para evaluar flujos restrictivos de seguridad (ejemplo: validar que un mapper comÃºn no pueda aprobar tareas o que un usuario no pueda auto-validarse).

### 3.4. TransiciÃ³n de Estados (TE)
ValidaciÃ³n del ciclo de vida transaccional del mapa, asegurando que las tareas sigan la secuencia de estados permitidos de la base PostGIS (`READY`, `LOCKED`, `MAPPED`, `VALIDATED`).

---

## 4. Criterios de Entrada y Salida

### 4.1. Criterios de Entrada (Fase de EjecuciÃ³n)
*   Disponer del entorno de pruebas unificado (QA local) desplegado de forma estable con Docker Compose.
*   Contar con el documento de especificaciÃ³n de requerimientos de QA y el diseÃ±o de casos de prueba finalizado y aprobado por el Test Lead en la Wiki.
*   Base de datos inicializada con usuarios de prueba y roles configurados.

### 4.2. Criterios de Salida
*   Haber ejecutado el 100% de los casos de prueba diseÃ±ados para los mÃ³dulos seleccionados.
*   Alcanzar una tasa de Ã©xito de pruebas funcionales aprobadas igual o superior al **95%**.
*   No contar con defectos de prioridad CrÃ­tica o Alta sin corregir o sin mitigar.

---

## 5. Entregables de la Fase Funcional
*   **Plan de Pruebas Funcionales:** El presente documento estratÃ©gico.
*   **DiseÃ±o de Casos de Prueba Funcionales:** EspecificaciÃ³n detallada de entradas, pasos y resultados esperados.
*   **Informe de EjecuciÃ³n de Pruebas Funcionales:** Registro de la ejecuciÃ³n manual en el entorno de QA, detallando Ã©xitos, fallos identificados y adjuntando las capturas de pantalla de la interfaz como evidencias fÃ­sicas.



