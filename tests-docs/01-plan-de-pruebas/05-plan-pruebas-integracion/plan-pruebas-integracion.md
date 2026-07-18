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
  <b>Proyecto:</b> HOT Tasking Manager — Plan de Pruebas de IntegraciÃ³n <br>
  <b>Fecha de Elaboración:</b> 12/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Plan de Pruebas de IntegraciÃ³n

**Proyecto:** HOT OSM Tasking Manager  
**Equipo:** Escarabajo Rinoceronte  
**Fase:** Sprint 2 - Hito 2  
**VersiÃ³n:** 2.1 (Consolidada)  
**Fecha:** Junio 2026  

---

## 1. Objetivo y Alcance

### 1.1 Objetivo
Validar la comunicaciÃ³n e interoperabilidad funcional y tÃ©cnica entre los componentes del sistema HOT OSM Tasking Manager, verificando que los contratos de integraciÃ³n (Base de Datos, APIs, Servicios de Dominio y Servicios Externos) operen de forma conjunta y preserven la integridad del flujo de negocio.

### 1.2 Estrategia de ModularizaciÃ³n del Backend
La implementaciÃ³n del backend estÃ¡ dividida por **Dominios de Negocio** (*Bounded Contexts*) en lugar de capas tÃ©cnicas puras. Para las pruebas de integraciÃ³n, esto significa que se validarÃ¡n transacciones completas (*Verticales*) y dependencias entre mÃ³dulos (*Horizontales*):

| MÃ³dulo Funcional | Responsabilidad de IntegraciÃ³n Principal |
| :--- | :--- |
| **Usuarios y Auth** | Identidad, perfiles, sesiÃ³n OAuth y niveles de mapper. |
| **Proyectos** | ConfiguraciÃ³n de metadatos, AOI (Ãrea de InterÃ©s) y control de autorÃ­a. |
| **Tareas y Mapeo** | Flujo de estados cartogrÃ¡ficos, locks temporales y particiÃ³n espacial. |

La asociaciÃ³n de una prueba a un mÃ³dulo se define por su **Punto de Entrada** y **Propiedad del Estado**. Una prueba de integraciÃ³n rara vez evalÃºa exclusivamente un mÃ³dulo; por definiciÃ³n, valida cÃ³mo un flujo de negocio especÃ­fico afecta mÃºltiples Ã¡reas del sistema.

### 1.3 Alcance
**Incluido en este plan:**
- IntegraciÃ³n Vertical: ComunicaciÃ³n entre API Gateway, Middlewares, Servicios de Dominio, Modelos ORM (SQLAlchemy) y la Base de Datos (PostgreSQL/PostGIS).
- IntegraciÃ³n Horizontal: La comunicaciÃ³n entre los MÃ³dulos Funcionales descritos.
- IntegraciÃ³n Externa: ComunicaciÃ³n del backend con el Servicio OpenStreetMap (OAuth2).
- Sistema de notificaciones interno por eventos.

**Excluido de este plan:**
- LÃ³gica interna pura aislada de dependencias (Pruebas Unitarias).
- Pruebas completas de interfaz grÃ¡fica E2E (Frontend/Tauri).
- Servicios descontinuados (RENIEC/SUNAT, legacy).
- Despliegue en entornos de producciÃ³n.

---

## 2. Enfoque y Estrategia de IntegraciÃ³n

Se aplicarÃ¡ una combinaciÃ³n de un enfoque **Modular Basado en Flujos de Negocio** apoyado por una estrategia de ensamblaje tÃ©cnico **Bottom-Up**.

1.  **Cimientos TÃ©cnicos:** Primero se garantiza la persistencia e infraestructura (PostgreSQL/PostGIS + Alembic).
2.  **LÃ³gica de API y Servicios:** Se verifican los controladores FastAPI interactuando con los servicios y la BD.
3.  **Dependencias Externas:** Se evalÃºa la integraciÃ³n con OSM y sistemas asÃ­ncronos.
4.  **IntegraciÃ³n Transversal (Big-Bang Parcial por MÃ³dulo):** Se orquesta la ejecuciÃ³n del flujo completo en un entorno efÃ­mero.

**Stubs y Mocks Definidos:**
- **Servicios Externos:** Las respuestas OAuth2 de OSM serÃ¡n simuladas mediante intercepciones de red (e.g. `WireMock` o `pytest-httpx`/`responses`) para evitar llamadas fallidas por cuotas o latencia.
- **Base de Datos:** Se utilizarÃ¡ un contenedor de PostgreSQL real y persistente efÃ­mera por cada sesiÃ³n de tests, en lugar de simular la BD (no se mockea el ORM).

---

## 3. Diagrama de IntegraciÃ³n

El siguiente flujo representa la ruta transversal tÃ­pica que evaluarÃ¡n las pruebas para un flujo de negocio (por ejemplo, Bloqueo de Tarea):

```mermaid
graph TD
    A[Cliente de Pruebas: HTTP/pytest] -->|Endpoint POST| B[API Gateway / Auth]
    B -->|ValidaciÃ³n Token| C[MÃ³dulo Usuarios]
    B -->|InvocaciÃ³n LÃ³gica| E[MÃ³dulo Tareas/Servicios]
    E -->|VerificaciÃ³n Dependencia| D[MÃ³dulo Proyectos]
    E -->|TransacciÃ³n ORM| F[SQLAlchemy]
    F -->|Persistencia| G[PostgreSQL / PostGIS]
    E -.->|NotificaciÃ³n| H[MÃ³dulo MensajerÃ­a]
```

---

## 4. Criterios de Entrada

Para iniciar las pruebas de integraciÃ³n en cada sprint/mÃ³dulo, deben cumplirse:
- [ ] Pruebas unitarias de los componentes participantes aprobadas (Objetivo general > 80% cobertura).
- [ ] Contenedores de prueba definidos en `docker-compose.yml` ejecutando sin errores (API y DB).
- [ ] Migraciones de esquema (`alembic upgrade head`) aplicadas correctamente en la BD de pruebas.
- [ ] DefiniciÃ³n completa de los contratos de la API o los DTOs intermedios a validar.

---

## 5. Matriz de Interfaces a Integrar (Capa Core)

| ID | Origen | Destino | OperaciÃ³n | Endpoint / Evento Principal |
|---|---|---|---|---|
| INT-IF-01 | FastAPI | PostgreSQL (PostGIS) | Operaciones GIS y CRUD sobre estado de tareas | Capa ORM / `db.py` |
| INT-IF-02 | FastAPI | OSM Auth (OAuth2) | SincronizaciÃ³n de token y perfil OSM | `GET /api/v2/system/authentication/login/` |
| INT-IF-03 | FastAPI | Internal Bus | GeneraciÃ³n de notificaciones post-mapeo | Eventos `notifications.py` |

*(Nota: Las matrices especÃ­ficas de APIs funcionales se documentan en el DiseÃ±o de Pruebas de cada mÃ³dulo).*

---

## 6. Entorno y Recursos Requeridos

*(Este componente se documenta detalladamente en la EspecificaciÃ³n de Infraestructura y Entorno: `01-infraestructura-entorno.md`).*

**Resumen Operativo:**
- **Base de Datos:** Instancia aislada de PostgreSQL 14 con extensiÃ³n PostGIS 3.
- **OrquestaciÃ³n:** Docker Compose para estandarizar el despliegue local de backend y BD.
- **Framework de Pruebas:** Pytest con `anyio` (para asincronÃ­a) y `httpx` (para invocaciÃ³n de APIs).

---

## 7. Cronograma General de Pruebas de IntegraciÃ³n

| Fase | Tarea | Componentes Involucrados |
|---|---|---|
| **Fase 1** | ValidaciÃ³n Base (Bottom-Up) | Modelos ORM, Migraciones, Repositorios, ConexiÃ³n BD. |
| **Fase 2** | IntegraciÃ³n de Servicios Externos | OSM OAuth2, Mocks de Red, Respuestas Externas. |
| **Fase 3** | EjecuciÃ³n de Flujos Modulares | MÃ³dulo Usuarios, Proyectos y Tareas (Controladores + Servicios + BD). |
| **Fase 4** | E2E TÃ©cnico y Reportes | EjecuciÃ³n automatizada en CI/CD, CÃ¡lculo de Cobertura Final. |

---

## 8. Riesgos y Mitigaciones

| ID | Riesgo | Probabilidad / Impacto | MitigaciÃ³n |
|---|---|---|---|
| R-INT-01 | Fallo de conexiÃ³n o cuota API OSM | Alta / Alto | Utilizar librerÃ­as de Mocking de red (por ejemplo, `httpx-mock`) para interceptar la respuesta de login. |
| R-INT-02 | ContaminaciÃ³n de Datos entre Pruebas | Alta / Alto | Utilizar transacciones efÃ­meras (`force_rollback=True`) por cada funciÃ³n de test para mantener un estado limpio. |
| R-INT-03 | Lentitud extrema de integraciÃ³n GIS | Media / Medio | Excluir datos cartogrÃ¡ficos mundiales; usar polÃ­gonos minimalistas (Cajas delimitadoras pequeÃ±as) en los tests de `SplitService`. |

---

## 9. Criterios de Salida

Se considerarÃ¡ aprobado el plan de integraciÃ³n de un mÃ³dulo o hito cuando:
- El 100% de las pruebas diseÃ±adas para los mÃ³dulos de Usuarios, Proyectos y Tareas se encuentren programadas y ejecutÃ¡ndose en un orquestador local.
- Se haya alcanzado un **Pass Rate** > 95%.
- Se reporte la cobertura real (excluyendo tests duplicados unitarios) superando los umbrales definidos por mÃ³dulo (80-85%).
- Los resultados y volcados de consola estÃ©n anexados en el respectivo Reporte de EjecuciÃ³n.


