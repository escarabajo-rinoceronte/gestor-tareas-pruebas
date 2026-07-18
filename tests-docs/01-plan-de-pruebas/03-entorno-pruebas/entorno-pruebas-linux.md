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
  <b>Proyecto:</b> HOT Tasking Manager — GuÃ­a de ConfiguraciÃ³n del Entorno de Desarrollo Local <br>
  <b>Fecha de Elaboración:</b> 15/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# GuÃ­a de ConfiguraciÃ³n del Entorno de Desarrollo Local

## 1. Requisitos Previos del Sistema

Antes de comenzar, asegÃºrese de tener instaladas las siguientes herramientas. Los nombres de los paquetes pueden variar segÃºn su distribuciÃ³n:

*   **Git:** Para el control de versiones.
*   **Docker:** Motor de contenedores (v20.10+).
*   **Docker Compose:** Orquestador (v2.0+, preferiblemente el plugin nativo de Docker).

### InstalaciÃ³n de dependencias

#### **Arch Linux**
```bash
sudo pacman -S git docker docker-compose
```

#### **Debian / Ubuntu**
```bash
sudo apt update
sudo apt install git docker.io docker-compose-v2
```

#### **Fedora**
```bash
sudo dnf install git moby-engine docker-compose-plugin
```

> [!NOTE]
> AsegÃºrese de que su usuario tenga permisos para ejecutar Docker sin `sudo`. En la mayorÃ­a de las distros:
> `sudo usermod -aG docker $USER` (requiere cerrar y abrir sesiÃ³n).

---

## 2. ConfiguraciÃ³n Inicial del Proyecto

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/hotosm/tasking-manager.git
    cd tasking-manager
    ```

2.  **Preparar las Variables de Entorno:**
    El sistema se configura mediante un archivo `.env`. Copie el archivo de ejemplo proporcionado:
    ```bash
    cp tasking-manager.env.txt tasking-manager.env
    ```

---

## 3. ConfiguraciÃ³n de AutenticaciÃ³n (Paso CrÃ­tico)

Tasking Manager utiliza **OpenStreetMap (OSM)** para el inicio de sesiÃ³n. Sin esto, no podrÃ¡ acceder a las funciones de administraciÃ³n.

1.  Inicie sesiÃ³n en [OpenStreetMap.org](https://www.openstreetmap.org).
2.  Vaya a **My Settings -> OAuth 2 applications -> Register new application**.
3.  Configure los siguientes campos:
    *   **Name:** TM Local Dev
    *   **Redirect URI:** `http://127.0.0.1:3000/authorized` (Debe ser exactamente asÃ­).
    *   **Permissions:** `read_prefs` y `write_api`.
4.  Copie el `Client ID` y el `Client Secret` en su archivo `tasking-manager.env`:
    ```env
    TM_CLIENT_ID=su_client_id_aqui
    TM_CLIENT_SECRET=su_client_secret_aqui
    ```

---

## 4. EjecuciÃ³n con Docker Compose

El proyecto utiliza un flujo de construcciÃ³n multi-etapa. Para desarrollo, utilizaremos el target `debug` que permite recarga en vivo (hot-reload).

1.  **Construir las imÃ¡genes:**
    ```bash
    docker compose build
    ```

2.  **Levantar los servicios:**
    ```bash
    docker compose up -d
    ```

### Â¿QuÃ© sucede durante este proceso?
*   `tm-db`: Levanta una instancia de PostGIS.
*   `tm-migration`: Ejecuta automÃ¡ticamente las migraciones de Alembic para crear las tablas.
*   `tm-backend`: Inicia la API en Python (FastAPI/Flask) en modo debug.
*   `tm-frontend`: Inicia el servidor de desarrollo de React.
*   `traefik`: ActÃºa como proxy inverso en el puerto 3000.

---

## 5. ValidaciÃ³n del Entorno

Verifique que los servicios estÃ©n respondiendo correctamente:

*   **Frontend:** Acceda a `http://127.0.0.1:3000`. DeberÃ­a ver la interfaz principal.
*   **Backend (API):** Acceda a `http://127.0.0.1:3000/api/docs`. VerificarÃ¡ la documentaciÃ³n Swagger.
*   **Base de Datos:** El backend indicarÃ¡ en los logs si la conexiÃ³n fue exitosa.

---

## 6. Comandos de InspecciÃ³n y DepuraciÃ³n

Esta secciÃ³n es esencial para diagnosticar problemas durante el desarrollo.

### A. Contenedor del Backend (`tm-backend`)
El backend es el motor de lÃ³gica y conexiÃ³n a base de datos.

*   **Ver logs en tiempo real:**
    ```bash
    docker compose logs -f tm-backend
    ```
*   **Acceder a la terminal interna:**
    ```bash
    docker exec -it tm-backend bash
    ```
*   **Verificar variables de entorno cargadas:**
    ```bash
    docker exec tm-backend env | grep TM_
    ```
*   **Revisar procesos de Python activos:**
    ```bash
    docker exec tm-backend ps aux | grep python
    ```

### B. Contenedor del Frontend (`tm-frontend`)
Contenedor basado en Node.js para la interfaz React.

*   **Ver errores de compilaciÃ³n:**
    ```bash
    docker compose logs -f tm-frontend
    ```
*   **Reiniciar solo el frontend:**
    ```bash
    docker compose restart tm-frontend
    ```

### C. Contenedor de Base de Datos (`tm-db`)
Instancia de PostgreSQL + PostGIS.

*   **Acceder a la consola de PostgreSQL (psql):**
    ```bash
    docker exec -it tm-db psql -U tm -d tasking-manager
    ```
*   **Listar tablas para verificar migraciones:**
    ```sql
    -- Dentro de psql
    \dt
    ```
*   **Verificar logs de consultas y errores:**
    ```bash
    docker compose logs -f tm-db
    ```

### D. Comandos Globales Ãštiles
*   **Ver estado de salud de todos los servicios:**
    ```bash
    docker compose ps
    ```
*   **Limpiar el entorno completamente (borra datos de DB):**
    ```bash
    docker compose down -v
    ```

---

## 7. SoluciÃ³n de Problemas Comunes

1.  **Error de ConexiÃ³n a la DB:** Si el backend falla al iniciar, verifique que `tm-migration` haya terminado exitosamente. A veces la DB tarda mÃ¡s en estar lista; Docker Compose tiene un `healthcheck` configurado para mitigar esto.
2.  **Error de OAuth/Login:** Verifique que el `TM_APP_BASE_URL` en el archivo `.env` coincida exactamente con la URL que usa en el navegador (usualmente `http://127.0.0.1:3000`).
3.  **Puertos ocupados:** Si el puerto 3000 estÃ¡ en uso por otra aplicaciÃ³n, cÃ¡mbielo en el archivo `.env` mediante la variable `TM_DEV_PORT`.


