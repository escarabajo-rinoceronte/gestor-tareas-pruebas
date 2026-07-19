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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — EspecificaciÃ³n de Pruebas Unitarias: Seguridad, Usuarios y ComunicaciÃ³n</td></tr>
      <tr><td class="label">Fecha</td><td>29/05/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
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

