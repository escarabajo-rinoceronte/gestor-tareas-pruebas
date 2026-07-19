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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — EspecificaciÃ³n TÃ©cnica: Pruebas de Seguridad</td></tr>
      <tr><td class="label">Fecha</td><td>17/07/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# EspecificaciÃ³n TÃ©cnica: Pruebas de Seguridad
**Proyecto:** HOT OSM Tasking Manager
**Componentes Evaluados:** API REST (FastAPI) y Middleware de AutorizaciÃ³n (JWT)

---

## 1. Estrategia y Objetivos de EjecuciÃ³n

| Vector Analizado | PropÃ³sito TÃ©cnico | Herramienta Asignada | JustificaciÃ³n de la SelecciÃ³n |
| :--- | :--- | :--- | :--- |
| **SAST (DetecciÃ³n de Secretos)** | Escanear el Ã¡rbol de commits y archivos de configuraciÃ³n para identificar exposiciÃ³n de tokens, credenciales de base de datos o variables de entorno filtradas. | **Gitleaks** | Procesamiento basado en heurÃ­stica y expresiones regulares de alta precisiÃ³n. Rastrea historiales Git completos en segundos sin interrumpir el flujo CI/CD. |
| **DAST (Fuzzing DinÃ¡mico)** | Interrogar directamente el API en ejecuciÃ³n (`:5000`) inyectando payloads corruptos y secuencias de escape para forzar fugas de informaciÃ³n, OOM o Inyecciones SQL. | **OWASP ZAP** | IntÃ©rprete nativo del contrato OpenAPI (`/api/docs`). Despliega automÃ¡ticamente ataques iterativos sobre todos los endpoints de FastAPI documentados sin necesidad de scripting manual extenso. |
| **AutorizaciÃ³n Rota (BOLA)** | Auditar la impermeabilidad del middleware de roles intentando operaciones destructivas (ej. Crear Proyectos) utilizando tokens desprovistos de los claims pertinentes. | **Newman (Postman)** | IteraciÃ³n programÃ¡tica dinÃ¡mica. Facilita la inyecciÃ³n e intercambio de la cabecera `Authorization: Bearer <jwt>`, permitiendo simular suplantaciÃ³n de roles a nivel de integraciÃ³n continua. |

## 2. PreparaciÃ³n del Entorno y Precondiciones CrÃ­ticas

| Requisito | ConfiguraciÃ³n TÃ©cnica y JustificaciÃ³n |
| :--- | :--- |
| **Aislamiento de Red** | El ataque ZAP de tipo *Active Scan* corrompe esquemas y altera metadatos relacionales irreparablemente. El entorno objetivo debe aislarse en una red puente local (`tm-net`) empleando volumen transitorio (`tm_db_data_test`). **ProhibiciÃ³n absoluta** de ejecuciÃ³n contra la BD de staging remoto o producciÃ³n. |
| **InhibiciÃ³n de Bloqueos (Rate Limiting)** | Deshabilitar middlewares de limitaciÃ³n de frecuencia volumÃ©trica durante la ejecuciÃ³n DAST. Los limitadores interceptarÃ­an al fuzzer reportando falsos negativos, impidiendo evaluar la tolerancia del backend a inyecciones. |
| **PoblaciÃ³n de Sesiones (Seed)** | Ejecutar `e2e-seed.py` para forzar la inyecciÃ³n inicial de usuarios. Extraer localmente 2 tokens JWT (`e2e_mapper` de bajo privilegio; `e2e_admin` de alto privilegio). Requerido para abrir el anÃ¡lisis ZAP hacia rutas protegidas por autenticaciÃ³n. |

## 3. Escenarios de Prueba: Vectores de Ataque OWASP

| Atributo | Escenario 1: GeoJSON SQL Injection (OWASP A03:2021 - Injection) |
| :--- | :--- |
| **Endpoint Objetivo** | `POST /api/v2/projects/` |
| **Vector de Ataque (Carga Ãštil)** | `{"type": "FeatureCollection", "features": [{"geometry": {"type": "Polygon", "coordinates": [[[0,0]...]]'; DROP TABLE projects CASCADE;--}}]}` |
| **JustificaciÃ³n TÃ©cnica** | GeoAlchemy2 aplica mapeos directos entre cadenas GeoJSON y tipos geomÃ©tricos binarios de PostGIS. La carencia de validaciÃ³n estricta de tipos de datos de entrada habilita el encadenamiento de comandos SQL destructivos (SQLi) a nivel del driver DBAPI. |
| **Criterio de ValidaciÃ³n** | Pydantic intercepta el payload deforme antes del ruteador asÃ­ncrono, devolviendo `422 Unprocessable Entity`. La traza no alcanza el *statement compiler* de SQLAlchemy ni genera transacciones nulas en la BD. |

<br>

| Atributo | Escenario 2: Broken Object Level Auth - BOLA (OWASP A01:2021) |
| :--- | :--- |
| **Endpoint Objetivo** | `POST /api/v2/tasks/{id}/validate/` |
| **Vector de Ataque (Carga Ãštil)** | EjecuciÃ³n de la solicitud HTTP adjuntando el JWT asignado exclusivamente al rol raso `e2e_mapper`. |
| **JustificaciÃ³n TÃ©cnica** | Medir la fiabilidad del decorador de roles y de los *claims* en FastAPI. Si la validaciÃ³n ocurre a nivel de vista (*frontend* React) sin correlato backend, los usuarios base podrÃ­an validar sus propias Ã¡reas alterando la integridad cartogrÃ¡fica del proyecto. |
| **Criterio de ValidaciÃ³n** | El middleware decodifica el JWT, comprueba la ausencia del *claim* necesario (`Validator`) y bloquea inmediatamente el acceso, emitiendo un HTTP `403 Forbidden` limpio. |

<br>

| Atributo | Escenario 3: ExposiciÃ³n de Entornos Debug (OWASP A05:2021) |
| :--- | :--- |
| **Endpoint Objetivo** | Mapeo de Puertos de Contenedores Host (`localhost`). |
| **Vector de Ataque (Carga Ãštil)** | Escaneo de *binds* mediante `nmap -p 5678,5000 localhost` bajo flag `TARGET_TAG=prod`. |
| **JustificaciÃ³n TÃ©cnica** | La imagen Docker despliega *DebugPy* (puerto 5678) habilitando inyecciÃ³n directa en memoria al intÃ©rprete de Python. Su filtraciÃ³n en redes expuestas confiere a un atacante capacidades absolutas de RCE (Remote Code Execution) evadiendo todas las reglas API. |
| **Criterio de ValidaciÃ³n** | El puerto 5678 responde `closed` o `filtered` al escÃ¡ner TCP; nula disponibilidad del *socket* fuera del modo `debug`. |

## 4. Procedimiento TÃ©cnico de EjecuciÃ³n

| Etapa | Comando de EjecuciÃ³n | JustificaciÃ³n de la Fase |
| :--- | :--- | :--- |
| **1. SAST (AnÃ¡lisis de Repositorio)** | `gitleaks detect --source . -v --report-path gl-report.json` | AuditorÃ­a retroactiva de todos los *commits* buscando claves API expuestas (Mapbox, Sentry) pre-compilaciÃ³n. |
| **2. ZAP Context Auth** | En OWASP ZAP (GUI): Context -> Authentication -> Inyectar Header `Authorization: Bearer <TOKEN_ADMIN>`. | Confiere autorizaciÃ³n nivel Administrador al fuzzer; vital para atravesar `401 Unauthorized` y mapear la superficie de control total. |
| **3. DAST (Active Scan)** | Importar Swagger `/api/docs` -> Iniciar *Active Scan* -> Restringir polÃ­tica a `SQL Injection`, `Command Injection` y `Path Traversal`. | ConcentraciÃ³n del *spider* dinÃ¡mico en forzar vectores de inyecciÃ³n contra todos los parÃ¡metros *query/body* del esquema OpenAPI. |
| **4. ValidaciÃ³n BOLA** | `newman run bola_collection.json -e jwt_env.json` | EjecuciÃ³n automatizada del set determinista de violaciones de roles, aislando la lÃ³gica de autorizaciÃ³n. |

## 5. Criterios de AceptaciÃ³n Global y Mecanismos de Respuesta

| MÃ©trica de Severidad | Umbral Transaccional (Bloqueo CI/CD) | Directiva de Respuesta y RemediaciÃ³n |
| :--- | :--- | :--- |
| **Vulnerabilidades Graves (CVSS >= 7.0)** | >= 1 hallazgo validado de InyecciÃ³n SQL, EjecuciÃ³n Remota o BOLA. | SuspensiÃ³n obligatoria del *merge* hacia *main*. RecreaciÃ³n empÃ­rica y manual del Payload Ofensivo por QA para descartar falsos positivos de ZAP antes de reportar a IngenierÃ­a. |
| **FiltraciÃ³n de Credenciales Clave** | IdentificaciÃ³n de *passwords* de PostgreSQL, URLs privadas, o JWT *Secrets* en texto plano. | EmisiÃ³n de alerta P1: Bloqueo de despliegue, rotaciÃ³n obligatoria de los secretos expuestos y reescritura forzada del historial Git involucrado. |
| **Fuzzing: Stacktraces y CaÃ­das** | El servidor devuelve respuestas HTTP `500` con el volcado completo de la pila (Stacktrace de Python) o el contenedor se detiene (*Crash*). | Las trazas revelan arquitectura interna (paths, nombres de base de datos) a un atacante. FastAPI debe enmascarar excepciones genÃ©ricas (`{"detail": "Internal Server Error"}`) bajo perfiles de producciÃ³n. |

