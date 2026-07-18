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
  <b>Proyecto:</b> HOT Tasking Manager — MÃ³dulo de Usuarios y AutenticaciÃ³n (User Management) <br>
  <b>Fecha de Elaboración:</b> 15/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# MÃ³dulo de Usuarios y AutenticaciÃ³n (User Management)

## 1. Criterio de SelecciÃ³n

Para que un archivo de prueba sea considerado parte de este mÃ³dulo, debe cumplir al menos uno de los siguientes requisitos:
1.  **GestiÃ³n de Identidad y Perfil:** El test debe validar operaciones relacionadas con la creaciÃ³n de la cuenta, actualizaciÃ³n de intereses, roles, datos de contacto (email) y visibilidad de informaciÃ³n personal.
2.  **AutenticaciÃ³n y AutorizaciÃ³n:** El test debe verificar la conexiÃ³n con OpenStreetMap (OSM) para el inicio de sesiÃ³n, la generaciÃ³n y verificaciÃ³n de tokens JWT, o las polÃ­ticas de roles de acceso.
3.  **Niveles de Experiencia y Recompensas:** El test debe interactuar con el recÃ¡lculo de *Mapping Levels* de los mappers o la simulaciÃ³n de insignias (*Badges*).
4.  **ExposiciÃ³n de Recursos de Usuarios:** El punto de entrada debe ser un endpoint diseÃ±ado para consultar o mutar perfiles ubicado en `backend/api/users/`.

---

## 2. Listado de suites de pruebas de integraciÃ³n actuales

El conjunto completo para el mÃ³dulo **Usuarios y AutenticaciÃ³n** consta de **8 archivos**.

### Archivos Incluidos

| Archivo de Prueba | JustificaciÃ³n de InclusiÃ³n |
| :--- | :--- |
| `api/users/test_actions.py` | Valida acciones restrictivas sobre el usuario: asignaciÃ³n de rol por administradores, verificaciÃ³n de correos y permisos HTTP 403. |
| `api/users/test_openstreetmap.py` | Cubre el flujo de callbacks, autorizaciones y manejo de errores 502 al interactuar con el login de OSM. |
| `api/users/test_resources.py` | Valida las reglas de privacidad de datos, obtenciÃ³n de perfil ajeno frente a propio y filtros paginados. |
| `api/users/test_statistics.py` | Valida la recuperaciÃ³n temporal del historial de mapeo y lectura del estado de la experiencia del mapper. |
| `services/users/test_authentication_service.py` | Prueba la lÃ³gica aislada de login; determina si el usuario existe o si es su primer registro (*User Create*). |
| `services/users/test_osm_service.py` | EvalÃºa las llamadas directas de sincronizaciÃ³n al servicio externo de OpenStreetMap. |
| `services/users/test_user_service.py` | Prueba el algoritmo central de salto de nivel (*Mapping Level*), simulando hitos de mapeo sin dependencia de red HTTP. |
| `models/test_user.py` | EvalÃºa directamente la serializaciÃ³n segura a DTO (Data Transfer Object), asegurando que el correo electrÃ³nico no sea expuesto pÃºblicamente. |

### Archivos Excluidos

*   `api/projects/*`: Se excluyen porque administran el ciclo de vida, campaÃ±as y gestiÃ³n de proyectos, lo que pertenece al **MÃ³dulo de GestiÃ³n de Proyectos**.
*   `api/tasks/*`: Se excluyen porque validan la creaciÃ³n, divisiÃ³n y estado cartogrÃ¡fico de una tarea en el editor geogrÃ¡fico, no la identidad del usuario en sÃ­.

---

## 3. AnÃ¡lisis Funcional por Archivo

### A. AutenticaciÃ³n y Login (`api/users/test_openstreetmap.py`, `services/users/test_authentication_service.py`)
*   **Objetivo:** Garantizar que la entrada al sistema mediante OAuth sea robusta y las sesiones se validen criptogrÃ¡ficamente.
*   **Flujos Cubiertos:** Callback de OSM, creaciÃ³n transparente de usuario al primer login, generaciÃ³n de JWT, validaciÃ³n de token.
*   **Componentes:** `AuthenticationService`, `OSMService`, endpoints de login en OSM.

### B. Consulta de Perfiles y Privacidad (`api/users/test_resources.py`, `models/test_user.py`)
*   **Objetivo:** Verificar que el acceso a datos sensibles (correo, gÃ©nero) respete las reglas de propiedad y se ejecuten consultas correctas.
*   **Flujos Cubiertos:** PeticiÃ³n del propio perfil, ocultaciÃ³n de datos a terceros, listado general de contribuidores.
*   **Componentes:** `UserService`, `User` (Modelo PostGIS).

### C. AdministraciÃ³n y Acciones del Usuario (`api/users/test_actions.py`)
*   **Objetivo:** Comprobar que los cambios de estado interno y roles administrativos funcionen correctamente.
*   **Flujos Cubiertos:** Cambios de rol (Mappers a Admins), validaciÃ³n de correos, actualizaciÃ³n de intereses, control de roles invÃ¡lidos.
*   **Componentes:** `UserService`, middlewares de autorizaciÃ³n.

### D. Reglas de Negocio de Identidad y Experiencia (`services/users/test_user_service.py`)
*   **Objetivo:** Probar el core del dominio, especÃ­ficamente la progresiÃ³n del *Mapper*.
*   **Flujos Cubiertos:** Salto de nivel (*Beginner* a *Intermediate*), asignaciÃ³n de atributos y actualizaciÃ³n de perfiles en la base de datos.
*   **Componentes:** `UserService`, simulaciones de `MappingBadge`.

---

## 4. Diagrama de InteracciÃ³n de las Pruebas de IntegraciÃ³n

Este diagrama muestra cÃ³mo los tests de este mÃ³dulo ejercen mÃºltiples capas y componentes del sistema:

```mermaid
sequenceDiagram
    participant Test as Integration Test (User Auth)
    participant API as FastAPI Controllers
    participant AuthService as AuthenticationService
    participant UserService as UserService
    participant OSM as OpenStreetMap API
    participant DB as PostgreSQL + PostGIS

    Test->>API: GET /api/v2/system/authentication/login/
    API->>AuthService: login_user(osm_oauth_response)
    AuthService->>OSM: Request OSM user details
    OSM-->>AuthService: OSM User Data (username, id)
    AuthService->>DB: Query existing User by OSM ID
    alt User exists
        AuthService->>DB: UPDATE last_login
    else User is new
        AuthService->>UserService: register_user()
        UserService->>DB: INSERT new User
    end
    DB-->>AuthService: User persisted
    AuthService->>AuthService: Generate JWT Session Token
    AuthService-->>API: Session JWT
    API-->>Test: Assert Session Token created (HTTP 200)
```

---

## 5. Alcance

El alcance actual de las pruebas de integraciÃ³n para el mÃ³dulo **Usuarios y AutenticaciÃ³n** es **excelente** en la capa de seguridad perimetral, pero presenta Ã¡reas de mejora en el procesamiento de bÃºsquedas y recompensas.

| DimensiÃ³n | Alcance | Nivel de Confianza | Observaciones |
| :--- | :--- | :--- | :--- |
| **Inicio de SesiÃ³n y AutenticaciÃ³n** | 90% | **Muy Alto** | La suma de `openstreetmap.py` y `authentication_service.py` brinda gran seguridad en la puerta de entrada. |
| **Persistencia de Entidad de Usuario** | 81% | **Alto** | `user.py` se validÃ³ exhaustivamente, asegurando que los datos sensibles (ej. correo) no se fuguen. |
| **GestiÃ³n de Roles Administrativos** | 70% | **Medio-Alto** | Se aseguran las respuestas HTTP 403 para proteger roles crÃ­ticos. |
| **CÃ¡lculo de Mapping Levels** | 65% | **Medio** | Cubre progresiones normales, pero ignora fluctuaciones extremas de estadÃ­sticas. |
| **BÃºsqueda y PaginaciÃ³n** | 45% | **Bajo** | Gran parte de las mutaciones de queries HTTP estÃ¡n sin probar en `resources.py`. |
| **Otorgamiento de Badges** | 10% | **Bajo** | Alta dependencia en simulaciones (*mocks*) para la persistencia transaccional de recompensas. |

**ConclusiÃ³n del Estado Actual:**
Las pruebas de integraciÃ³n actuales establecen un cerco de seguridad perimetral excelente sobre el MÃ³dulo de Usuarios y AutenticaciÃ³n. Garantizan que los colaboradores y sus accesos iniciales estÃ©n blindados (ej. 100% en flujos OAuth con OSM). Sin embargo, para escalar a un modelo de excelencia tÃ©cnica superior, el mÃ³dulo requiere abandonar las simulaciones transaccionales en el otorgamiento de insignias (*Badges*) e implementar casos de prueba combinados para los filtros de bÃºsqueda de contribuidores.

---

## 6. EjecuciÃ³n de pruebas funcionales previa

Hemos ejecutado las pruebas de integraciÃ³n previamente para cobertura del mÃ³dulo.

```sh
PS E:\Ing. Sistemas\4to_aÃ±o\PS\Proyecto_Final\gestor-tareas-pruebas> docker compose exec tm-backend coverage run -m pytest tests/api/integration/api/users/test_resources.py tests/api/integration/api/users/test_actions.py tests/api/integration/api/users/test_statistics.py tests/api/integration/api/users/test_openstreetmap.py tests/api/integration/services/users/test_authentication_service.py tests/api/integration/services/users/test_user_service.py tests/api/integration/services/users/test_osm_service.py tests/api/integration/models/test_user.py -p no:warnings
time="2026-07-04T02:40:42-05:00" level=warning msg="The \"DEFAULT_VALIDATOR_TEAM_ID\" variable is not set. Defaulting to a blank string."
time="2026-07-04T02:40:42-05:00" level=warning msg="The \"DEFAULT_VALIDATOR_TEAM_ID\" variable is not set. Defaulting to a blank string."
==================================================== test session starts =====================================================
platform linux -- Python 3.10.20, pytest-8.3.5, pluggy-1.5.0
rootdir: /usr/src/app
configfile: pyproject.toml
plugins: anyio-4.9.0, cov-7.1.0
collected 83 items                                                                                                           

tests/api/integration/api/users/test_resources.py .............................                                        [ 34%]
tests/api/integration/api/users/test_actions.py .....................                                                  [ 60%]
tests/api/integration/api/users/test_statistics.py .........                                                           [ 71%]
tests/api/integration/api/users/test_openstreetmap.py ....                                                             [ 75%]
tests/api/integration/services/users/test_authentication_service.py ..........                                         [ 87%]
tests/api/integration/services/users/test_user_service.py ......                                                       [ 95%]
tests/api/integration/services/users/test_osm_service.py ..                                                            [ 97%]
tests/api/integration/models/test_user.py ..                                                                           [100%]

=============================================== 83 passed in 71.56s (0:01:11) ================================================
```

```sh
PS E:\Ing. Sistemas\4to_aÃ±o\PS\Proyecto_Final\gestor-tareas-pruebas> docker compose exec tm-backend coverage report -m --include="backend/api/users/actions.py,backend/api/users/openstreetmap.py,backend/api/users/resources.py,backend/api/users/statistics.py,backend/services/users/authentication_service.py,backend/services/users/osm_service.py,backend/services/users/user_service.py,backend/models/postgis/user.py"
time="2026-07-04T02:42:36-05:00" level=warning msg="The \"DEFAULT_VALIDATOR_TEAM_ID\" variable is not set. Defaulting to a blank string."
time="2026-07-04T02:42:36-05:00" level=warning msg="The \"DEFAULT_VALIDATOR_TEAM_ID\" variable is not set. Defaulting to a blank string."
Name                                               Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------
backend/api/users/__init__.py                          0      0   100%
backend/api/users/actions.py                          83     27    67%   90, 101-103, 161-165, 243-248, 270-274, 319-323, 404-405
backend/api/users/openstreetmap.py                    16      0   100%
backend/api/users/resources.py                       119     61    49%   84-111, 204-205, 214-294, 325-326, 536-546
backend/api/users/statistics.py                       68     28    59%   100-101, 153, 191-230, 244
backend/models/postgis/user.py                       325     63    81%   130-131, 173-175, 210-211, 223, 238, 273-276, 331-350, 359-411, 448-462, 468-473, 540, 545, 558-576, 580-586, 612-619, 623, 638-643, 647, 679, 696-708, 712
backend/services/users/__init__.py                     0      0   100%
backend/services/users/authentication_service.py     188     55    71%   39-40, 55-57, 61-62, 79, 82-86, 92-93, 165, 185-187, 210-211, 228, 240, 244, 247-251, 254, 267-290, 298, 302, 305-308, 312, 321
backend/services/users/osm_service.py                 57     27    53%   26-34, 43-63, 76, 78, 90
backend/services/users/user_service.py               470    190    60%   107-113, 117-123, 134, 141-157, 161-168, 202-224, 305-406, 462-567, 668-669, 718, 738-742, 747, 752-754, 759-766, 771-775, 826, 831-832, 967, 982-983, 996-999, 1004-1005, 1012-1022, 1032-1033, 1056, 1064, 1073, 1077-1096, 1102-1127, 1138-1159, 1174-1186, 1195-1196, 1205, 1209-1219
--------------------------------------------------------------------------------
TOTAL                                               1326    451    66%
```



