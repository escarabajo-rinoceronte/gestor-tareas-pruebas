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
  <b>Proyecto:</b> HOT Tasking Manager — Informe de EjecuciÃ³n y AnÃ¡lisis de Pruebas Unitarias - Core Module <br>
  <b>Fecha de Elaboración:</b> 24/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Informe de EjecuciÃ³n y AnÃ¡lisis de Pruebas Unitarias - Core Module

## 1. Resumen del Proceso Realizado
El presente proceso tuvo como objetivo principal el fortalecimiento de la calidad del software del **Tasking Manager** mediante la estabilizaciÃ³n, implementaciÃ³n y optimizaciÃ³n de la suite de pruebas unitarias. La estrategia se centrÃ³ en el **MÃ³dulo Core** (Modelos PostGIS y Servicios de Negocio), identificando inicialmente una brecha de cobertura significativa y errores de ejecuciÃ³n crÃ­ticos derivados de la migraciÃ³n tecnolÃ³gica a entornos asÃ­ncronos (`pytest` + `asyncio`).

**Hitos del proceso:**
1.  **EstabilizaciÃ³n de Infraestructura de Tests:** CorrecciÃ³n de fallos en los *fixtures* y *helpers* para garantizar la integridad referencial en la base de datos de pruebas.
2.  **Incremento de Cobertura:** ImplementaciÃ³n de casos de prueba para archivos con cobertura nula (0%) o crÃ­tica (<30%).
3.  **AnÃ¡lisis de Defectos:** DetecciÃ³n de errores lÃ³gicos y bugs en el backend a travÃ©s de la ejecuciÃ³n de pruebas de borde.
4.  **RefactorizaciÃ³n de Pruebas:** MigraciÃ³n de lÃ³gica de inserciÃ³n manual a patrones de diseÃ±o basados en objetos para asegurar la mantenibilidad.

---

## 2. Estado Final de la EjecuciÃ³n de Pruebas
Tras las intervenciones realizadas, se logrÃ³ pasar de un entorno con mÃºltiples errores de ejecuciÃ³n (`errors`) a una suite de pruebas estable y funcional.

### Resumen de EjecuciÃ³n (Final)
| MÃ©trica | Resultado |
| :--- | :--- |
| **Pruebas Recolectadas** | 270 |
| **Pruebas Exitosas (Passed)** | 263 |
| **Fallos Pendientes (Failures)** | 7 |
| **Errores de EjecuciÃ³n (Errors)** | 0 |
| **Tiempo de EjecuciÃ³n** | ~40.24s |

*Nota: Los 7 fallos restantes corresponden a discrepancias identificadas entre la lÃ³gica esperada y la implementaciÃ³n actual del backend, las cuales han sido documentadas como recomendaciones tÃ©cnicas para el equipo de desarrollo.*

---

## 3. AnÃ¡lisis de Cobertura
La cobertura se obtuvo mediante el uso de `pytest-cov`, generando un reporte detallado que evalÃºa la ejecuciÃ³n de cada lÃ­nea de cÃ³digo en el directorio `backend/`. 

**Resultados por MÃ³dulo CrÃ­tico:**
| MÃ³dulo / Carpeta | Cobertura Promedio | Estado |
| :--- | :---: | :--- |
| `backend/models/postgis/` | ~88% | **Objetivo Alcanzado** |
| `backend/services/` | ~84% | **En Mejora** |
| **MÃ³dulo Core (Consolidado)** | **~86%** | **Certificado** |

> [!NOTE]
> Sobre el Reporte HTML:** El reporte detallado muestra que los archivos de lÃ³gica pura (como `tags.py` y `task_annotation.py`) han alcanzado el **100% de cobertura**, mientras que los archivos de integraciÃ³n externa (como `mapswipe_service.py`) se mantienen en un rango menor debido a la necesidad de mocks de red complejos.

---

## 4. Archivos Analizados y Pruebas Implementadas

Se priorizaron los archivos del nÃºcleo que presentaban mayor riesgo tÃ©cnico debido a su baja cobertura inicial.

| Archivo | Cobertura Inicial | Cobertura Final (Est.) | Casos de Prueba Implementados / Corregidos |
| :--- | :---: | :---: | :--- |
| `postgis/tags.py` | 0% | 100% | CreaciÃ³n, recuperaciÃ³n y validaciÃ³n de unicidad de etiquetas. |
| `postgis/project.py` | 38% | 49% | Ciclo de vida de favoritos, destacados y borrado fÃ­sico. |
| `grid/split_service.py` | 22% | 77% | DivisiÃ³n geomÃ©trica, validaciÃ³n de candados y limpieza de registros. |
| `postgis/task_annotation.py` | 46% | 100% | Constructor, recuperaciÃ³n por tipo y conversiÃ³n a DTO. |
| `messaging/chat_service.py` | 35% | 92% | Permisos en proyectos privados y saneamiento de Markdown. |
| `messaging/message_service.py` | 44% | 44%* | ValidaciÃ³n de preferencias de usuario y parseo de menciones. |

*\*Nota: En `message_service.py` se agregaron pruebas crÃ­ticas, pero el volumen de lÃ­neas del archivo requiere mÃ¡s casos para mover el porcentaje global significativamente.*

---

## 5. Fallos Detectados y AnÃ¡lisis de Causa RaÃ­z
Durante la ejecuciÃ³n, se identificaron problemas que impidieron el Ã©xito de ciertos tests, clasificados a continuaciÃ³n:

| Archivo / Fallo | Causa RaÃ­z | AnÃ¡lisis TÃ©cnico |
| :--- | :--- | :--- |
| `task_annotation.py` | `AttributeError: get` | El backend intenta usar `.get()` en un objeto `Record` de `databases`, el cual es inmutable y solo soporta acceso por llaves `[]`. |
| `split_service.py` | `ForeignKeyViolationError` | El mÃ©todo de borrado de tareas no limpiaba las anotaciones de tareas, rompiendo la integridad referencial de la BD. |
| `chat_service.py` | `TypeError` en DTO | El `__init__` manual del DTO bloquea la instanciaciÃ³n estÃ¡ndar de Pydantic v2. |
| `project.py` | `NotNullViolation` | OmisiÃ³n de campos de auditorÃ­a (`created`, `last_updated`) en inserciones manuales de SQL crudo. |

---

## 6. Recomendaciones para el Equipo de Desarrollo
Se sugiere al equipo de desarrollo del backend revisar los siguientes hallazgos para mejorar la robustez del sistema:

1.  **RefactorizaciÃ³n de `task_annotation.py`:** Cambiar el acceso a los registros de base de datos. Se recomienda convertir los objetos `Record` a `dict` inmediatamente despuÃ©s de la consulta para permitir el uso de mÃ©todos como `.get()` y asegurar la mutabilidad de los datos antes de procesar el JSON.
2.  **Integridad en Cascada en `split_service.py`:** El mÃ©todo `delete_task_and_related_records` debe ser actualizado para incluir la eliminaciÃ³n de `task_annotations`. Actualmente, el sistema falla al intentar dividir tareas que contienen metadatos de IA.
3.  **EstandarizaciÃ³n de Fechas:** Se detectÃ³ que el backend es sensible a objetos `datetime` con zona horaria (offset-aware). Se recomienda estandarizar el uso de `datetime.utcnow()` o asegurar que el esquema de la base de datos sea `TIMESTAMP WITH TIME ZONE`.
4.  **ActualizaciÃ³n de DTOs:** Remover los constructores `__init__` manuales en los DTOs de `message_dto.py` para permitir que Pydantic maneje la validaciÃ³n y el mapeo de campos de forma nativa.

---

## 7. Conclusiones
El proceso de testing ha sido exitoso en la **estabilizaciÃ³n del entorno local** y en la **identificaciÃ³n de bugs crÃ­ticos** que podrÃ­an haber afectado la integridad de los datos en producciÃ³n. Con una cobertura consolidada del **86% en el Core Module**, el proyecto cuenta ahora con una base sÃ³lida para recibir nuevas funcionalidades. Se recomienda como prÃ³ximo paso enfocarse en la cobertura de los controladores de la API (capa de recursos) para alcanzar el 85% de cobertura total en todo el repositorio.



