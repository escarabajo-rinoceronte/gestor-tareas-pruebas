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
  <b>Proyecto:</b> HOT Tasking Manager — Informe de Ejecución y Análisis de Pruebas Unitarias - Core Module <br>
  <b>Fecha de Elaboración:</b> 24/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Informe de Ejecución y Análisis de Pruebas Unitarias - Core Module

## 1. Resumen del Proceso Realizado

El presente proceso tuvo como objetivo principal la estabilización y análisis de cobertura de la suite de pruebas unitarias correspondiente al **Módulo de Servicios Core y Lógica de Negocio**. Tras alinear el diseño con la arquitectura real de los servicios (descartando dependencias de modelos PostGIS y comunicación que pertenecen a otros dominios), se evaluaron los servicios transaccionales críticos responsables de proyectos, mapeos, validaciones, divisiones de cuadrículas, campañas y organizaciones.

**Hitos del proceso:**
1.  **Alineación del Dominio:** Se reestructuró la ejecución para medir de forma aislada los componentes estipulados en la fase de análisis estructural (`backend/services/*.py` excluyendo comunicación/usuarios).
2.  **Estabilización de Infraestructura de Tests:** Corrección de fallos en los *fixtures* y ejecución bajo el framework asíncrono (`pytest` + `asyncio`).
3.  **Auditoría de Cobertura Base:** Extracción de las métricas reales que evidencian el estado actual del núcleo del sistema, exponiendo la necesidad de campañas TDD futuras.

---

## 2. Estado Final de la Ejecución de Pruebas

El entorno local fue estabilizado exitosamente, eliminando cualquier error de infraestructura (500s, fallos de inyección de DB temporal). 

### Resumen de Ejecución de Suites Unitarias (Servicios Core)
| Métrica | Resultado |
| :--- | :--- |
| **Pruebas Recolectadas** | 88 |
| **Pruebas Exitosas (Passed)** | 88 |
| **Fallos Pendientes (Failures)** | 0 |
| **Errores de Ejecución (Errors)** | 0 |
| **Tiempo de Ejecución** | ~14.48s |

*Nota: La ejecución limpia (0 fallos) garantiza que los caminos felices actualmente automatizados funcionan correctamente. Sin embargo, el análisis de cobertura revelará una baja penetración en escenarios borde.*

---

## 3. Análisis de Cobertura

La cobertura se obtuvo mediante el uso de `pytest-cov`, generando un reporte detallado que evalúa la ejecución de cada línea de código dentro de los servicios evaluados. 

**Resultados Consolidados del Módulo:**
| Métrica | Resultado |
| :--- | :--- |
| **Líneas ejecutables totales (Stmts)** | 2319 |
| **Líneas no cubiertas (Miss)** | 1105 |
| **Cobertura Global del Core Module** | **52%** |

---

## 4. Archivos Analizados y Pruebas Implementadas

El desglose de la cobertura expone disparidades críticas entre los servicios. El motor geométrico (`split_service.py`) y las validaciones de mapping (`mapping_service.py`) mantienen los índices más aceptables del dominio, mientras que las lógicas auxiliares presentan deficiencias sustanciales.

| Componente | Líneas (Stmts) | Faltantes (Miss) | Cobertura Final |
| :--- | :---: | :---: | :---: |
| `grid/split_service.py` | 130 | 30 | 77% |
| `mapping_service.py` | 215 | 60 | 72% |
| `organisation_service.py` | 195 | 82 | 58% |
| `campaign_service.py` | 172 | 76 | 56% |
| `project_admin_service.py` | 194 | 101 | 48% |
| `project_service.py` | 368 | 193 | 48% |
| `validator_service.py` | 233 | 120 | 48% |
| `project_search_service.py` | 424 | 231 | 46% |
| `team_service.py` | 388 | 212 | 45% |

---

## 5. Análisis Técnico y Fallos Potenciales

El alto porcentaje de líneas no cubiertas (1105) en un módulo tan sensible como los **Servicios Core** representa un riesgo operacional elevado, ya que los controladores HTTP delegan toda la lógica de negocio en estos archivos. 

**Análisis de Vacíos de Cobertura:**
1.  **Lógica Condicional (If/Else):** Los bloques no cubiertos en `project_service.py` y `team_service.py` corresponden casi en su totalidad a excepciones HTTP no lanzadas durante las pruebas unitarias (ej., verificaciones de permisos cuando el usuario no es *Manager*).
2.  **Validaciones Transaccionales:** Gran parte de las sentencias omitidas en `validator_service.py` y `mapping_service.py` son bifurcaciones para rollback de transacciones en escenarios de concurrencia forzada.

---

## 6. Recomendaciones y Siguientes Pasos

Se sugiere al equipo de Aseguramiento de Calidad tomar acciones inmediatas en la siguiente iteración (Fase de Implementación TDD) sobre los hallazgos:

1.  **Priorización de Diseños:** Expandir las especificaciones en `02-servicios-core-negocio.md` para focalizarse intensivamente en `project_service.py` y `validator_service.py`, debido a su baja métrica actual (~48%) y su alta criticidad.
2.  **Simulación de Errores de BD:** Incrementar el uso de Mocks de la base de datos (e.g. `unittest.mock.patch`) para simular `IntegrityError` y forzar al backend a ejecutar los flujos de *rollback*, cubriendo las líneas residuales.
3.  **Evaluación de Seguridad (RBAC):** Diseñar aserciones específicas para roles no autorizados, forzando y capturando excepciones 403 Forbidden dentro de los servicios.

---

## 7. Conclusiones

La auditoría y validación documental del módulo Core fue exitosa al revelar la cobertura técnica auténtica del sistema, disipando asunciones previas. La suite unitaria es completamente funcional y asíncrona, demorando apenas 14 segundos en procesar 88 integraciones complejas con *fixtures*. 

A pesar de que el **52%** de cobertura general indica que la plataforma no está lista para un proceso de certificación ISO de alta rigurosidad, establece una métrica de referencia transparente (Línea Base) sobre la cual los Test Designers pueden trabajar ordenadamente hacia el umbral deseado del >85%.
