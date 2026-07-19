<style>
  .cover-page {
    max-width: 700px;
    margin: 0 auto;
    padding: 60px 50px;
    font-family: 'Georgia', 'Times New Roman', serif;
    text-align: center;
    color: #1a1a1a;
    border-top: 4px solid #8B0000;
    border-bottom: 4px solid #8B0000;
  }
  .cover-page .institucion { font-size: 20px; font-weight: 700; letter-spacing: 0.05em; margin: 0 0 6px; text-transform: uppercase; }
  .cover-page .facultad, .cover-page .escuela { font-size: 14px; font-weight: 400; color: #444; margin: 0 0 4px; line-height: 1.4; }
  .cover-page .logo-wrap { margin: 32px auto; width: 130px; height: 130px; display: flex; align-items: center; justify-content: center; }
  .cover-page .logo-wrap img { max-width: 100%; max-height: 100%; }
  .cover-page .ficha { display: inline-block; text-align: left; margin-top: 20px; border-top: 1px solid #ddd; padding-top: 20px; }
  .cover-page .ficha table { border-collapse: collapse; }
  .cover-page .ficha td { padding: 6px 14px 6px 0; font-size: 13px; vertical-align: top; }
  .cover-page .ficha td.label { color: #777; font-weight: 600; white-space: nowrap; text-transform: uppercase; font-size: 11px; letter-spacing: 0.03em; }
  .cover-page .ubicacion { margin-top: 36px; font-size: 13px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #8B0000; }
</style>

<div class="cover-page">
  <p class="institucion">Universidad Nacional de San Agustín</p>
  <p class="facultad">Facultad de Ingeniería de Producción y Servicios</p>
  <p class="escuela">Escuela Profesional de Ingeniería de Sistemas</p>

  <div class="logo-wrap">
    <img src="/tests-docs/logo-unsa.png" alt="Logo UNSA" />
  </div>

  <div class="ficha">
    <table>
      <tr><td class="label">Curso</td><td>Pruebas de Software</td></tr>
      <tr><td class="label">Docente</td><td>Ing. Robert Edison Arisaca Mamani</td></tr>
      <tr><td class="label">Semestre</td><td>VII</td></tr>
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — EspecificaciÃ³n de Infraestructura y Entorno de Pruebas de IntegraciÃ³n</td></tr>
      <tr><td class="label">Fecha</td><td>15/07/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# EspecificaciÃ³n de Infraestructura y Entorno de Pruebas de IntegraciÃ³n

Este documento detalla la arquitectura tÃ©cnica, los componentes y el ciclo de vida del entorno requerido para la ejecuciÃ³n automatizada y reproducible de las pruebas de integraciÃ³n del backend del **Tasking Manager**.

---

## 1. PropÃ³sito del Entorno de Pruebas

Para aislar las pruebas de integraciÃ³n y evitar la contaminaciÃ³n del entorno de desarrollo local o producciÃ³n, se ha diseÃ±ado una infraestructura basada en bases de datos efÃ­meras y orquestaciÃ³n por contenedores. Su propÃ³sito central es garantizar un entorno determinista donde cada prueba inicie con un estado conocido y limpio.

---

## 2. OrquestaciÃ³n y Componentes (Docker Compose)

El ciclo de vida del entorno de pruebas se gestiona a travÃ©s de Docker Compose (`docker-compose.yml`).

| Componente | Rol en las Pruebas de IntegraciÃ³n | ConfiguraciÃ³n EspecÃ­fica |
| :--- | :--- | :--- |
| **Backend API (FastAPI)** | Servidor de pruebas (`tm-backend`). | Expuesto en el puerto 5000, con recarga en caliente desactivada para optimizar memoria en CI. |
| **Base de Datos (PostgreSQL 14)** | Persistencia real del motor PostGIS. | Red dedicada `tm-net`. |
| **Proxy Reverso (Traefik)** | SimulaciÃ³n de la capa de enrutamiento. | Valida que las rutas API (`/api/v2/`) se expongan correctamente como en producciÃ³n. |

---

## 3. Arquitectura del Motor de Pruebas (`conftest.py`)

El archivo `conftest.py` en la raÃ­z de la carpeta `tests/` es el orquestador tÃ©cnico crÃ­tico que habilita las pruebas de integraciÃ³n en Python, implementando el patrÃ³n de **Base de Datos EfÃ­mera** y **Transacciones Reversibles**.

### Flujo de EjecuciÃ³n del Entorno

```mermaid
graph TD
    A[Inicio Session Pytest] --> B[Crear BD de Test FÃ­sica]
    B --> C[Aplicar Migraciones Alembic / Crear Tablas]
    C --> D[Instalar Extensiones PostGIS]
    D --> E{Ejecutar Suite de IntegraciÃ³n}
    E -- Cada Test Individual --> F[Forzar Rollback AutomÃ¡tico]
    F -- Limpieza --> G[Destruir BD de Test `_test`]
```

### Decisiones TÃ©cnicas Implementadas:

1.  **Aislamiento FÃ­sico (`_test` database):**
    *   *ImplementaciÃ³n:* Al inicio de la sesiÃ³n, se duplica el esquema configurando la conexiÃ³n con un sufijo de pruebas (por ejemplo, `tasking_manager_test`).
    *   *JustificaciÃ³n:* Previene la destrucciÃ³n accidental de los datos de los desarrolladores durante la ejecuciÃ³n local de la suite de integraciÃ³n.
2.  **Transacciones Reversibles (`force_rollback=True`):**
    *   *ImplementaciÃ³n:* El motor inyecta un conector SQLAlchemy que inicia una transacciÃ³n en la base de datos que nunca llega a confirmarse (`commit`). Al terminar la funciÃ³n de prueba, se realiza un *rollback* forzado.
    *   *JustificaciÃ³n:* Otorga independencia absoluta a los casos de prueba. El test *B* nunca fallarÃ¡ por culpa de datos residuales insertados por el test *A*.
3.  **Cliente ASGI (FastAPI TestClient / HTTPX):**
    *   *ImplementaciÃ³n:* Las peticiones HTTP no pasan por la red local, sino que invocan directamente la aplicaciÃ³n ASGI en memoria usando `httpx.AsyncClient`.
    *   *JustificaciÃ³n:* Minimiza la latencia de red, acelerando la ejecuciÃ³n de los cientos de tests de integraciÃ³n.

---

## 4. GestiÃ³n de ConfiguraciÃ³n y Mocking

### ConfiguraciÃ³n DinÃ¡mica (`config.py` y `Settings`)
El entorno de pruebas sobreescribe variables crÃ­ticas usando Pydantic Settings. Las credenciales de base de datos se alteran dinÃ¡micamente para apuntar a los contenedores Docker mediante el uso de variables de entorno configuradas por `pytest-env`.

### SimulaciÃ³n de Dependencias Externas (Mocking)
Dado que las pruebas de integraciÃ³n evalÃºan el backend y su base de datos, el entorno debe cortar la comunicaciÃ³n real con servidores de terceros para evitar errores por tiempos de espera o cuotas de API.

*   **OAuth2 OSM:** Interceptado mediante simulaciÃ³n a nivel de `AuthenticationService`.
*   **SMTP (Correos):** El mÃ³dulo de envÃ­o de correos opera en modo *dummy* o se utiliza captura de salida (log capture) para validar el contenido del mensaje sin intentar entregarlo.

---

## 5. IntegraciÃ³n Continua (CI/CD)

El entorno diseÃ±ado localmente se replica 1:1 en GitHub Actions.
1. Se levantan los servicios de PostgreSQL/PostGIS.
2. Se inyectan las credenciales.
3. Se ejecuta el comando `pytest tests/api/integration/` con el plugin `pytest-cov` para generar los artefactos de mÃ©tricas de cobertura.

