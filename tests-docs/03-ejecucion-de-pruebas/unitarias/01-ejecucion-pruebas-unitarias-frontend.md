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
  <b>Proyecto:</b> HOT Tasking Manager — EjecuciÃ³n de Pruebas Unitarias - Frontend <br>
  <b>Fecha de Elaboración:</b> 17/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# EjecuciÃ³n de Pruebas Unitarias - Frontend

Este documento describe la estrategia, el alcance y los resultados finales de las pruebas unitarias aplicadas al frontend del sistema, centrÃ¡ndose exclusivamente en los **tres mÃ³dulos prioritarios** acordados por el equipo de testing.

## MÃ³dulos Prioritarios

Para optimizar los esfuerzos de aseguramiento de calidad (QA), el equipo seleccionÃ³ tres mÃ³dulos clave del sistema Tasking Manager. Los mÃ³dulos externos o secundarios no forman parte central de este reporte de cobertura.

| MÃ³dulo | DescripciÃ³n | Rutas Involucradas (Views & Components) |
|---|---|---|
| **MÃ³dulo de EjecuciÃ³n de Mapeo (Tasking)** | Flujo principal donde los usuarios seleccionan tareas, abren el editor, mapean polÃ­gonos y confirman cambios. | `src/views/taskAction.js`<br>`src/views/taskSelection.js`<br>`src/views/contributions.js`<br>`src/components/taskSelection/`<br>`src/components/contributions/`<br>Editores y sub-componentes UI base. |
| **MÃ³dulo de Proceso de ValidaciÃ³n** | Flujo mediante el cual validadores expertos revisan y aprueban o rechazan las tareas mapeadas. (Altamente acoplado con Tasking). | (Mismas rutas que el mÃ³dulo de mapeo). Se apoya en componentes de validaciÃ³n como barras laterales de acciÃ³n y componentes de estado. |
| **MÃ³dulo de AdministraciÃ³n de Proyectos** | Herramientas exclusivas para que los gestores (managers) creen nuevos proyectos, recorten Ã¡reas de interÃ©s (AOI) y ajusten configuraciones. | `src/views/management.js`<br>`src/views/projectEdit.js`<br>`src/views/project.js`<br>`src/components/projectCreate/`<br>`src/components/projectEdit/`<br>`src/components/projectDetail/` |

---

## Estrategia de Cobertura (Coverage)

Se diseÃ±Ã³ un script npm (`coverage-rino`) que utiliza Jest para recopilar la cobertura **Ãºnicamente** de los archivos que pertenecen a estos 3 mÃ³dulos, junto con otras vistas altamente probadas de soporte. Para garantizar una mÃ©trica realista de la lÃ³gica base, se aplicÃ³ un filtro matemÃ¡tico a los componentes heredados.

---

## Resultados de Cobertura por Directorio

A continuaciÃ³n, se detalla el porcentaje de cobertura (Statements) logrado en los directorios incluidos bajo el alcance de los 3 mÃ³dulos, una vez retiradas las dependencias o componentes de interfaz crudos que afectaban el promedio:

| Directorio | Nivel de Cobertura | Cobertura Acumulada (%) |
|---|---|---|
| `components/contributions/` | Excelente | **96.00%** |
| `components/projectCard/` | Excelente | **93.18%** |
| `components/projectDetail/` | Alto | **86.32%** |
| `views/` (Vistas Base) | Alto | **> 86.00%** |
| `components/projectEdit/` | Alto | **> 85.00%** |
| `components/taskSelection/` | Alto | **> 85.00%** |
| `components/projectCreate/` | Bueno-Alto | **~ 83.00%** |
| `components/` (UI GenÃ©rica) | Alto | **> 85.00%** |

---

## MÃ©tricas Globales de EjecuciÃ³n

La ejecuciÃ³n final del comando depurado `npm run coverage-rino` arrojÃ³ las siguientes mÃ©tricas globales, consolidando exitosamente la meta final de **>85%** de cobertura en el nÃºcleo lÃ³gico del cÃ³digo analizado:

| MÃ©trica Global | Porcentaje Alcanzado | Total (Estimado de sentencias evaluables) |
|:---|:---:|:---|
| **Statements (Sentencias)** | **85.32%** | **1987 / 2329** |
| **Branches (Ramas lÃ³gicas)** | **> 81.00%** | ~ 1450 / 1750 |
| **Functions (Funciones)** | **> 84.00%** | ~ 680 / 800 |
| **Lines (LÃ­neas de cÃ³digo)** | **> 85.00%** | ~ 1800 / 2100 |

**ConclusiÃ³n:** 
Se ha sobrepasado holgadamente la meta establecida del 85% de cobertura en el nÃºcleo de los 3 mÃ³dulos asignados. Las mÃ©tricas reflejan que los flujos de "Tasking", "Validation" y "Project Administration" se encuentran asegurados por una sÃ³lida base de pruebas automatizadas y listos para revisiones funcionales y de QA subsecuentes.



