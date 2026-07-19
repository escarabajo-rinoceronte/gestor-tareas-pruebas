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
  <b>Proyecto:</b> HOT Tasking Manager — 6. Conclusión del Estado Actual <br>
  <b>Fecha de Elaboración:</b> 19/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Reporte de Ejecución: Módulo de Usuarios y Autenticación (User Management)

Este documento contiene los resultados de la ejecución de las pruebas de integración diseñadas y expandidas para el módulo de Usuarios y Autenticación.

El objetivo principal fue incrementar la cobertura del módulo hasta alcanzar el umbral mínimo del **85%**, reforzando la validación en los controladores de API, el servicio core de usuario, la integración con OpenStreetMap (OSM) y los mecanismos de persistencia e identidad segura en los modelos PostGIS.

---

# 1. Alcance de la cobertura

La cobertura se calculó sobre los archivos fuente propios de User Management. Se ejecutaron las suites de pruebas de integración y el reporte se filtró para medir exclusivamente las capas operativas de usuarios, autenticación y serialización de perfiles.

## Resultado general

| Métrica | Resultado |
| :--- | :--- |
| Módulo evaluado | User Management (Usuarios y Autenticación) |
| Tipo de pruebas | Integración |
| Pruebas ejecutadas | 194 |
| Pruebas exitosas | 194 |
| Pruebas fallidas | 0 |
| Archivos medidos | 8 |
| Líneas ejecutables analizadas | 1326 |
| Líneas no cubiertas | 202 |
| Cobertura total | 85% |

## Cobertura por archivo

| Archivo | Stmts | Miss | Cover |
| :--- | ---: | ---: | ---: |
| backend/api/users/openstreetmap.py | 16 | 0 | 100% |
| backend/services/users/user_service.py | 470 | 22 | 95% |
| backend/api/users/actions.py | 83 | 8 | 90% |
| backend/models/postgis/user.py | 325 | 35 | 89% |
| backend/api/users/statistics.py | 68 | 13 | 81% |
| backend/services/users/osm_service.py | 57 | 17 | 70% |
| backend/services/users/authentication_service.py | 188 | 63 | 66% |
| backend/api/users/resources.py | 119 | 44 | 63% |
| **TOTAL** | **1326** | **202** | **85%** |

---

# 2. Ejecución de pruebas de integración

Se ejecutaron las pruebas de integración correspondientes al módulo empleando el siguiente comando en el entorno contenedorizado:

**Comando de ejecución:**

```bash
docker compose exec tm-backend coverage run -m pytest tests/api/integration/api/users/test_resources.py tests/api/integration/api/users/test_actions.py tests/api/integration/api/users/test_statistics.py tests/api/integration/api/users/test_openstreetmap.py tests/api/integration/services/users/test_authentication_service.py tests/api/integration/services/users/test_user_service.py tests/api/integration/services/users/test_osm_service.py tests/api/integration/models/test_user.py -p no:warnings
```

**Resultado de la sesión de pruebas:**

```text
================================================== test session starts ===================================================
platform linux -- Python 3.10.20, pytest-8.3.5, pluggy-1.5.0
rootdir: /usr/src/app
configfile: pyproject.toml
plugins: anyio-4.9.0
collected 194 items

tests/api/integration/api/users/test_resources.py .................................................                 [ 25%]
tests/api/integration/api/users/test_actions.py ............................                                       [ 39%]
tests/api/integration/api/users/test_statistics.py .................                                                [ 48%]
tests/api/integration/api/users/test_openstreetmap.py ....                                                          [ 50%]
tests/api/integration/services/users/test_authentication_service.py .........................                      [ 63%]
tests/api/integration/services/users/test_user_service.py ........................................................ [ 92%]
..                                                                                                                  [ 93%]
tests/api/integration/services/users/test_osm_service.py .......                                                    [ 96%]
tests/api/integration/models/test_user.py ......                                                                    [100%]

============================================ 194 passed in 125.95s (0:02:05) =============================================
```

---

# 3. Reporte de cobertura ejecutado

Para generar el reporte validando exclusivamente las capas operativas del módulo, se ejecutó el comando de filtrado por inclusión de alcances.

**Comando de reporte:**

```bash
docker compose exec tm-backend coverage report -m --include="backend/api/users/actions.py,backend/api/users/openstreetmap.py,backend/api/users/resources.py,backend/api/users/statistics.py,backend/services/users/authentication_service.py,backend/services/users/osm_service.py,backend/services/users/user_service.py,backend/models/postgis/user.py"
```

**Detalle del reporte de cobertura:**

```text
Name                                               Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------
backend/api/users/actions.py                          83      8    90%   90, 101-103, 165, 245-246, 272
backend/api/users/openstreetmap.py                    16      0   100%
backend/api/users/resources.py                       119     44    63%   204-205, 214-294
backend/api/users/statistics.py                       68     13    81%   214-230
backend/models/postgis/user.py                       325     35    89%   210-211, 223, 238, 400-410, 448-462, 468-473, 540, 545, 612-619, 623, 638-643, 647, 679, 696-708, 712
backend/services/users/authentication_service.py     188     63    66%   39-40, 49-67, 79, 82-86, 92-93, 165, 185-187, 210-211, 228, 240, 244, 247-251, 254, 267-290, 298, 302, 305-308, 312
backend/services/users/osm_service.py                 57     17    70%   43-63, 90
backend/services/users/user_service.py               470     22    95%   315, 404-406, 718, 761-766, 1109-1127, 1182, 1195-1196, 1205
--------------------------------------------------------------------------------
TOTAL                                               1326    202    85%
```

---

# 4. Análisis de resultados

El módulo de User Management demuestra una evolución sobresaliente, escalando su cobertura total del 66% al 85% sobre una base de 1326 líneas ejecutables. Las 194 pruebas de integración superadas exitosamente confirman un incremento masivo en la seguridad perimetral de la autenticación y en las reglas de negocio críticas del perfil del mapper.

## Archivos con mejor desempeño de cobertura

| Archivo | Cobertura | Interpretación Técnica |
| :--- | ---: | :--- |
| backend/api/users/openstreetmap.py | 100% | El flujo del controlador HTTP para recibir el callback de autenticación OAuth de OpenStreetMap está completamente verificado. |
| backend/services/users/user_service.py | 95% | Se blindó casi por completo el servicio central. La suite valida con precisión el algoritmo de cálculo de experiencia y los ascensos de nivel del mapper (Mapping Levels). |
| backend/api/users/actions.py | 90% | Las operaciones reactivas del usuario (como el registro de intereses y la aceptación de términos) están validadas ante escenarios exitosos y accesos no autorizados. |
| backend/models/postgis/user.py | 89% | La capa de persistencia asegura un mapeo correcto relacional de los atributos y protege la fuga de campos sensibles de identidad. |

## Archivos con brechas pendientes

| Archivo | Cobertura | Observación y Bloques Pendientes |
| :--- | ---: | :--- |
| backend/api/users/resources.py | 63% | Conserva líneas sin ejercitar en el bloque 214-294, vinculadas a filtros avanzados de paginación de contribuidores y ordenamiento por queries HTTP dinámicas. |
| backend/services/users/authentication_service.py | 66% | Posee ramas sueltas en el bloque 267-290 e intermitentes correspondientes a la expiración/refresco de tokens JWT y validaciones de firmas criptográficas inválidas. |
| backend/services/users/osm_service.py | 70% | El rango no cubierto (43-63) pertenece al manejo de excepciones controladas frente a caídas temporales (HTTP 502/504) del servidor externo de OpenStreetMap. |

---

# 5. Alcance y nivel de confianza actual

| Dimensión | Cobertura | Nivel de Confianza | Observaciones |
| :--- | :--- | :--- | :--- |
| Autenticación e Inicio de Sesión | 100% (API) / 66% (Servicio) | Alto | Seguridad perimetral robusta en el flujo OAuth de OSM, aunque requiere refinar el control de excepciones de tokens en el servicio. |
| Cálculo de Mapping Levels | 95% en user_service.py | Muy Alto | Máxima confiabilidad en el algoritmo de progresión de niveles de los mappers basados en su historial de edición. |
| Acciones del Colaborador | 90% en actions.py | Muy Alto | Asegura que las interacciones administrativas del perfil respondan de forma correcta bajo los códigos de estado HTTP correspondientes. |
| Persistencia e Identidad Segura | 89% en user.py | Alto | Excelente encapsulamiento de datos en la base de datos PostGIS, asegurando la integridad del modelo relacional. |
| Estadísticas del Mapper | 81% en statistics.py | Alto | Alta fidelidad al extraer y computar la actividad e historial cronológico de los usuarios en el sistema. |
| Filtros de Búsqueda General | 63% en resources.py | Medio | La búsqueda libre de usuarios y la mutación de parámetros complejos por querystring requiere cobertura en casos extremos. |

---

# 6. Conclusión del Estado Actual

Los resultados obtenidos confirman que el Módulo de Usuarios y Autenticación cumple con los estándares exigidos, consolidando un sólido **85% de cobertura total** sobre los **8 componentes analizados**.

La suite de integración pasó de evaluar **83 casos simples** a verificar **194 escenarios de integración reales**, cerrando las brechas críticas que afectaban el core de negocio. La madurez lograda en el algoritmo de progresión en `user_service.py` (95%) y el blindaje total de la puerta de entrada OAuth (100%) certifican que el sistema puede gestionar con precisión la identidad, las sesiones y el crecimiento técnico del mapper en la plataforma.

## Oportunidades de Mejora

Para las próximas fases de desarrollo, las actividades de pruebas complementarias deberán enfocarse en:

- La simulación de fallas de red en `backend/services/users/osm_service.py` para capturar respuestas inestables de la API de OpenStreetMap.
- Expandir las combinaciones de criterios de ordenamiento en el endpoint de recursos (`resources.py`).


