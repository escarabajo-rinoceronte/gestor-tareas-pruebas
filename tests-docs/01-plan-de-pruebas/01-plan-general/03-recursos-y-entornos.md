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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — Plan General de Pruebas: Recursos y Entornos</td></tr>
      <tr><td class="label">Fecha</td><td>11/06/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# Plan General de Pruebas: Recursos y Entornos

**Proyecto:** HOT OSM Tasking Manager  
**EstÃ¡ndar de Referencia:** ISO/IEC/IEEE 29119-3 (EspecificaciÃ³n del Entorno de Pruebas)  

## 1. Arquitectura de los Entornos de Pruebas
Para garantizar el aislamiento y la repetibilidad de los resultados, el aseguramiento de calidad del Tasking Manager exige el uso de entornos encapsulados mediante contenedores, dada la complejidad de sus dependencias espaciales.

![Recursos y entornos](/tests-docs/01-plan-de-pruebas/01-plan-general/img/recursos-entornos.png) 

*(PropÃ³sito del diagrama: Aclarar la separaciÃ³n de responsabilidades operativas. Las pruebas unitarias ocurren entre Local y CI; las pruebas de Sistema ocurrirÃ¡n en Staging).*

## 2. Requerimientos de Infraestructura y Herramientas QA
El stack tecnolÃ³gico de pruebas ha sido estandarizado para todo el equipo:

### 2.1. Frameworks de EjecuciÃ³n
*   **Backend (Python/FastAPI):** `pytest` como framework principal de aserciones. Uso intensivo de `unittest.mock` para aislar microservicios.
*   **Frontend (React):** `Jest` y `React Testing Library` para pruebas de componentes aislados.
*   **End-to-End (E2E):** `Cypress` (a implementar a partir de la Fase 3) para automatizar flujos de mapeo y validaciÃ³n en la UI.

### 2.2. Dependencias TÃ©cnicas y Entorno Local
*   **Motor de Base de Datos Temporal:** Cada ejecuciÃ³n de pruebas unitarias/integraciÃ³n del backend *debe* levantar una base de datos efÃ­mera de PostgreSQL con la extensiÃ³n **PostGIS**. EstÃ¡ estrictamente prohibido apuntar pruebas de escritura a bases de datos de desarrollo o producciÃ³n.
*   **Mocks de Servicios Externos:** Se requiere la configuraciÃ³n de servidores mock (ej. `WireMock` o librerÃ­as internas como `responses` en Python) para interceptar y simular respuestas de la API pÃºblica de **OpenStreetMap (OSM)** y **Ohsome**.

## 3. IntegraciÃ³n Continua (CI/CD)
El proyecto confÃ­a en **GitHub Actions** como orquestador de pruebas.
*   Todo *Pull Request* hacia la rama `develop` o dispararÃ¡ automÃ¡ticamente el *Test Pipeline*.
*   **Bloqueo de Merge:** Si el reporte de cobertura automatizado (generado por `coverage.py`) cae por debajo del umbral del 80%, el PR serÃ¡ bloqueado automÃ¡ticamente en GitHub.

## 4. Limitaciones TÃ©cnicas y Restricciones
*   **LÃ­mites de Tasa (Rate Limiting) de OSM:** Tasking Manager consume datos reales de OSM. Durante las pruebas E2E y de IntegraciÃ³n, el equipo QA debe tener cuidado de no ser baneado por exceder el *rate limit* de la API pÃºblica de OSM. El uso de *Mocks* es obligatorio en Fases 1 y 2.
*   **Datos Espaciales (Test Data):** La generaciÃ³n manual de polÃ­gonos GeoJSON (multipolygon) para pruebas es compleja. El equipo deberÃ¡ mantener un banco de datos estÃ¡ticos en `tests/fixtures/` con geometrÃ­as pre-validadas.

