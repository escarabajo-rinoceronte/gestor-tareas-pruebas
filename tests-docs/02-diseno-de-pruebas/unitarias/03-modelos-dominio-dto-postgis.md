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
  <b>Proyecto:</b> HOT Tasking Manager — 1. Base de Pruebas (Test Basis) <br>
  <b>Fecha de Elaboración:</b> 19/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# EspecificaciÃ³n de Pruebas Unitarias: Modelos de Dominio, Entidades PostGIS y DTOs
# 1. Base de Pruebas (Test Basis)

La presente suite de pruebas unitarias cubre las validaciones funcionales, reglas de integridad, restricciones estructurales y comportamiento geogrÃ¡fico asociados a los modelos de dominio, entidades PostGIS y objetos de transferencia de datos (DTOs) dentro de la arquitectura backend del sistema.

El alcance funcional comprende la verificaciÃ³n transversal de la consistencia de los datos en el almacenamiento relacional y espacial, el control de mutaciones en campos crÃ­ticos y el correcto mapeo estructural en el intercambio de informaciÃ³n.

## 1.1 Directorios y componentes relacionados al dominio

### Entidades de Dominio y Datos GeogrÃ¡ficos (PostGIS)

Componentes del modelo de datos encargados de la persistencia base, definiciÃ³n de relaciones, restricciones de integridad relacional y comportamiento geomÃ©trico o espacial en el almacenamiento.

* `backend/models/postgis/`

---

### Objetos de Transferencia de Datos (DTOs) y Esquemas

Componentes encargados de la definiciÃ³n de estructuras, tipado fuerte, serializaciÃ³n/deserializaciÃ³n y reglas de validaciÃ³n de los payloads que viajan hacia y desde los puntos de acceso del sistema.

* `backend/models/dtos/`

---

### Reglas de ValidaciÃ³n y Restricciones del Modelo

LÃ³gica interna acoplada a las entidades del sistema encargada de restringir de manera autÃ³noma los estados prohibidos, ciclos de vida de los registros y consistencia de los perfiles y recursos.

---
## 1.2 Suites de pruebas unitarias relacionadas

| Suite de prueba | Dominio funcional | DescripciÃ³n |
| :--- | :--- | :--- |
| `test_user.py` | GestiÃ³n de Usuarios | Valida la persistencia, restricciones de unicidad, mutaciÃ³n segura de campos crÃ­ticos del perfil (como identificadores y enlaces de avatar) y consistencia en consultas paginadas tanto en entornos sÃ­ncronos como asÃ­ncronos. |
| `test_project.py` | GestiÃ³n de Proyectos | Valida la creaciÃ³n, relaciones base con usuarios y la integridad de los datos descriptivos y espaciales/geogrÃ¡ficos vinculados a los proyectos de mapeo en el sistema. |
| `test_project_info.py` | InformaciÃ³n de Proyectos | Valida la consistencia, traducciÃ³n, almacenamiento y recuperaciÃ³n de metadatos, descripciones y especificaciones detalladas asociadas a los proyectos. |
| `test_task.py` | GestiÃ³n de Tareas | Valida el ciclo de vida de las tareas, control de estados permitidos (mapeado, validado, etc.), restricciones transaccionales y consistencia espacial de las geometrÃ­as de las tareas. |
| `test_message.py` | MensajerÃ­a y Alertas | Valida la estructura de almacenamiento, persistencia de notificaciones e integridad relacional de los mensajes enviados entre colaboradores y el sistema. |
| `test_organisation.py` | Organizaciones | Valida la persistencia de entidades organizacionales, restricciones de nombres, almacenamiento de imÃ¡genes/logos y la correcta vinculaciÃ³n relacional con proyectos y usuarios. |
| `test_banner.py` | Componentes de DifusiÃ³n | Valida el almacenamiento, vigencia, estados de visibilidad y consistencia de los banners informativos o alertas globales del sistema. |
| `test_custom_editor.py` | Editores Personalizados | Valida la configuraciÃ³n, persistencia y estructuras de datos que definen los editores de mapas personalizados permitidos para los colaboradores. |
| `test_mapping_dto.py` | ValidaciÃ³n de Datos (DTO) | Valida la estructura, tipado fuerte, restricciones de entrada y mapeo de datos orientados a los flujos y estados del proceso de mapeo. |
| `test_project_dto.py` | ValidaciÃ³n de Datos (DTO) | Valida las reglas de serializaciÃ³n, deserializaciÃ³n y esquemas de validaciÃ³n estructural para la creaciÃ³n y actualizaciÃ³n de la informaciÃ³n de proyectos. |

### Directorios de pruebas relacionados

#### API (Entorno Moderno / AsÃ­ncrono)

* `tests/api/unit/models/postgis/`

#### Backend (Entorno Legado / SÃ­ncrono y DTOs)

* `tests/backend/unit/models/dtos/`
* `tests/backend/unit/models/postgis/`

---

## 1.3 Dependencias controladas o simuladas

| Dependencia | Tipo | Objetivo |
| :--- | :--- | :--- |
| Motor de Base de Datos | Componente de datos | Validar la persistencia e integridad relacional/espacial real bajo aislamiento controlado, garantizando la reversiÃ³n completa (`force_rollback=True`) de transacciones en cada ciclo de prueba (`db_connection_fixture`). |
| APIs y Plataformas Externas | Servicios externos | Simular respuestas, flujos de autenticaciÃ³n e intercambio de perfiles remotos (como OpenStreetMap) para verificar la resiliencia y la capacidad de transformaciÃ³n de los modelos ante datos externos. |
| Servicios de Red y Multimedia | Servicios de red | Interceptar y simular peticiones de verificaciÃ³n de recursos remotos (como URLs de avatares u organizaciÃ³n) para validar formatos permitidos sin requerir conectividad activa a internet. |

---

## 1.4 Cobertura de objetivos del proyecto

### Ã‰picas y Objetos de Negocio Asociados
* GestiÃ³n del ciclo de vida y persistencia de datos de colaboradores, proyectos, tareas y configuraciones del sistema.
* Integridad, consistencia relacional y almacenamiento seguro de informaciÃ³n descriptiva y geogrÃ¡fica (PostGIS).

### Requisitos funcionales validados
* Restricciones de integridad a nivel de datos (control de mutaciÃ³n de roles, flujos de estados de tareas y reglas de unicidad).
* Estructuras de intercambio de informaciÃ³n robustas mediante DTOs para motores de bÃºsqueda, filtros avanzados y paginaciÃ³n integrada.


