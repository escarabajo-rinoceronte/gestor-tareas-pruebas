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
      <tr><td class="label">Proyecto</td><td>HOT Tasking Manager — EjecuciÃ³n de Casos de Prueba del MOD-02: ExploraciÃ³n de Proyectos</td></tr>
      <tr><td class="label">Fecha</td><td>12/06/2026</td></tr>
    </table>
  </div>

  <p class="ubicacion">Arequipa — Perú</p>
</div>

<br><br>

---

<br><br>
# EjecuciÃ³n de Casos de Prueba del MOD-02: ExploraciÃ³n de Proyectos

## 1. ESC-2001: Motor de BÃºsqueda y CombinaciÃ³n de Filtros Avanzados

### 1.1. EjecuciÃ³n de CP-2001-01

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-2001-01** | Verificar el estado inicial de la pantalla sin interactuar con los desplegables (sin filtros activos). | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La interfaz carga por defecto el catÃ¡logo completo de proyectos disponibles en el sistema (`CS-3 = V`). | La pantalla principal de exploraciÃ³n cargÃ³ de manera correcta e instantÃ¡nea la totalidad de las tarjetas de proyectos activos y archivados disponibles en la base de datos. |

| Evidencia |
| :-- |
| CatÃ¡logo Inicial Completo por Defecto<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-02-ejecucion-exploracion-proyectos/CP-2001-01-catalogo-defecto.png" width="800px" alt="CP-2001-01 - CatÃ¡logo completo sin filtros"></a><br>Captura de la pantalla "Explore Projects" mostrando el listado general de proyectos en su estado inicial. |

---

### 1.2. EjecuciÃ³n de CP-2001-02

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-2001-02** | Validar que la pantalla se actualice asÃ­ncronamente mostrando Ãºnicamente las tarjetas de proyectos cuyo estado sea "Activo". | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La pantalla se actualiza asÃ­ncronamente mostrando Ãºnicamente las tarjetas de proyectos cuyo estado sea "Activo" (`CS-1 = V`). | Al seleccionar el filtro de estado en 'Activo', la grilla de proyectos se refrescÃ³ mediante una peticiÃ³n asÃ­ncrona, ocultando los archivados y listando solo los vigentes. |

| Evidencia |
| :-- |
| Grilla Filtrada por Estado Activo<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-02-ejecucion-exploracion-proyectos/CP-2001-02-filtro-activo.png" width="800px" alt="CP-2001-02 - Listado filtrado por proyectos activos"></a><br>Vista de la UI mostrando Ãºnicamente las tarjetas que cumplen con la etiqueta de estado 'Activo'. |

---

### 1.3. EjecuciÃ³n de CP-2001-03

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-2001-03** | Validar la reducciÃ³n de elementos mostrando solo proyectos que sean "Activos" y para mappers "Easy" en simultÃ¡neo. | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La lista reduce sus elementos, mostrando solo los proyectos que son "Activos" y que simultÃ¡neamente aceptan mappers "Easy" (`CS-1 = V`). | La interfaz procesÃ³ la intersecciÃ³n lÃ³gica de ambos controles de selecciÃ³n, reduciendo la lista visible exclusivamente a proyectos vigentes de dificultad baja (Easy). |

| Evidencia |
| :-- |
| IntersecciÃ³n de Filtros Estado y Dificultad<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-02-ejecucion-exploracion-proyectos/CP-2001-03-filtro-combinado.png" width="800px" alt="CP-2001-03 - Filtros de Activo y Easy activos"></a><br>Captura de la interfaz de usuario con los selectores de Estado (Activo) y Dificultad (Easy) aplicados a la vez. |

---

### 1.4. EjecuciÃ³n de CP-2001-04

| ID | DescripciÃ³n | Tipo | Estado | Defectos |
| :-- | :-- | :-- | :-- | :-- |
| **CP-2001-04** | Validar la combinaciÃ³n final de tres filtros simultÃ¡neos (Estado: Activo, Dificultad: Easy, CampaÃ±a: Malaria). | Manual | Exitoso | Ninguno |

| Resultado esperado | Resultado obtenido |
| :-- | :-- |
| La interfaz procesa la intersecciÃ³n final. Muestra en pantalla solo los proyectos que cumplan estrictamente con los tres criterios en simultÃ¡neo, reflejando de forma clara que la combinaciÃ³n estÃ¡ vacÃ­a si no hay coincidencia. | La UI resolviÃ³ la consulta combinada correctamente de forma asÃ­ncrona. Al no existir registros en el entorno que reÃºnan las tres condiciones a la vez, la grilla ocultÃ³ todas las tarjetas y actualizÃ³ el contador de control a "0 de 0" proyectos encontrados. |

| Evidencia |
| :-- |
| **SelecciÃ³n de los Tres Filtros**<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-02-ejecucion-exploracion-proyectos/CP-2001-04-interseccion-tres-filtros.png" width="800px" alt="CP-2001-04 - Aplicando los tres filtros en la interfaz"></a><br>Captura del momento de ejecuciÃ³n aplicando los tres criterios simultÃ¡neos (Activo, Easy y CampaÃ±a Malaria) en la barra superior.<br><br>**Resultado de la Grilla con "0 de 0"**<br><a href="#--------"><img src="/tests-docs/03-ejecucion-de-pruebas/funcionales/img/MOD-02-ejecucion-exploracion-proyectos/CP-2001-04-resultado-cero.png" width="800px" alt="CP-2001-04 - Grilla vacÃ­a con contador mostrando 0 de 0"></a><br>Vista final de la interfaz tras procesar la consulta; se verifica que las tarjetas se ocultaron y el indicador visual numÃ©rico marca 0 de 0 resultados. |
