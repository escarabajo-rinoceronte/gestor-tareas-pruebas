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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — Plan Maestro de Pruebas: IntroducciÃ³n y Alcance</td></tr>
      <tr><td class="label">Fecha</td><td>11/06/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# Plan Maestro de Pruebas: IntroducciÃ³n y Alcance

**Proyecto:** HOT OSM Tasking Manager  
**EstÃ¡ndar de Referencia:** ISO/IEC/IEEE 29119-3:2013 (DocumentaciÃ³n de Pruebas)  

## 1. PropÃ³sito del Documento
El presente documento constituye la base del **Plan Maestro de Pruebas (Master Test Plan)** para el proyecto Tasking Manager. Su objetivo es definir el contexto, el alcance global, los lÃ­mites de la intervenciÃ³n de QA y la arquitectura funcional del sistema. Este documento actÃºa como la mÃ¡xima directriz de la cual se derivan los planes de las fases subsiguientes (Unitarias, IntegraciÃ³n, Sistema y AceptaciÃ³n).

## 2. Contexto General del Proyecto
El **Tasking Manager (TM)** es una herramienta de cÃ³digo abierto desarrollada por el *Humanitarian OpenStreetMap Team (HOT)*. Permite la coordinaciÃ³n masiva de mapeadores voluntarios. El sistema delimita Ã¡reas geogrÃ¡ficas de interÃ©s afectadas por desastres o necesidades humanitarias, subdividiÃ©ndolas en cuadrÃ­culas (tareas) mÃ¡s pequeÃ±as. Estas tareas pasan por un ciclo de vida estricto: **Disponible, Mapeada, Validada (QA) y Completada**.

Dada la criticidad humanitaria de los datos y el alto volumen de concurrencia, el aseguramiento de la calidad funcional, espacial y de seguridad del cÃ³digo es un requisito innegociable.

## 3. Arquitectura y MÃ³dulos Bajo Prueba (SUT)
Desde la perspectiva del Aseguramiento de Calidad, el Sistema Bajo Prueba (System Under Test - SUT) se compone de una arquitectura distribuida que interactÃºa con servicios externos crÃ­ticos.

### 3.1. TopologÃ­a del Sistema
El siguiente diagrama detalla las capas arquitectÃ³nicas que serÃ¡n sometidas a los distintos niveles de prueba.

![Arquitectura de anÃ¡lisis](/tests-docs/01-plan-de-pruebas/01-plan-general/img/arquitectura-general.png) 

*(Nota: Este diagrama debe utilizarse para comprender el flujo de los datos al diseÃ±ar las pruebas de integraciÃ³n y sistema).*

### 3.2. MÃ³dulos Funcionales CrÃ­ticos
1. **GestiÃ³n de Proyectos (AdministraciÃ³n):** CreaciÃ³n de Ã¡reas de interÃ©s (AOI), definiciÃ³n de instrucciones y asignaciÃ³n de prioridades.
2. **Ciclo de Vida de Tareas (Mapeo y ValidaciÃ³n):** LÃ³gica de bloqueo concurrente de tareas, cambios de estado y gestiÃ³n de polÃ­gonos.
3. **Usuarios, Roles y Permisos:** Niveles de acceso (Principiante, Intermedio, Avanzado), control de acceso basado en roles (RBAC) y autenticaciÃ³n OAuth 2.0 con OpenStreetMap.
4. **Comunicaciones y EstadÃ­sticas:** MensajerÃ­a interna, notificaciones, e integraciÃ³n de mÃ©tricas (Ohsome API).

## 4. Objetivos del Plan General de Pruebas
1. Garantizar que la migraciÃ³n e implementaciÃ³n de la API en **FastAPI** cumple con los estÃ¡ndares de seguridad y lÃ³gica espacial requeridos.
2. Validar que la concurrencia masiva no genere condiciones de carrera (Race Conditions) al bloquear o liberar tareas cartogrÃ¡ficas.
3. Establecer un marco de trazabilidad documental total utilizando el estÃ¡ndar **ISO/IEC/IEEE 29119**, conectando el diseÃ±o de pruebas directamente con el cÃ³digo fuente del repositorio.

## 5. Alcance del Testing
Este Plan General cubre el aseguramiento de la calidad mediante pruebas dinÃ¡micas.

**Dentro del Alcance (In-Scope):**
*   Pruebas Unitarias de Backend (FastAPI, LÃ³gica de servicios, DTOs).
*   Pruebas de IntegraciÃ³n (API REST y Base de Datos PostGIS).
*   Pruebas de Sistema y Funcionales End-to-End (E2E) simulando los flujos de Mapeadores y Validadores.

**Fuera del Alcance (Out-of-Scope):**
*   Pruebas de la API externa de OpenStreetMap (estÃ¡ fuera de nuestro control).
*   Pruebas de EstrÃ©s y Carga masiva (serÃ¡n abordadas en un plan de operaciones paralelo, a menos que el alcance cambie).

## 6. Estructura de Niveles de Prueba
Para cumplir con el ciclo de vida del estÃ¡ndar, el proyecto se dividirÃ¡ en las siguientes fases (Sub-planes):
1. **Fase 1: Pruebas Unitarias** (Foco en el cÃ³digo Backend - Servicios, Modelos y Seguridad).
2. **Fase 2: Pruebas de IntegraciÃ³n** (InteracciÃ³n entre la capa FastAPI y PostGIS).
3. **Fase 3: Pruebas de Sistema** (ValidaciÃ³n funcional de la UI interactuando con la API).
4. **Fase 4: Pruebas de AceptaciÃ³n** (ValidaciÃ³n de flujos cartogrÃ¡ficos con usuarios finales).

## 7. Supuestos, Restricciones y Riesgos
*   **Supuestos:** El equipo de desarrollo mantendrÃ¡ actualizado el archivo `README.md` y la documentaciÃ³n tÃ©cnica de despliegue con Docker para facilitar la creaciÃ³n de los entornos de prueba.
*   **Restricciones:** El testing espacial (ValidaciÃ³n de geometrÃ­as PostGIS) requerirÃ¡ datos mokeados (mock data) de alta precisiÃ³n que deben ser diseÃ±ados previamente.
*   **Riesgos Globales:**
    *   *Riesgo:* Cambios abruptos en las APIs externas (OSM, Ohsome) pueden romper las pruebas de integraciÃ³n. 
    *   *MitigaciÃ³n:* Implementar contratos de prueba (Contract Testing) y uso extensivo de Mocks durante las Fases 1 y 2.


