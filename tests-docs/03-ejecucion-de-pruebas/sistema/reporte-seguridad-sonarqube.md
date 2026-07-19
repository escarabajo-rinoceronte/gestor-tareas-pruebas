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
  <b>Proyecto:</b> HOT Tasking Manager — Reporte de EjecuciÃ³n: Pruebas de Sistema (Seguridad â€” SAST y SCA) <br>
  <b>Fecha de Elaboración:</b> 19/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Reporte de EjecuciÃ³n: Pruebas de Sistema (Seguridad â€” SAST y SCA)

**Atributo de Calidad:** Seguridad (Security Testing)
**Responsable de EjecuciÃ³n:** Alexandra
**Fecha de EjecuciÃ³n:** 19 de Julio de 2026
**Herramientas:** SonarCloud (SCA + SAST) + Gitleaks (Secret Scanning)
**IntegraciÃ³n:** GitHub Actions CI/CD Pipeline (`seguridad-sonarqube.yml`)
**EstÃ¡ndar de referencia:** ISO/IEC 25010 â€” Atributo de Seguridad; IEEE 829

---

## 1. Objetivo

Detectar vulnerabilidades de seguridad, secretos expuestos y deuda tÃ©cnica en el cÃ³digo fuente del sistema Tasking Manager, utilizando herramientas de anÃ¡lisis estÃ¡tico (SAST) integradas al pipeline de integraciÃ³n continua (CI/CD).

---

## 2. Estrategia de Prueba

La estrategia de seguridad se divide en dos capas automatizadas que se ejecutan secuencialmente en cada `push` a la rama `develop`:

| Capa | Herramienta | Tipo de AnÃ¡lisis | Objetivo |
| :--- | :--- | :--- | :--- |
| 1 | **Gitleaks** | Secret Scanning | Detectar contraseÃ±as, tokens o claves API accidentalmente subidas al cÃ³digo |
| 2 | **SonarCloud** | SAST + SCA | Detectar vulnerabilidades de seguridad, bugs crÃ­ticos y cÃ³digo de baja calidad |

---

## 3. Evidencia de EjecuciÃ³n

### 3.1. Vista General de Proyectos en la OrganizaciÃ³n

La figura siguiente muestra que el proyecto `gestor-tareas-pruebas` fue analizado exitosamente por SonarCloud. El pipeline de CI/CD detectÃ³ y reportÃ³ resultados sobre las 76,000 lÃ­neas de cÃ³digo del sistema real.

![Vista general de la organizaciÃ³n en SonarCloud con el proyecto analizado](./sonar-01-projects-overview.jpeg)

---

### 3.2. Dashboard de Estado del Proyecto

La figura siguiente muestra el panel de control (dashboard) del proyecto, con el estado de calidad general.

![Dashboard de estado del proyecto en SonarCloud](./sonar-02-project-dashboard.jpeg)

**InterpretaciÃ³n del Quality Gate (Filtro de Calidad):**
> El "Quality Gate" indica **Failed** (Fallido). Esto es el **resultado esperado y buscado** de una prueba de seguridad efectiva: el sistema tiene deuda de seguridad preexistente en el cÃ³digo fuente, y la herramienta la detectÃ³ con precisiÃ³n. Si el Quality Gate hubiera salido en verde sin ningÃºn hallazgo sobre 76k lÃ­neas de cÃ³digo real, la herramienta habrÃ­a sido inefectiva.

---

### 3.3. Snapshot de Seguridad (Hallazgos de Vulnerabilidad)

La figura siguiente muestra el panel de seguridad, con los hallazgos clasificados por severidad.

![Panel de seguridad con 9 issues clasificados por severidad](./sonar-03-security-snapshot.jpeg)

**MÃ©tricas de Seguridad:**

| MÃ©trica | Valor | ClasificaciÃ³n ISO/IEC 25010 |
| :--- | :--- | :--- |
| **Security Rating** | E (CrÃ­tico) | Confidencialidad / Integridad |
| **Security Issues detectados** | 9 | Vulnerabilidades activas |
| **Blocker** | 11% | Requieren correcciÃ³n inmediata |
| **High** | 11% | CorrecciÃ³n en el prÃ³ximo sprint |
| **Medium** | 56% | Planificar correcciÃ³n |
| **Low** | 22% | Monitorear |
| **Security Hotspots Reviewed** | 100% âœ… | Todos los puntos sensibles marcados para revisiÃ³n |

---

### 3.4. Snapshot de Confiabilidad y Mantenibilidad

La figura siguiente muestra el anÃ¡lisis de confiabilidad (bugs) y mantenibilidad (deuda tÃ©cnica).

![Panel de confiabilidad y mantenibilidad con bugs y code smells](./sonar-04-reliability-maintainability.jpeg)

**MÃ©tricas de Confiabilidad y Mantenibilidad:**

| MÃ©trica | Valor | Impacto |
| :--- | :--- | :--- |
| **Reliability Rating** | E | 234 bugs potenciales en el cÃ³digo |
| **Reliability Issues** | 234 | Mayormente Medium (56%) y Low (32%) |
| **Maintainability Rating** | A âœ… | Excelente para un proyecto de 76k lÃ­neas |
| **Maintainability Issues** | 1,485 | CÃ³digo funcional pero mejorable (code smells) |
| **Duplications** | 1.2% | Dentro del rango aceptable |

---

## 4. AnÃ¡lisis e InterpretaciÃ³n

### 4.1. Â¿Por quÃ© el Quality Gate fallÃ³?
El Quality Gate fallÃ³ porque SonarCloud encontrÃ³ **9 vulnerabilidades de seguridad activas** en el cÃ³digo fuente. Este resultado es el **objetivo de la prueba**: demostrar que la herramienta funciona y es capaz de identificar problemas reales de seguridad en el sistema bajo prueba.

> **Nota metodolÃ³gica (Myers, "The Art of Software Testing"):** Una prueba de seguridad exitosa NO es aquella donde "no se encuentra nada". Una prueba exitosa es aquella que identifica los defectos existentes. El hallazgo de 9 vulnerabilidades confirma que la prueba fue ejecutada correctamente.

### 4.2. Â¿QuÃ© significa la calificaciÃ³n E en Seguridad?
SonarCloud utiliza una escala de A (mejor) a E (peor). La calificaciÃ³n **E en Security** indica que existe al menos una vulnerabilidad de severidad Blocker o Critical. Las 9 vulnerabilidades encontradas incluyen issues de severidad Blocker (11%) que deben priorizarse en el backlog de correcciones del equipo.

### 4.3. Punto positivo: Mantenibilidad A
A pesar de los hallazgos de seguridad, la calificaciÃ³n de **Mantenibilidad A** es notable: para un proyecto de 76,000 lÃ­neas de cÃ³digo real (un sistema open-source de producciÃ³n), solo 1,485 code smells representan una baja densidad de deuda tÃ©cnica. Esto habla bien de las prÃ¡cticas de desarrollo del equipo.

---

## 5. ConclusiÃ³n

| Aspecto | Resultado |
| :--- | :--- |
| **Pipeline CI/CD integrado** | âœ… Funciona en cada push a `develop` |
| **Secret Scanning (Gitleaks)** | âœ… NingÃºn secreto expuesto detectado |
| **AnÃ¡lisis SAST ejecutado** | âœ… Exitoso sobre 76k lÃ­neas de cÃ³digo |
| **Vulnerabilidades detectadas** | 9 issues de seguridad (requieren plan de remediaciÃ³n) |
| **Objetivo de la prueba** | âœ… **APROBADO** â€” la herramienta detectÃ³ deuda de seguridad real |

La Prueba de Sistema â€” Atributo de Seguridad se da por **ejecutada y documentada**. Los hallazgos deben ser ingresados al backlog del proyecto como defectos a remediar en sprints futuros.



