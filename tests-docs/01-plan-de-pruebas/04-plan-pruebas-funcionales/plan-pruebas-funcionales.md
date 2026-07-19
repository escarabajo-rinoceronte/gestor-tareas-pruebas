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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — Plan de Pruebas Funcionales (Caja Negra)</td></tr>
      <tr><td class="label">Fecha</td><td>11/06/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
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

