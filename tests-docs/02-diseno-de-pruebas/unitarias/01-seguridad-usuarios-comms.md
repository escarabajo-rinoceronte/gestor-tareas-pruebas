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
  <b>Fecha de Elaboración:</b> 29/05/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# EspecificaciÃ³n de Pruebas Unitarias: Seguridad, Usuarios y ComunicaciÃ³n
# 1. Base de Pruebas (Test Basis)

La presente suite de pruebas unitarias cubre funcionalidades relacionadas con autenticaciÃ³n, autorizaciÃ³n, validaciÃ³n de identidad, gestiÃ³n de usuarios, procesamiento de mensajes y comunicaciÃ³n del sistema dentro de la arquitectura backend.

El alcance funcional comprende componentes distribuidos transversalmente en mÃºltiples capas arquitectÃ³nicas relacionadas con seguridad, usuarios y comunicaciÃ³n.

## 1.1 Directorios y componentes relacionados al dominio

### Servicios de negocio

Componentes responsables de la lÃ³gica principal de autenticaciÃ³n, usuarios y comunicaciÃ³n.

* `backend/services/users/`
* `backend/services/messaging/`

---

### API y Endpoints

Componentes responsables de exponer funcionalidades relacionadas con autenticaciÃ³n, usuarios y comunicaciÃ³n mediante rutas HTTP y controladores asociados.

* `backend/api/users/`
* `backend/api/auth/`

---

### Modelos y transformaciÃ³n de datos

Componentes responsables de representar, validar y transformar informaciÃ³n relacionada con usuarios y autenticaciÃ³n.

* Modelos relacionados con usuarios y sesiones.
* DTOs y validadores asociados a autenticaciÃ³n.
* TransformaciÃ³n de respuestas externas y payloads.

---

### ComunicaciÃ³n y procesos desacoplados

Componentes relacionados con procesamiento de mensajes, validaciÃ³n de correo electrÃ³nico y comunicaciÃ³n desacoplada.

* Servicios SMTP.
* GeneraciÃ³n de mensajes y notificaciones.
* Procesamiento de validaciones por correo electrÃ³nico.
* Flujos de comunicaciÃ³n asÃ­ncrona.

---

### Integraciones externas

Servicios externos utilizados por componentes asociados a usuarios y comunicaciÃ³n.

* OpenStreetMap (OSM).
* SMTP Service.
* GeneraciÃ³n y validaciÃ³n de tokens de autenticaciÃ³n.

---
## 1.2 Suites de pruebas unitarias relacionadas

| Suite de prueba                  | Dominio funcional | DescripciÃ³n                                                                                                                                                          |
| :------------------------------- | :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `test_authentication_service.py` | Seguridad         | Valida generaciÃ³n y verificaciÃ³n de tokens de autenticaciÃ³n, validaciÃ³n de sesiones y flujos de verificaciÃ³n de correo electrÃ³nico.                                  |
| `test_osm_service.py`            | Usuarios          | Valida procesamiento y transformaciÃ³n de respuestas provenientes de OpenStreetMap (OSM), asÃ­ como el manejo controlado de errores asociados a usuarios inexistentes. |
| `test_user_service.py`           | Usuarios          | Valida operaciones relacionadas con gestiÃ³n, procesamiento y recuperaciÃ³n de informaciÃ³n de usuarios dentro del sistema.                                             |
| `test_messaging_service.py`      | ComunicaciÃ³n      | Valida funcionalidades relacionadas con generaciÃ³n, procesamiento y envÃ­o de mensajes dentro del sistema de comunicaciÃ³n.                                            |
| `test_template_service.py`       | ComunicaciÃ³n      | Valida el procesamiento y renderizado de plantillas utilizadas en servicios de comunicaciÃ³n y mensajerÃ­a.                                                            |

### Directorios de pruebas relacionados

#### API

* `tests/api/messaging/`
* `tests/api/users/`

#### Backend

* `tests/backend/unit/services/messaging/`
* `tests/backend/unit/services/users/`

---

## 1.3 Dependencias controladas o simuladas

| Dependencia             | Tipo             | Objetivo                                                                           |
| :---------------------- | :--------------- | :--------------------------------------------------------------------------------- |
| OpenStreetMap (OSM)     | API externa      | Validar procesamiento de informaciÃ³n externa y transformaciÃ³n de datos de usuario. |
| SMTP Service            | Servicio externo | Validar procesos de verificaciÃ³n de correo electrÃ³nico y generaciÃ³n de mensajes.   |
| Tokens de autenticaciÃ³n | Seguridad        | Validar integridad y consistencia de autenticaciÃ³n y sesiones.                     |
| URLs de validaciÃ³n      | ComunicaciÃ³n     | Validar integridad de flujos de verificaciÃ³n de identidad.                         |



