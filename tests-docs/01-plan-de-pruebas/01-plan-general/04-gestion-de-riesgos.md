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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — Plan General de Pruebas: GestiÃ³n de Riesgos</td></tr>
      <tr><td class="label">Fecha</td><td>11/06/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# Plan General de Pruebas: GestiÃ³n de Riesgos

**Proyecto:** HOT OSM Tasking Manager  
**EstÃ¡ndar de Referencia:** ISO/IEC/IEEE 29119-2 (Proceso de GestiÃ³n de Riesgos de Pruebas)  

## 1. MetodologÃ­a de AnÃ¡lisis de Riesgos
La identificaciÃ³n y tratamiento de riesgos se evalÃºa en base a su **Probabilidad de Ocurrencia** (Baja, Media, Alta) y su **Impacto en la Calidad/Cronograma** (Bajo, Medio, CrÃ­tico). Todo riesgo con una valoraciÃ³n combinada "Alta-CrÃ­tica" requiere una estrategia de mitigaciÃ³n de ejecuciÃ³n obligatoria.

## 2. Matriz de Riesgos TÃ©cnicos y ArquitectÃ³nicos
Estos riesgos estÃ¡n directamente vinculados con el SUT (System Under Test) y las tecnologÃ­as empleadas.

| ID | Riesgo Identificado | Probabilidad | Impacto | Estrategia de MitigaciÃ³n y Contingencia |
| :--- | :--- | :--- | :--- | :--- |
| **RT-01** | **Bloqueo por APIs Externas:** La API de OpenStreetMap (OSM) rechaza peticiones del pipeline CI/CD debido a *rate limits*, haciendo fallar pruebas vÃ¡lidas. | Alta | CrÃ­tico | **MitigaciÃ³n:** Desacoplar pruebas unitarias usando *Mocks* obligatorios. <br>**Contingencia:** Proveer un servidor de pruebas OSM en Docker (vÃ­a `osm-seed`) si fuera estrictamente necesario. |
| **RT-02** | **Falsos Positivos en GeometrÃ­as:** Las aserciones sobre cÃ¡lculos espaciales (PostGIS) fallan en CI/CD debido a diferencias de precisiÃ³n de punto flotante entre SOs locales y servidores GitHub. | Media | Medio | **MitigaciÃ³n:** Estandarizar tolerancias de error (`delta`) en las aserciones numÃ©ricas espaciales de `pytest`. |


## 3. Matriz de Riesgos Organizacionales y de Proyecto
Estos riesgos contemplan las dinÃ¡micas del equipo de QA, la estructura del proyecto Open Source (HOTOSM) y la planificaciÃ³n.

| ID | Riesgo Identificado | Probabilidad | Impacto | Estrategia de MitigaciÃ³n y Contingencia |
| :--- | :--- | :--- | :--- | :--- |
| **RO-01** | **Cuello de Botella Documental:** Test Lead se convierte en el Ãºnico revisor de la Wiki, generando retrasos en la etapa de DiseÃ±o de pruebas de los demÃ¡s roles. | Media | Alto | **MitigaciÃ³n:** Establecer SLAs internos (por ejemplo, mÃ¡ximo 24 horas para revisiÃ³n de PRs en la Wiki). Si la carga es muy alta, Test Analyst y Test Design asume el rol de revisor de respaldo (Back-up Reviewer). |
| **RO-02** | **Curva de Aprendizaje del Equipo:** Los nuevos integrantes que se sumarÃ¡n en las siguientes tareas de QA carecen de contexto tÃ©cnico de la API, afectando la calidad de las pruebas E2E. | Alta | Medio | **MitigaciÃ³n:** Asegurar que los repositorios `qa-gestion` y `producto-docs` estÃ©n 100% finalizados y auditados antes de la incorporaciÃ³n del equipo completo, sirviendo como material de onboarding autogestionado. |

## 4. Plan de Seguimiento de Riesgos
Esta matriz no es estÃ¡tica. Test Lead es el responsable de monitorear el estado de estos riesgos y agregar nuevos hallazgos durante las sesiones de evaluaciÃ³n que se realizarÃ¡n al finalizar cada iteraciÃ³n o sprint de pruebas.

