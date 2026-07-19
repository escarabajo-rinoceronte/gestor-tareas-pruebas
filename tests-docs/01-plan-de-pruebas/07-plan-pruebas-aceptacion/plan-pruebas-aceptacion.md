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
  <b>Proyecto:</b> HOT Tasking Manager — Plan de Pruebas de Aceptación <br>
  <b>Fecha de Elaboración:</b> 20/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Plan de Pruebas de Aceptación

## 1. Objetivo

Definir la campaña de pruebas de aceptación para validar los tres módulos analizados del sistema desde la perspectiva del usuario final y sobre rutas reales del producto.

## 2. Alcance

| Módulo | RF incluidos | Casos |
| :--- | :--- | :---: |
| **MOD-01** Autenticación y Perfil | `RF-1001` a `RF-1004` | **6** |
| **MOD-02** Exploración de Proyectos | `RF-2001` a `RF-2003` | **5** |
| **MOD-03** Ejecución de Mapeo | `RF-3001` a `RF-3006` | **9** |
| **Total** | `RF-1001` a `RF-3006` | **20** |

## 3. Criterios de construcción

- Solo se consideran `MOD-01`, `MOD-02` y `MOD-03`.
- Se usan flujos reales ya observados en las ejecuciones funcionales del repositorio.
- Se evitan casos redundantes de frontera o validaciones demasiado técnicas para aceptación.
- Los casos están asociados a rutas reales del frontend.

## 5. Entorno mínimo

| Recurso | Necesidad |
| :--- | :--- |
| Frontend | Navegación funcional sobre `/explore`, `/projects/:id`, `/projects/:id/tasks`, `/projects/:id/map`, `/settings`, `/login`. |
| Backend | API operativa para autenticación, proyectos, tareas y licencias. |
| Datos | Proyecto público, proyecto privado, proyecto con licencia, tareas `READY` y usuario mapper. |
| Usuario | Usuario anónimo, usuario autenticado, usuario autorizado para proyecto privado. |

## 6. Resultado esperado

La campaña debe concluir con una decisión formal de:

- `APROBADO`
- `APROBADO CON OBSERVACIONES`
- `RECHAZADO`
