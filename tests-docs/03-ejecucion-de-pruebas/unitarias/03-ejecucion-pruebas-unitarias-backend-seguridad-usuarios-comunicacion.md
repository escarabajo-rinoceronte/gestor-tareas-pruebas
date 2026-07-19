# UNIVERSIDAD NACIONAL DE SAN AGUSTÍN

## FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
### ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

<div align="center">
<img src="/tests-docs/img/logo-unsa.png" alt="Logo UNSA" width="200"/>
</div>

**Curso:** Pruebas de Software  
**Docente:** Ing. Robert Edison Arisaca Mamani  
**Semestre:** VII  
**Proyecto:** Reporte de Ejecución: Módulo de Seguridad, Usuarios y Comunicación  
**Fecha de Elaboración:** 24/06/2026  
**Lugar:** Arequipa – Perú

---

# Reporte de Ejecución: Módulo de Seguridad, Usuarios y Comunicación

Este documento presenta los resultados de la ejecución de las pruebas unitarias correspondientes al **módulo de Seguridad, Usuarios y Comunicación**. El objetivo principal fue evaluar el estado inicial de la cobertura de pruebas de los servicios relacionados con autenticación, gestión de usuarios, mensajería, plantillas de comunicación e integración con OpenStreetMap, tomando como línea base una cobertura del **30%**. A partir de la implementación de nuevas pruebas unitarias orientadas a cubrir flujos principales, casos límite y escenarios de error, se logró incrementar la cobertura hasta **82%**, estableciendo una base sólida para las siguientes fases del proceso de aseguramiento de la calidad del software.

---

# 1. Alcance de la cobertura

La cobertura se calculó sobre los archivos fuente correspondientes a los servicios de **Seguridad, Usuarios y Comunicación**. Las pruebas unitarias se ejecutaron utilizando *mocks* y *fixtures* para aislar los servicios de autenticación, mensajería, gestión de usuarios y comunicación.

## Resultado general

| Métrica | Resultado |
|----------|-----------|
| Módulo evaluado | Seguridad, Usuarios y Comunicación |
| Tipo de pruebas | Unitarias |
| Pruebas ejecutadas | 197 |
| Pruebas exitosas | 197 |
| Pruebas fallidas | 0 |
| Archivos medidos | 7 |
| Líneas ejecutables analizadas | 1467 |
| Líneas no cubiertas | 257 |
| Cobertura total | **82%** |

## Cobertura por archivo

| Archivo | Stmts | Miss | Cover |
|----------|------:|-----:|------:|
| `backend/services/messaging/chat_service.py` | 60 | 1 | 98% |
| `backend/services/messaging/message_service.py` | 537 | 114 | 79% |
| `backend/services/messaging/smtp_service.py` | 114 | 20 | 82% |
| `backend/services/messaging/template_service.py` | 41 | 6 | 85% |
| `backend/services/users/authentication_service.py` | 188 | 47 | 75% |
| `backend/services/users/osm_service.py` | 57 | 0 | 100% |
| `backend/services/users/user_service.py` | 470 | 69 | 85% |
| **TOTAL** | **1467** | **257** | **82%** |

---

# 2. Ejecución de pruebas unitarias

Para ejecutar las pruebas unitarias del módulo se utilizó el siguiente comando:

```sh
docker compose exec tm-backend coverage run -m pytest tests/api/unit/services/messaging/ tests/api/unit/services/users/ -p no:warnings -v
```

## Resultado de la ejecución

```text
WARN[0000] The "DEFAULT_VALIDATOR_TEAM_ID" variable is not set. Defaulting to a blank string.

================================================== test session starts ==================================================
platform linux -- Python 3.10.20, pytest-8.3.5, pluggy-1.5.0
rootdir: /usr/src/app
configfile: pyproject.toml
plugins: anyio-4.9.0

collected 197 items

tests/api/unit/services/messaging/test_chat_service.py ............... [  7%]
tests/api/unit/services/messaging/test_messaging_service.py .........  [ 24%]
tests/api/unit/services/messaging/test_smtp_service.py .............   [ 34%]
tests/api/unit/services/messaging/test_template_service.py ...         [ 36%]
tests/api/unit/services/users/test_authentication_service.py .....     [ 55%]
tests/api/unit/services/users/test_osm_service.py .........            [ 61%]
tests/api/unit/services/users/test_user_service.py ...............     [100%]

============================================= 197 passed in 90.60s =============================================
```

---

# 3. Reporte de cobertura ejecutado

Para generar el reporte de cobertura únicamente del módulo evaluado se ejecutó:

```sh
docker compose exec tm-backend coverage report -m --include="backend/services/messaging/*,backend/services/users/*"
```

## Resultado del reporte

```text
Name                                               Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------
backend/services/messaging/chat_service.py            60      1    98%   43
backend/services/messaging/message_service.py        537    114    79%   183, 191-241, 275, 330-340, 366-393, 623-649, 652-723, 789, 797-825, 831-834, 837-843, 971-972, 1020, 1048, 1080, 1083
backend/services/messaging/smtp_service.py           114     20    82%   95-141
backend/services/messaging/template_service.py        41      6    85%   28-30, 52-54
backend/services/users/authentication_service.py     188     47    75%   39-40, 49-67, 72-95, 248-249, 254, 275-277, 286, 305-306, 308, 312
backend/services/users/osm_service.py                 57      0   100%
backend/services/users/user_service.py               470     69    85%   205-214, 315, 404-406, 478, 481, 528, 530, 532, 534, 537, 578-693, 725, 733, 766, 826, 831-832, 971-972, 1004-1005, 1182, 1198-1205, 1209-1219
--------------------------------------------------------------------------------
TOTAL                                               1467    257    82%
```

---

# 4. Análisis de resultados

La auditoría evidencia una cobertura unitaria del **82%**, lo que representa una mejora de **52 puntos porcentuales** respecto al estado inicial de **30%**. Los **197 casos de prueba** finalizaron exitosamente, sin registrarse fallos durante la ejecución, lo que demuestra la estabilidad del módulo evaluado.

## Componentes con mayor cobertura

| Archivo | Cobertura | Interpretación |
|----------|----------:|----------------|
| `osm_service.py` | 100% | Integración con OpenStreetMap completamente validada. |
| `chat_service.py` | 98% | Gestión de chat en tiempo real con alta cobertura. |
| `user_service.py` | 85% | Gestión de usuarios con un buen nivel de pruebas. |
| `template_service.py` | 85% | Renderizado de plantillas correctamente validado. |

## Componentes con menor cobertura

| Archivo | Cobertura | Observación |
|----------|----------:|-------------|
| `authentication_service.py` | 75% | Permanecen pendientes algunos escenarios del proceso de autenticación y procesamiento relacionado con OSM. |
| `message_service.py` | 79% | Existen rutas de ejecución sin cubrir en `_push_messages` y `send_message_after_chat`. |
| `smtp_service.py` | 82% | Falta cubrir completamente el envío de correos de progreso de proyectos. |

---

# 5. Alcance y nivel de confianza actual

| Dimensión | Alcance | Nivel de confianza | Observaciones |
|-----------|---------|--------------------|---------------|
| Autenticación | 75% | Medio-Alto | Flujo de autenticación y generación de tokens validado. |
| Gestión de Usuarios | 85% | Alto | Operaciones CRUD y administración de roles probadas. |
| Mensajería | 79%–98% | Alto | Chat, notificaciones y correos electrónicos funcionando correctamente. |
| Plantillas | 85% | Alto | Renderizado de plantillas validado mediante pruebas unitarias. |
| Integración OSM | 100% | Muy Alto | Integración completamente cubierta por las pruebas. |

---

# 6. Conclusión

El módulo de **Seguridad, Usuarios y Comunicación** alcanzó una cobertura total del **82%**, dejando **257 líneas de código** aún sin cubrir por las pruebas unitarias. Respecto al estado inicial de **30%**, se obtuvo un incremento de **52 puntos porcentuales**, producto de la incorporación de aproximadamente **100 nuevas pruebas unitarias** enfocadas en flujos principales, casos límite y escenarios de error.

Si bien la cobertura alcanzada refleja un nivel de confianza alto en la estabilidad del módulo, aún existen oportunidades de mejora en **`authentication_service.py` (75%)** y **`message_service.py` (79%)**, cuyos escenarios pendientes permitirán superar el objetivo de cobertura del **85%** en futuras iteraciones del proceso de aseguramiento de la calidad del software.