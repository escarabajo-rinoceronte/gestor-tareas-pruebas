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
  <b>Proyecto:</b> HOT Tasking Manager — Plan General de Pruebas: GestiÃ³n de Riesgos <br>
  <b>Fecha de Elaboración:</b> 11/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

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


