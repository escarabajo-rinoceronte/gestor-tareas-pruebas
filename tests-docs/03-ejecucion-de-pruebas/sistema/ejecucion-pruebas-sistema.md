# Informe de Ejecución de Pruebas de Sistema — Tasking Manager

## 1. Portada
**Curso:** Pruebas de Software  
**Proyecto:** Sistema Tasking Manager (HOT) — Informe de Ejecución de Pruebas de Sistema para los Módulos de Mapeo, Validación y Administración.  
**Fecha de Elaboración:** 19 de julio de 2026  
**Responsables:** Jhonatan y Alexandra  

---

## 2. Control de Versiones
| Versión | Autor(es) | Descripción del Cambio | Fecha |
| :--- | :--- | :--- | :--- |
| 1.0 | Equipo QA | Creación del informe consolidado de ejecución de pruebas de sistema (E2E, Desempeño y Seguridad) basado en el Plan de Pruebas de Jorge. | 19/07/2026 |

---

## 3. Introducción
### 3.1. Propósito
El presente informe documenta formalmente la ejecución de las **Pruebas de Sistema** para el Tasking Manager. Su propósito es registrar los resultados reales obtenidos al ejecutar las pruebas integrales de frontend y backend, validando el comportamiento observable del sistema completo desde la perspectiva del usuario final en un entorno réplica de producción.

### 3.2. Alcance
A diferencia de las pruebas manuales tradicionales, nuestra estrategia de pruebas de sistema es **altamente automatizada**, cubriendo los 3 flujos críticos de negocio y validando los atributos de calidad arquitectónica (Desempeño y Seguridad).

| Categoría | Total de Flujos / Casos |
| :--- | :--- |
| **Pruebas Funcionales (E2E Automatizado - Playwright)** | 3 flujos completos |
| **Pruebas No Funcionales (Desempeño y Carga - K6)** | 1 escenario de estrés masivo |
| **Pruebas No Funcionales (Seguridad - SonarQube)** | Pendiente de token |

---

## 4. Entorno de Pruebas
| Componente | Configuración utilizada |
| :--- | :--- |
| **Orquestador** | Docker Engine + Docker Compose v2.0+ |
| **Backend** | Python Flask (Imagen `ghcr.io/hotosm/tasking-manager/backend:main`) |
| **Base de datos** | PostgreSQL + PostGIS 14-3.3 (DB_MAX_CONNECTIONS optimizado a 30) |
| **Automatización E2E** | Node.js v18.x + Playwright Test + Chromium |
| **Automatización Carga** | Grafana K6 v0.52+ |

---

## 5. Estrategia de Pruebas Aplicada
Las pruebas de sistema se ejecutaron de forma automatizada. Las técnicas aplicadas fueron:
*   **Pruebas End-to-End (E2E):** Ejecución de flujos completos (Frontend + Backend + DB) operados como un usuario real a través de Playwright.
*   **Pruebas de Estrés y Contención (Carga):** Ejecución de scripts K6 simulando 50 usuarios concurrentes compitiendo transaccionalmente por el mismo recurso de base de datos.
*   **Análisis Estático de Seguridad (SAST):** Integración continua en GitHub Actions con SonarCloud y Gitleaks.

---

## 6. Resultados de Ejecución

### 6.1. Pruebas Funcionales E2E (Flujos Críticos)
Los siguientes reportes detallan la ejecución automatizada de los flujos de negocio principales. Haz clic en cada uno para ver la evidencia detallada de ejecución por Playwright:

*   ✅ **[01 Ejecución Flujo de Mapeo](01-ejecucion-flujo-mapeo.md)** (Ejecutado por Jhonatan)
*   ✅ **[02 Ejecución Flujo de Validación](02-ejecucion-flujo-validacion.md)** (Ejecutado por Jhonatan)
*   ✅ **[03 Ejecución Flujo de Administración](03-ejecucion-flujo-administracion.md)** (Ejecutado por Jhonatan)

### 6.2. Pruebas No Funcionales (Desempeño y Carga)
El análisis exhaustivo de contención de base de datos e integridad transaccional mediante Grafana K6:

*   ✅ **[Reporte Formal de Desempeño y Carga K6](reporte-desempeno-k6.md)** (Ejecutado por Alexandra)

### 6.3. Pruebas No Funcionales (Seguridad)
El escaneo de vulnerabilidades mediante SonarQube y SAST en el pipeline CI/CD:

*   ✅ **[Reporte Formal de Seguridad SonarQube](reporte-seguridad-sonarqube.md)** (Ejecutado por Alexandra)

---

## 7. Resumen de Cobertura
El sistema cuenta con una cobertura automatizada completa para los escenarios prioritarios definidos en el plan de diseño, superando los estándares de ejecución manual tradicionales gracias al uso de herramientas modernas (Playwright y K6).

---

## 8. Defectos Encontrados y Optimizaciones
Durante las rondas de pruebas de desempeño, se descubrió un defecto de arquitectura crítico (Cuello de Botella):

| ID Defecto | Componente | Descripción | Severidad | Estado |
| :--- | :--- | :--- | :--- | :--- |
| **DEF-SYS-001** | Backend / Base de Datos | La operación síncrona de recálculo de medallas (badges) al liberar una tarea (unlock) agota el límite por defecto de 8 conexiones (`DB_MAX_CONNECTIONS`) provocando *Timeouts* bajo concurrencia masiva. | Alta | **RESUELTO** (Límite elevado a 30) |

---

## 9. Conclusiones
*   **Nivel de Calidad:** Excelente. Los flujos de mapeo, validación y administración operan sin fallos en un entorno completo.
*   **Desempeño:** El sistema ha demostrado una capacidad excepcional para mantener la integridad de los datos (Race Conditions evitadas correctamente con rechazos HTTP 403) bajo el estrés de 50 usuarios concurrentes, manteniendo latencias inferiores a 1.8 segundos.
*   **Recomendación:** Se aprueba el pase a Producción de los módulos evaluados, condicionado únicamente a la finalización del análisis estático de seguridad (Atributo 2).
