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
  <b>Proyecto:</b> HOT Tasking Manager — Entorno de Pruebas <br>
  <b>Fecha de Elaboración:</b> 12/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Entorno de Pruebas 

Este documento describe el entorno de pruebas utilizado para el proyecto **Tasking Manager**. El objetivo es que todos los integrantes del equipo puedan levantar y probar el sistema bajo las mismas condiciones, usando una configuraciÃ³n comÃºn basada en **Docker Compose**.

El entorno permite ejecutar el sistema de forma local, incluyendo la interfaz web, el backend, la base de datos, las migraciones y los servicios necesarios para que la aplicaciÃ³n funcione correctamente durante las pruebas.

---

## 1. Objetivo del entorno

El entorno de pruebas busca garantizar que las pruebas funcionales, unitarias e integrales se realicen sobre una misma configuraciÃ³n tÃ©cnica.

De esta manera, se evita que cada integrante pruebe el sistema en condiciones diferentes, como distintas versiones de Python, PostgreSQL, dependencias o configuraciones locales.

---

## 2. Arquitectura general del entorno

El proyecto proporciona un entorno compuesto por varios contenedores Docker. Cada contenedor cumple una funciÃ³n especÃ­fica dentro del sistema.

```mermaid
flowchart LR
    Tester[Tester / Usuario] --> Frontend[tm-frontend<br/>Interfaz web]
    Frontend --> Backend[tm-backend<br/>API del sistema]
    Backend --> DB[(tm-db<br/>PostgreSQL + PostGIS)]
    Migration[tm-migration<br/>Migraciones] --> DB
    Traefik[traefik<br/>Proxy] --> Frontend
    Traefik --> Backend
```

El usuario accede al sistema desde el navegador. El frontend muestra la interfaz web y se comunica con el backend. El backend procesa las operaciones del sistema y guarda la informaciÃ³n en la base de datos PostgreSQL con PostGIS.

---

## 3. Servicios principales del entorno

| Servicio       | FunciÃ³n                                                            |
| :------------- | :----------------------------------------------------------------- |
| `tm-frontend`  | Muestra la interfaz web del Tasking Manager.                       |
| `tm-backend`   | Ejecuta la API y la lÃ³gica principal del sistema.                  |
| `tm-db`        | Almacena la informaciÃ³n del sistema en PostgreSQL/PostGIS.         |
| `tm-migration` | Ejecuta las migraciones necesarias para preparar la base de datos. |
| `traefik`      | Gestiona el acceso y enrutamiento hacia los servicios.             |
| `tm-cron-jobs` | Ejecuta tareas programadas del sistema.                            |

---

## 4. Versiones verificadas

### Backend (`tm-backend`)

* **Python:** `3.10.20`
* **Framework:** FastAPI / Uvicorn
* **Migraciones:** Alembic `1.11.1`

### Frontend (`tm-frontend`)

* **Servidor web:** Nginx `1.31.1`

### Base de datos (`tm-db`)

* **PostgreSQL:** `14.9`
* **PostGIS:** `3.3.4`

### Proxy (`traefik`)

* **Traefik:** `3.6.1`

---

## 5. Variables de entorno principales

Las variables principales se definen en el archivo:

```txt
tasking-manager.env
```

| Variable            | Valor                |
| :------------------ | :------------------- |
| `POSTGRES_DB`       | `tasking-manager`    |
| `POSTGRES_USER`     | `tm`                 |
| `POSTGRES_PASSWORD` | `tm`                 |
| `POSTGRES_TEST_DB`  | `taskingmanagertest` |

Estas variables permiten que el backend, la base de datos y las pruebas trabajen con una configuraciÃ³n comÃºn.

---

## 6. CÃ³mo levantar el entorno

Desde la raÃ­z del proyecto

Levantar los servicios:

```powershell
docker compose up -d
```

Verificar el estado de los contenedores:

```powershell
docker compose ps
```

Acceder al sistema desde el navegador:

```txt
http://127.0.0.1:3000
```

---

## 7. Criterios para considerar el entorno listo

El entorno se considera listo para ejecutar pruebas cuando:

| Criterio      | Resultado esperado                                 |
| :------------ | :------------------------------------------------- |
| Base de datos | `tm-db` aparece en estado saludable.               |
| Backend       | `tm-backend` se encuentra levantado correctamente. |
| Frontend      | La aplicaciÃ³n carga desde `http://127.0.0.1:3000`. |
| Migraciones   | `tm-migration` finaliza sin errores.               |
| ComunicaciÃ³n  | El frontend puede comunicarse con el backend.      |

---



