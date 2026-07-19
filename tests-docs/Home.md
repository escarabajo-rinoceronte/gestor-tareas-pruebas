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
  <b>Proyecto:</b> HOT Tasking Manager — Hito 3 Final: Sistema y Automatización Completa <br>
  <b>Fecha de Elaboración:</b> 19/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# HITO 3 — Pruebas de Software: Escarabajo Rinoceronte

**Repositorio:** [escarabajo-rinoceronte/gestor-tareas-pruebas](https://github.com/escarabajo-rinoceronte/gestor-tareas-pruebas)

## 📌 Descripción General
Este repositorio contiene todos los artefactos producidos durante el ciclo completo de testing sobre **HOT OSM Tasking Manager**, una plataforma de código abierto utilizada mundialmente para coordinar el mapeo colaborativo en respuesta a emergencias humanitarias. El sistema cuenta con un backend en Python/FastAPI y un frontend en React/Vite, desplegados mediante Docker.

El esfuerzo de validación finaliza en el **Hito 3** cubriendo el espectro completo: **Pruebas Unitarias, Funcionales, de Integración y de Sistema**.

## 👥 Integrantes y Especialización

| Nombre y Apellidos | Especialidad en Hito 3 |
|---|---|
| Quispe Arratea, Alexandra Raquel | **QA Lead, Pruebas de Sistema (Desempeño K6, Seguridad SonarQube/Gitleaks)** |
| Cari Lipe, Paul Andre | **Pruebas de Integración y Mantenimiento Unitarias Frontend** |
| Arias Quispe, Jhonatan David | **Pruebas de Sistema E2E (Playwright) e Integración de Bot WhatsApp** |
| Mamani Huarsaya Jorge | **Pruebas de Integración (Backend) y Unitarias** |
| Boza Portilla, Yordano Hernan | **Pruebas de Integración (Backend)** |
| Mollo Chuquicaña, Dolly Yadhira | **Pruebas Funcionales y Soporte de Calidad** |

---

## 🚀 Entregables y Artefactos del Hito 3

### 1. Pruebas de Sistema (ISO/IEC 25010)
Se focalizó en tres atributos de calidad principales, logrando una automatización total integrada en el pipeline CI/CD:
- **Funcionalidad (E2E con Playwright):** 3 flujos críticos ejecutados (Mapeo, Validación y Administración). Realizado por Jhonatan.
- **Eficiencia de Desempeño (Grafana K6):** Pruebas de carga y contención transaccional simulando 50 usuarios recurrentes. Realizado por Alexandra.
- **Seguridad (SonarCloud SAST y Gitleaks):** Implementación de análisis estático y búsqueda de secretos como compuerta de calidad en los pipelines de CI/CD para más de 76,000 líneas de código. Realizado por Alexandra.
- **Reporte Consolidado:** [[ejecucion pruebas sistema]]

### 2. Pruebas de Integración
Estrategia para verificar la correcta interacción de los módulos del backend y su comunicación con la base de datos PostGIS, alcanzando la **métrica del 85% de cobertura global exigida**. Liderado por Yordano, Paul y Jorge.
- **Módulo Tareas/Mapeo:** [[03 ejecucion modulo tareas mapeo]]
- **Módulo Usuarios/Autenticación:** [[04 ejecucion modulo usuarios autenticacion]]
- **Módulo Proyectos:** [[integration projects module]]

### 3. Pruebas Unitarias y Funcionales (Consolidación)
- **Cobertura Métrica del 85% Alcanzada:** Se logró superar y mantener el umbral del 85% de cobertura tanto en los módulos de Frontend (Jest) como de Backend (pytest) exigidos para este hito final.
- **Frontend:** [[01 ejecucion pruebas unitarias frontend]]
- **Backend:** [[02 ejecucion pruebas unitarias backend]]
- **Pruebas Funcionales:** 75 casos ejecutados al 100% con evidencias visuales en los 3 módulos críticos.

### 4. Automatización y Bots (Plus)
Como valor agregado, se incluyó el diseño de un bot de WhatsApp para notificaciones automáticas integrado al flujo de calidad del equipo, sumado a las potentes automatizaciones continuas en GitHub Actions (workflows de validación de PRs, auto-sincronización de Wiki y SonarQube).

---

## 🛠️ GitHub Wiki (Documentación completa)
La Wiki de GitHub es el portal de consulta unificado. **Se actualiza y renderiza automáticamente** mediante GitHub Actions (wiki-sync.yml) con cada push a la rama develop.

* **1. Planes de Pruebas:** Unitarias, Funcionales, Integración y Sistema.
* **2. Diseño:** Casos de uso de caja negra, unitarios y flujos E2E.
* **3. Ejecución:** Reportes con evidencias, capturas, y métricas reales.

👉 **Navega usando la barra lateral de la derecha para explorar todos los reportes formales.**
